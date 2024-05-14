from typing import List
from serial.tools import list_ports


class StageUtils:
    @staticmethod
    def get_coms() -> List[str]:
        return [port for port, _, _ in list_ports.comports()]
