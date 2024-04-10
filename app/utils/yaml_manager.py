import yaml
import logging


logger = logging.getLogger(__name__)


class YamlData:
    def __init__(self, filename='confiig.yaml'):
        try:
            with open(filename) as f:
                self.data = yaml.load(f, Loader=yaml.FullLoader)
                self.stage_data = self.data['stage_params']
                f.close()
        except EnvironmentError:
            logger.critical("YAML")
            exit(1)

    def get_stage_ddl_path(self) -> str:
        return self.stage_data('path')

    def get_stage_com_port(self) -> int:
        return self.stage_data['port']
