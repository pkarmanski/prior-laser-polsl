"""
This class will talk with repositories and will have logic for error handling
and what to return to window when error happens
"""
import logging
import time

from app.enums.service_errors import ServiceError
from app.laser.laser_connector import LaserConnector
from app.models.service_models import StageStatus, ServiceAppParams
from app.stage.daos.stage_dao import StageDAO
from app.stage_utils.utils import StageUtils
from app.stage_utils.yaml_manager import YamlData
from typing import List, Tuple


class Service:
    def __init__(self):
        self.__yaml = YamlData()
        self.__stage_dao = StageDAO(self.__yaml)
        # self.__stage_dao.initialize() # FIXME: uncomment after tests with arduino
        self.__running_thread = None
        self.__laser_connector = None
        self.__service_app_params = None
        self.__logger = logging.getLogger(__name__)

    def init_stage(self, com_port: str):
        com_port = int(com_port[3:])
        self.__stage_dao.initialize(com_port)

    def init_laser(self, com_port: str):
        self.__laser_connector = LaserConnector(com_port)

    def laser_write(self, value):
        self.__logger.info(self.__laser_connector)
        self.__laser_connector.write_data(value)

    def get_stage_status(self) -> StageStatus:
        return StageStatus(running=self.__stage_dao.running, position=self.__stage_dao.position)

    def open_session(self, com: str = "") -> ServiceError:
        com = self.__yaml.get_stage_com_port() if not com else ""
        self.__stage_dao.set_com_port(int(com))  # Fixme removed [-1] for testing
        open_session_response = self.__stage_dao.open_session()
        if open_session_response.error.error == ServiceError.STAGE_CONNECT_ERROR:
            self.__stage_dao.close_session(close_normally=False)
        return open_session_response.error.error

    def close_session(self):
        close_session_response = self.__stage_dao.close_session()
        return close_session_response.error.error
        # if close_session_response.error.error == ServiceError.STAGE_ERROR:
        #     pass
        #     # TODO info do frontu?

    def set_service_params(self, stage_width: int, stage_height: int, canvas_width: int, canvas_height: int):
        self.__service_app_params = ServiceAppParams(scale_x=stage_width / canvas_width, scale_y=stage_height / canvas_height)


    # TODO check if function is working while stage is connected
    def calibrate(self, canvas_width: int, canvas_height: int) -> ServiceError:
        self.__stage_dao.running = True
        move_at_velocity_response = self.__stage_dao.move_at_velocity(-7000, -7000)
        if move_at_velocity_response.error.error != ServiceError.OK:
            return ServiceError.STAGE_CALIBRATION_ERROR
        limits = 0
        error_count = 0
        while limits != 10:
            limit_check_response = self.__stage_dao.check_stage_limits()
            if limit_check_response.error.error != ServiceError.OK:
                error_count += 1
                if error_count > 3:
                    self.__stage_dao.running = False
                    self.__stage_dao.move_at_velocity(0, 0)
                    return ServiceError.STAGE_CALIBRATION_ERROR
            else:
                limits = limit_check_response.data
            time.sleep(1)

        self.__stage_dao.running = False
        position = self.__stage_dao.get_position().data

        if position:
            self.set_service_params(position[0], position[1], canvas_width, canvas_height)
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

    def print_lines(self, lines: List[List[Tuple[int, int]]]):
        for line in lines:
            scaled_lines = StageUtils.scale_list_points(line,
                                                        self.__service_app_params.scale_x,
                                                        self.__service_app_params.scale_y)



