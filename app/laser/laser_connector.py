import logging
import time

import serial

from app.enums.service_errors import ServiceError
from app.stage.models.stage_models import DaoResponse, DaoError


class LaserConnector:
    def __init__(self, com_port):
        self.__com_port = com_port
        self.__baudrate = 115200
        self.__timeout = 0.1
        self.__laser = None
        self.__logger = logging.getLogger(__name__)

    def connect(self) -> DaoResponse[str]:
        try:
            self.__logger.info("connecting to laser")
            self.__laser = serial.Serial(self.__com_port, self.__baudrate, timeout=self.__timeout)
            if self.__laser.isOpen():
                return DaoResponse[str](data="", error=DaoError(error=ServiceError.OK, description=""))
            return DaoResponse[str](data="", error=DaoError(error=ServiceError.LASER_ERROR, description=""))
        except Exception as err:
            self.__logger.error(err)
            return DaoResponse[str](data="", error=DaoError(error=ServiceError.LASER_ERROR, description=str(err)))

    def write_data(self, value: str) -> DaoResponse[str]:
        try:
            self.__laser.write(bytes(value, 'utf-8'))
            time.sleep(0.1)
            response = self.__laser.readline()
            return DaoResponse[str](data=str(response), error=DaoError(error=ServiceError.OK, description=""))
        except Exception as err:
            self.__logger.error(err)
            return DaoResponse[str](data="", error=DaoError(error=ServiceError.LASER_ERROR, description=str(err)))
