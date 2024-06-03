import math
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

    @staticmethod
    def calculate_arc_angle(start, center, end, radius) -> float:
        x1, y1 = start
        cx, cy = center
        x2, y2 = end

        vector_start = (x1 - cx, y1 - cy)
        vector_end = (x2 - cx, y2 - cy)

        angle_start = math.atan2(vector_start[1], vector_start[0])
        angle_end = math.atan2(vector_end[1], vector_end[0])

        arc_angle = angle_end - angle_start

        if arc_angle < 0:
            arc_angle += 2 * math.pi

        return arc_angle
