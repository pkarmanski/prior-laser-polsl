"""
Class for directly accessing stage
"""

import logging
from typing import Any

from app.enums.service_errors import ServiceError
from app.stage.daos.stage_connector import StageConnector
from app.stage.errors.errors import StageConnectionError, StageExecuteError, StageOpenSessionError
from app.stage.factories.commands_factory import CommandsFactory
from app.stage.models.stage_models import StageResponse, StageError
from app.utils.yaml_manager import YamlData


class StageDAO:
    def __init__(self, yaml_data: YamlData):
        self.__yaml_data = yaml_data
        self.__com_port = self.__yaml_data.get_stage_com_port()
        self.__logger = logging.getLogger(__name__)
        self.__stage = StageConnector(self.__yaml_data.get_stage_ddl_path(), 1000)

    def set_com_port(self, com_port: int):
        self.__com_port = com_port

    def initialize(self) -> StageResponse[Any]:
        try:
            self.__stage.initialize()
            return StageResponse[Any](error=StageError(error=ServiceError.OK, description=""))
        except StageConnectionError as err:
            return StageResponse[Any](error=StageError(error=ServiceError.STAGE_ERROR, description=str(err),
                                                       return_status=err.msg))

    def open_session(self) -> StageResponse[str]:
        try:
            return_status = self.__stage.open_session(self.__com_port)
            return StageResponse[str](data=return_status, error=StageError(error=ServiceError.OK, description=""))
        except StageOpenSessionError as err:
            return StageResponse[str](data="", error=StageError(error=ServiceError.STAGE_OPEN_SESSION_ERROR,
                                                                description=str(err), return_status=err.msg))
        except StageExecuteError as err:
            return StageResponse[str](data="", error=StageError(error=ServiceError.STAGE_CONNECT_ERROR,
                                                                description=str(err), return_status=err.msg))

    def close_session(self) -> StageResponse:
        try:
            return_status = self.__stage.close_session()
            return StageResponse[str](data=return_status, error=StageError(error=ServiceError.OK, description=""))
        except (StageOpenSessionError, StageExecuteError) as err:
            return StageResponse[str](data="", error=StageError(error=ServiceError.STAGE_ERROR, description=str(err),
                                                                return_status=err.msg))

    def move_at_velocity(self, x: int, y: int) -> StageResponse:
        try:
            command = CommandsFactory.move_at_velocity(x, y)
            return_status = self.__stage.execute(command)
            return StageResponse[str](data=return_status, error=StageError(error=ServiceError.OK, description=""))
        except StageExecuteError as err:
            return StageResponse[str](data="", error=StageError(error=ServiceError.STAGE_ERROR, description=str(err),
                                                                return_status=err.msg))
