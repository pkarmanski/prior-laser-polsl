"""
Class for directly accessing stage
"""

import logging
from typing import Any, List

from app.enums.service_errors import ServiceError
from app.stage.daos.prior_connector import PriorConnector
from app.stage.errors.errors import StageExecuteError
from app.stage.factories.commands_factory import CommandsFactory
from app.stage.models.stage_models import StageResponse, StageError


class StageDAO:
    def __init__(self, prior_connector: PriorConnector):
        # self.__yaml_data = yaml_data
        # self.__com_port = None
        # self.__com_port = self.__yaml_data.get_stage_com_port()
        self.__logger = logging.getLogger(__name__)
        self.__stage = prior_connector
        self.__actual_speed = 1000
        self.running = False
        self.position = [0, 0]

    def goto_position(self, x: int, y: int, speed: int) -> StageResponse:
        try:
            if self.__actual_speed != speed:
                set_speed_command = CommandsFactory.set_max_speed(speed)
                self.__stage.execute(set_speed_command)
                self.__actual_speed = speed
            command = CommandsFactory.goto_position(x, y)
            response = self.__stage.execute(command)
            return StageResponse[str](data=response, error=StageError(error=ServiceError.OK, description=""))
        except StageExecuteError as err:
            return StageResponse[str](data="", error=StageError(error=ServiceError.STAGE_ERROR, description=str(err),
                                                                return_status=err.msg))

    def move_at_velocity(self, x_speed: int, y_speed: int) -> StageResponse:
        try:
            command = CommandsFactory.move_at_velocity(x_speed, y_speed)
            return_status = self.__stage.execute(command)
            return StageResponse[str](data=return_status, error=StageError(error=ServiceError.OK, description=""))
        except StageExecuteError as err:
            return StageResponse[str](data="", error=StageError(error=ServiceError.STAGE_ERROR, description=str(err),
                                                                return_status=err.msg))

    def check_stage_limits(self) -> StageResponse:
        try:
            command = CommandsFactory.get_limits()
            stage_limits = int(self.__stage.execute(command))
            return StageResponse[int](data=stage_limits, error=StageError(error=ServiceError.OK, description=""))
        except StageExecuteError as err:
            return StageResponse[str](data="", error=StageError(error=ServiceError.STAGE_ERROR, description=str(err),
                                                                return_status=err.msg))

    def set_position(self, x: int, y: int) -> StageResponse:
        try:
            command = CommandsFactory.set_position(x, y)
            return_status = self.__stage.execute(command)
            return StageResponse[str](data=return_status, error=StageError(error=ServiceError.OK, description=""))
        except StageExecuteError as err:
            return StageResponse[str](data="", error=StageError(error=ServiceError.STAGE_ERROR, description=str(err),
                                                                return_status=err.msg))

    def get_position(self) -> StageResponse[List]:
        try:
            command = CommandsFactory.get_position()
            position = self.__stage.execute(command)  # TODO check behaviour
            self.__logger.info('**************************')
            position = [int(coordinate) for coordinate in position.split(',')]
            self.position = position
            self.__logger.info(position)
            return StageResponse[List](data=position, error=StageError(error=ServiceError.OK, description=""))
        except StageExecuteError as err:
            return StageResponse[List](data=[], error=StageError(error=ServiceError.STAGE_ERROR,
                                                                  description=str(err),
                                                                  return_status=err.msg))

    def get_running(self) -> StageResponse[bool]:
        try:
            command = CommandsFactory.get_busy()
            running = self.__stage.execute(command)
            self.running = True if running != "0" else False
            return StageResponse[bool](data=running != "0", error=StageError(error=ServiceError.OK, description=""))
        except StageExecuteError as err:
            return StageResponse[bool](data=None, error=StageError(error=ServiceError.STAGE_ERROR,
                                                                 description=str(err),
                                                                 return_status=err.msg))

    def stop_stage(self) -> StageResponse[bool]:
        try:
            command = CommandsFactory.stop_smoothly()
            stopped = self.__stage.execute(command)  # TODO check behaviour
            return StageResponse[bool](data=stopped == 0, error=StageError(error=ServiceError.OK, description=""))
        except StageExecuteError as err:
            return StageResponse[bool](data=None, error=StageError(error=ServiceError.STAGE_ERROR,
                                                                 description=str(err),
                                                                 return_status=err.msg))
