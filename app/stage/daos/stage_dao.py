"""
Class for directly accessing stage
"""

from ctypes import create_string_buffer, WinDLL
import logging
from app.utils.yaml_manager import YamlData
from app.messages.error_messages import StageErrorMsg
from app.messages.info_messages import StageInfoMsg

logger = logging.getLogger(__name__)


class StageDAO:
    """
    Attributes:
        :arg __yaml_data: YamlData() instance to get data from a yaml file
        :arg rx: buffer for communication with stage
        :arg com_port: com port in computer to communicate with stage
        :arg __SDKPrior: instance of stage
        :arg __session_id: stores session id of current session
    """
    __SDKPrior = None
    __session_id = -1

    def __init__(self):
        self.__yaml_data = YamlData()
        self.rx = create_string_buffer(1000)
        self.config_prior_connection()
        self.com_port = self.__yaml_data.get_stage_com_port()

    def config_prior_connection(self):
        path = self.__yaml_data.get_stage_ddl_path()
        self.__SDKPrior = WinDLL(path)

        # initializing SDKPrior
        ret = self.__SDKPrior.PriorScientificSDK_Initialise()
        if ret:
            logger.critical(StageErrorMsg.PRIOR_INITIALIZATION_ERROR.description.format(ret))
        else:
            logger.info(StageInfoMsg.PRIOR_INITIALIZED.description.format(ret))

        # opening new session
        self.__session_id = self.__SDKPrior.PriorScientificSDK_OpenNewSession()
        if self.__session_id < 0:
            logger.critical(StageErrorMsg.PRIOR_SESSION_ERROR.description.format(self.__session_id))
        else:
            logger.info(StageInfoMsg.PRIOR_SESSION_CREATED.description.format(self.__session_id))

        # TODO: here connecting to proper com port, checking connection

