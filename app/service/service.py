"""
This class will talk with repositories and will have logic for error handling
and what to return to window when error happens
"""
from app.enums.service_errors import ServiceError
from app.stage.daos.stage_dao import StageDAO
from app.utils.yaml_manager import YamlData


class Service:
    def __init__(self):
        self.__yaml = YamlData()
        self.__stage_dao = StageDAO(self.__yaml)
        self.__stage_dao.initialize()

    def open_session(self, com: int):
        self.__stage_dao.set_com_port(com)
        open_session_response = self.__stage_dao.open_session()
        if open_session_response.error.error == ServiceError.STAGE_CONNECT_ERROR:
            self.__stage_dao.close_session()
        return open_session_response.error

    def close_session(self):
        close_session_response = self.__stage_dao.close_session()

    # def calibrate(self):
        # self.__stage_dao.move_at_velocity(x,y)

