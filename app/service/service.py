"""
This class will talk with repositories and will have logic for error handling
and what to return to window when error happens
"""
import logging
import math
import time
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from ezdxf.layouts import Modelspace
from app.files_processing.file_reading import DXFReader
from app.files_processing.enums import Figures
from app.enums.service_errors import ServiceError
from app.laser.laser_connector import LaserConnector
from app.laser.laser_dao import LaserDAO
from app.models.service_models import StageStatus, ServiceAppParams
from app.presentation.components.canvas.canvas import Canvas
from app.stage.daos.prior_connector import PriorConnector
from app.stage.daos.stage_dao import StageDAO
from app.stage_utils.utils import StageUtils
from app.stage_utils.yaml_manager import YamlData
from app.presentation.services.canvas_drawing import CanvasDrawingService
from typing import List, Tuple


class Service:
    def __init__(self):
        self.__yaml = YamlData()
        self.__prior_connector = PriorConnector(self.__yaml.get_stage_ddl_path(), 1000)
        self.__stage_dao = StageDAO(self.__prior_connector)
        self.__laser_dao = LaserDAO(self.__prior_connector)
        self.__dxf_reader = None
        self.__running_thread = None
        self.__laser_connector = None
        self.__service_app_params = None

        self.__is_prior_connected = False
        self.__logger = logging.getLogger(__name__)

    # FIXME needs to be executed in other thread
    # FIXME Timeout needs to be added
    def init_prior(self, com_port: str) -> ServiceError:
        try:
            com_port = int(com_port[3:])
            self.__prior_connector.initialize(com_port)
            response = self.__prior_connector.open_session()
            if response == "0":
                self.__is_prior_connected = True
                return ServiceError.OK
            self.__logger.error(response)
            return ServiceError.PRIOR_CONNECT_ERROR
        except Exception as e:
            self.__logger.error(e)
            return ServiceError.PRIOR_CONNECT_ERROR

    def close_session(self) -> ServiceError:
        try:
            self.__stage_dao.stop_stage()
            self.__prior_connector.disconnect_stage()
            close_session_response = self.__prior_connector.close_session()
            if close_session_response == "0":
                return ServiceError.OK
            self.__logger.error(close_session_response)
            return ServiceError.PRIOR_DISCONNECT_ERROR
        except AttributeError:
            return ServiceError.OK
        except Exception as e:
            self.__logger.error(e)
            return ServiceError.PRIOR_DISCONNECT_ERROR

    def init_laser(self, com_port: str) -> ServiceError:
        self.__laser_connector = LaserConnector(com_port)
        response = self.__laser_connector.connect()
        return response.error.error

    def laser_write(self, value) -> ServiceError:
        self.__logger.info(self.__laser_connector)
        response = self.__laser_connector.write_data(value)
        return response.error.error

    def get_stage_status(self) -> StageStatus:
        return StageStatus(running=self.__stage_dao.get_running(), position=self.__stage_dao.position)

    def set_service_params(self, stage_width: int, stage_height: int, canvas_width: int, canvas_height: int):
        self.__service_app_params = ServiceAppParams(scale_x=stage_width / canvas_width,
                                                     scale_y=stage_height / canvas_height)

    def calibrate(self, canvas_width: int, canvas_height: int) -> ServiceError:
        move_at_velocity_response = self.__stage_dao.move_at_velocity(-10000, -10000) # TODO: parameter
        if move_at_velocity_response.error.error != ServiceError.OK:
            return ServiceError.STAGE_CALIBRATION_ERROR
        limits = 0
        error_count = 0
        while limits != 10:
            limit_check_response = self.__stage_dao.check_stage_limits()
            if limit_check_response.error.error != ServiceError.OK:
                error_count += 1
                if error_count > 3:
                    self.__stage_dao.set_running(False)
                    self.__stage_dao.move_at_velocity(0, 0)
                    return ServiceError.STAGE_CALIBRATION_ERROR
            else:
                limits = limit_check_response.data
            time.sleep(1)

        self.__stage_dao.move_at_velocity(0, 0)
        self.__stage_dao.set_position(0, 0)

        # checking width and height
        move_at_velocity_response = self.__stage_dao.move_at_velocity(10000, 10000)   # TODO: parameter
        if move_at_velocity_response.error.error != ServiceError.OK:
            return ServiceError.STAGE_CALIBRATION_ERROR
        limits = 0
        error_count = 0
        while limits != 5:
            limit_check_response = self.__stage_dao.check_stage_limits()
            if limit_check_response.error.error != ServiceError.OK:
                error_count += 1
                if error_count > 3:
                    self.__stage_dao.set_running(False)
                    self.__stage_dao.move_at_velocity(0, 0)
                    return ServiceError.STAGE_CALIBRATION_ERROR
            else:
                limits = limit_check_response.data
            time.sleep(1)
        self.__stage_dao.move_at_velocity(0, 0)
        position = self.__stage_dao.get_position().data

        if position:
            self.set_service_params(position[0], position[1], canvas_width, canvas_height)
            self.__stage_dao.goto_position(int(position[0]/2), int(position[1]/2), speed=10000)
            while self.__stage_dao.get_running().data:
                time.sleep(1)
            self.__stage_dao.set_position(0, 0)
        return ServiceError.OK

    @staticmethod
    def get_coms() -> List[str]:
        return StageUtils.get_coms()

    def go_to_position(self, file_path: str):
        with open(file_path, "r") as file:
            positions = file.read()
            file.close()
            positions = positions.split("\n")
            positions = [[int(coordinate) for coordinate in position.split(',')] for position in positions[1:]]
            for x, y in positions:
                self.__stage_dao.goto_position(x, y, speed=10000)
                time.sleep(0.2)
        return_stopped = self.__stage_dao.stop_stage()
        if return_stopped.error == ServiceError.OK:
            self.__logger.info("***********************GIT")

    def check_position(self):
        spectrum = (x for x in range(200))
        for _ in spectrum:
            is_running_response = self.__stage_dao.get_running()
            if is_running_response.data is None:
                break
            elif is_running_response.data == 0:
                time.sleep(0.2)
                continue
            else:
                positions_response = self.__stage_dao.get_position()
            if positions_response.error == ServiceError.OK:
                self.__logger.info(positions_response.data)
            time.sleep(0.2)

    # TODO: proper laser switching and consider triggers
    def print_lines(self, lines: List[List[Tuple[int, int]]], dxf_file_path: str, from_canvas: bool, scale: int):
        if from_canvas:
            scaled_lines = [StageUtils.scale_list_points(line, scale, scale) for line in lines]
            for line in scaled_lines:
                self.__stage_dao.goto_position(line[-1][0], line[-1][1], speed=10000)
                while self.__stage_dao.get_running().data:
                    time.sleep(0.2)
                # Setting start laser position
                self.__laser_dao.turn_laser(True)

                position = len(line) - 1
                error_counter = 0
                while line:
                    x, y = line[position]
                    response = self.__stage_dao.goto_position(x, y, speed=10000)
                    if response.data == "0":
                        position -= 1
                        line.pop()
                        error_counter = 0
                    else:
                        time.sleep(0.1)
                        error_counter += 1

                    if error_counter > 100:
                        self.__stage_dao.stop_stage()
                        self.__laser_dao.turn_laser(False)
                        return ServiceError.STAGE_BUFFER_ERROR
                while self.__stage_dao.get_running().data:
                    time.sleep(0.2)
                self.__laser_dao.turn_laser(False)
            return ServiceError.OK
        else:
            if dxf_file_path:
                self.__dxf_reader = DXFReader(dxf_file_path)
                dxf_file = self.__dxf_reader.read_dxf_file()
                if dxf_file:
                    return self.draw(dxf_file.modelspace())
            return ServiceError.DXF_ERROR

    def draw_circles(self, radius: int, duration: int = 10, points: int = 200):
        dt = duration / points
        omega = 2 * math.pi / duration

        for i in range(points):
            t = i * dt
            v_x = int(-radius * omega * math.sin(omega * t))
            v_y = int(radius * omega * math.cos(omega * t))
            self.__stage_dao.move_at_velocity(v_x, v_y)
            time.sleep(dt)

        self.__stage_dao.stop_stage()

    def draw_arc(self, radius: int, angle: float, duration: int = 50, points: int = 200):
        dt = duration / points
        omega_full_circle = 2 * math.pi / duration
        omega = omega_full_circle * (angle / (2 * math.pi))

        for i in range(points):
            t = i * dt * (angle / (2 * math.pi))
            v_x = int(-radius * omega * math.sin(omega * t))
            v_y = int(radius * omega * math.cos(omega * t))
            self.__stage_dao.move_at_velocity(v_x, v_y)
            time.sleep(dt)

        self.__stage_dao.stop_stage()

    def draw(self, entities: Modelspace):
        for entity in entities:
            coords, radius, entity_type = self.__dxf_reader.get_coordinates(entity)
            entity_type =Figures.CIRCLE
            radius = 10000
            start_point = (0, 0)#coords[0]
            self.__stage_dao.goto_position(start_point[0], start_point[1], speed=10000)
            while self.__stage_dao.get_running().data:
                time.sleep(0.2)
            # Setting start laser position
            self.__laser_dao.turn_laser(True)

            if entity_type == Figures.LINE:
                end_point = coords[1]
                self.__stage_dao.goto_position(end_point[0], end_point[1], speed=10000)

            elif entity_type == Figures.ARC:
                center_point = coords[1]
                end_point = coords[2]
                angle = StageUtils.calculate_arc_angle(start_point, center_point, end_point)
                self.draw_arc(radius, angle)

            elif entity_type == Figures.CIRCLE:
                self.draw_circles(radius=radius, duration=10)
            elif entity_type == Figures.NONE:
                # TODO
                pass
            while self.__stage_dao.get_running().data:
                time.sleep(0.2)
            self.__laser_dao.turn_laser(False)
        return ServiceError.OK

    def get_stage_info(self) -> List:
        if self.__is_prior_connected:
            response = self.__stage_dao.get_position()
            if response.error.error == ServiceError.OK:
                x, y = response.data
            else:
                x, y = "Err", "Err"
        else:
            x, y = "NONE", "NONE"
        return [x, y, self.__stage_dao.get_running()]

    def draw_file_preview(self, check_box_click: bool, selected_file: str, canvas: Canvas, scale: int):
        if selected_file == "":
            return

        if check_box_click:
            return

        canvas.clear_canvas()

        self.__dxf_reader = DXFReader(selected_file)
        dxf_file = self.__dxf_reader.get_dxf_file()
        if dxf_file:
            return CanvasDrawingService(canvas).draw(entities=self.__dxf_reader.get_figures(), scale=scale)
