from typing import List, Tuple
from serial.tools import list_ports
import random

class StageUtils:
    @staticmethod
    def get_coms() -> List[str]:
        return [port for port, _, _ in list_ports.comports()]

    @staticmethod
    def scale_list_points(points_canvas: List[Tuple[int, int]], scale_x: float, scale_y: float) -> List[Tuple[int, int]]:
        return [(int(x * scale_x), int(y * scale_y)) for x, y in points_canvas]

    @staticmethod
    def generate_random_stage_position() -> List:
        return [random.random(), random.random(), True if random.randint(0, 1) else False]
