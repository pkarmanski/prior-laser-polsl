"""
This class will talk with repositories and will have logic for error handling
and what to return to window when error happens
"""
import time

from app.enums.service_errors import ServiceError
from app.models.service_models import StageStatus
from app.stage.daos.stage_dao import StageDAO
from app.utils.utils import Utils
from app.utils.yaml_manager import YamlData


class Service:
    def __init__(self):
        self.__yaml = YamlData()
        self.__stage_dao = StageDAO(self.__yaml)
        self.__stage_dao.initialize()
        self.__running_thread = None

    def get_stage_status(self) -> StageStatus:
        return StageStatus(running=self.__stage_dao.running, position=self.__stage_dao.position)

    def open_session(self, com: str) -> ServiceError:
        self.__stage_dao.set_com_port(int(com[-1]))
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

    def calibrate(self) -> ServiceError:
        self.__stage_dao.running = True
        move_at_velocity_response = self.__stage_dao.move_at_velocity(-1000, -1000)
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
        self.__stage_dao.move_at_velocity(0, 0)
        self.__stage_dao.set_position(0, 0)
        return ServiceError.OK

    def get_coms(self) -> List[str]:
        return Utils.get_coms()
