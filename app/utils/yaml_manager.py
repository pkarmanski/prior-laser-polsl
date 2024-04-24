import yaml
import logging


logger = logging.getLogger(__name__)


class YamlData:
    def __init__(self, filename='config.yaml'):
        try:
            with open(filename) as f:
                self.data = yaml.safe_load(f)
                f.close()
        except EnvironmentError as e:
            logger.critical(f"YAML: {e}")
            exit(1)

    def get_stage_ddl_path(self) -> str:
        return self.data["stage_params"]['path']

    def get_stage_com_port(self) -> int:
        return self.stage_data['port']
