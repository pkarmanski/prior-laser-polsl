import logging

from app.enums.service_errors import ServiceError
from app.stage.daos.prior_connector import PriorConnector
from app.stage.errors.errors import StageExecuteError
from app.stage.factories.commands_factory import CommandsFactory
from app.stage.models.stage_models import DaoResponse, DaoError


class LaserDAO:
    def __init__(self, prior_connector: PriorConnector):
        self.__logger = logging.getLogger(__name__)
        self.__prior = prior_connector
        self.__laser_intput = 0

    def turn_laser(self, turn_on: bool):
        try:
            command = CommandsFactory.set_ttl_output_state(1) if turn_on else CommandsFactory.set_ttl_output_state(0)
            response = self.__prior.execute(command)
            return DaoResponse[str](data=response, error=DaoError(error=ServiceError.OK, description=""))
        except StageExecuteError as err:
            return DaoResponse[str](data="", error=DaoError(error=ServiceError.STAGE_ERROR,
                                                            description=str(err),
                                                            return_status=err.msg))


