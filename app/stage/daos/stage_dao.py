"""
Class for directly accessing stage
"""

import logging

from app.stage.daos.stage import Stage
from app.utils.yaml_manager import YamlData


class StageDAO:
    def __init__(self):
        self.__yaml_data = YamlData()
        self.__com_port = self.__yaml_data.get_stage_com_port()
        self.__logger = logging.getLogger(__name__)
        self.__stage = Stage(self.__yaml_data.get_stage_ddl_path(), 1000, self.__com_port)



