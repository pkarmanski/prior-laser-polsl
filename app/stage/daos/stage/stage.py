import logging
from ctypes import create_string_buffer, WinDLL

from app.messages.error_messages import StageErrorMsg
from app.messages.info_messages import StageInfoMsg
from app.stage.errors.errors import StageConnectionError, StageOpenSessionError, StageCloseSessionError


class Stage:
    """
    Attributes:
        :arg __yaml_data: YamlData() instance to get data from a yaml file
        :arg __read_buffer: buffer for communication with stage
        :arg com_port: com port in computer to communicate with stage
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
            self.__logger.critical(StageErrorMsg.PRIOR_INITIALIZATION_ERROR.description.format(return_status))
            raise StageConnectionError(str(return_status))
        else:
            self.__logger.info(StageInfoMsg.PRIOR_INITIALIZED.description.format(return_status))

    def open_session(self):
        self.__session_id = self.__SDKPrior.PriorScientificSDK_OpenNewSession()
        if self.__session_id < 0:
            self.__logger.critical(StageErrorMsg.PRIOR_SESSION_ERROR.description.format(self.__session_id))
            raise StageOpenSessionError(str(self.__session_id))
        else:
            self.__logger.info(StageInfoMsg.PRIOR_SESSION_CREATED.description.format(self.__session_id))

    def close_session(self):
        return_status = self.__SDKPrior.PriorScientificSDK_CloseSession(self.__session_id)
        if return_status:
            self.__logger.critical(StageErrorMsg.PRIOR_SESSION_ERROR.description.format(return_status))
            raise StageCloseSessionError(str(return_status))
        else:
            self.__logger.info(StageInfoMsg.PRIOR_SESSION_CREATED.description.format(return_status))

    def execute(self):
        pass
