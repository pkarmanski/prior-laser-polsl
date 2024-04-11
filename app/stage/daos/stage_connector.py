import logging
from ctypes import create_string_buffer, WinDLL

from app.messages.error_messages import StageErrorMsg
from app.messages.info_messages import StageInfoMsg
from app.stage.errors.errors import StageConnectionError, StageOpenSessionError, StageCloseSessionError, \
    StageExecuteError


class StageConnector:
    """
    Attributes:
        :arg __yaml_data: YamlData() instance to get data from a yaml file
        :arg __read_buffer: buffer for communication with stage
        :arg __com_port: com port in computer to communicate with stage
        :arg __SDKPrior: instance of stage
        :arg __session_id: stores session id of current session
    """

    # TODO: here connecting to proper com port, checking connection
    def __init__(self, path: str, reading_buffer_size: int, com_port: int):
        self.__logger = logging.getLogger(__name__)
        self.__stage_dll_path = path
        self.__read_buffer = create_string_buffer(reading_buffer_size)
        self.__com_port = com_port
        self.__SDKPrior = None
        self.__session_id = None

    def initialize(self):
        self.__SDKPrior = WinDLL(self.__stage_dll_path)
        return_status = self.__SDKPrior.PriorScientificSDK_Initialise()
        if return_status:
            self.__logger.critical(f"Prior initialization error: {return_status}")
            raise StageConnectionError(str(return_status))
        else:
            self.__logger.info(f"Prior initialized: {return_status}")

    def open_session(self):
        self.__session_id = self.__SDKPrior.PriorScientificSDK_OpenNewSession()
        if self.__session_id < 0:
            self.__logger.critical(f"Open session error: {self.__session_id}")
            raise StageOpenSessionError(str(self.__session_id))
        else:
            self.__logger.info(f"Session opened: {self.__session_id}")

    def close_session(self):
        return_status = self.__SDKPrior.PriorScientificSDK_CloseSession(self.__session_id)
        if return_status:
            self.__logger.critical(f"Session close error: {return_status}")
            raise StageCloseSessionError(str(return_status))
        else:
            self.__logger.info(f"Session closed: {return_status}")

    def execute(self, message: str):
        self.__logger.info(f"Executed message: {message}")
        return_status = self.__SDKPrior.PriorScientificSDK_cmd(self.__session_id,
                                                               create_string_buffer(message.encode()),
                                                               self.__read_buffer)
        if return_status:
            self.__logger.critical(f"Api error {return_status}")
            raise StageExecuteError(str(return_status))
        else:
            self.__logger.info(f"Success {self.__read_buffer.value.decode()}")
        # TODO think if return is needed
        # input("Press ENTER to continue...")
        # return return_status, self.__read_buffer.value.decode()
