import math
from typing import List

from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPen

from app.files_processing.enums import Figures
from app.files_processing.models import Entity
from app.presentation.window_utils.window_utils import WindowUtils
from app.consts.presentation_consts import PRESENTATION_OFFSET


class CanvasDrawingService:
    @classmethod
    def draw(cls, painter: QPainter, entities: List[Entity], scale: int) -> None:
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        for entity in entities:
            coords, radius, entity_type, params = entity.coords, entity.radius, entity.entity_type, entity.params

            scaled_coords = [(x * scale, y * scale) for x, y in coords]

            if radius is not None:
                scaled_radius = radius * scale

            match entity_type:
                case Figures.LINE:
                    cls.draw_line(painter, scaled_coords)

                case Figures.CIRCLE:
                    cls.draw_circle(painter, scaled_coords, scaled_radius)

                case Figures.ARC:
                    cls.draw_arc(painter, scaled_coords, scaled_radius)

                case Figures.ELLIPSE:
                    cls.draw_ellipse(painter, scaled_coords, params)

                case _:
                    pass

    @staticmethod
    def draw_line(painter: QPainter, coords: list) -> None:
        start, end = coords
        start = WindowUtils.convert_float_to_int_list(start)
        end = WindowUtils.convert_float_to_int_list(end)

        painter.drawLine(start[0] + PRESENTATION_OFFSET, start[1] + PRESENTATION_OFFSET,
                         end[0] + PRESENTATION_OFFSET, end[1] + PRESENTATION_OFFSET)

    @staticmethod
    def draw_arc(painter: QPainter, coords: list, radius: float) -> None:
        start_point, center, end_point = coords
        start_point = WindowUtils.convert_float_to_int_list(start_point)
        end_point = WindowUtils.convert_float_to_int_list(end_point)
        center = WindowUtils.convert_float_to_int_list(center)

        radius = int(radius)
        rect = (
            center[0] - radius + PRESENTATION_OFFSET, center[1] - radius + PRESENTATION_OFFSET,
            radius * 2, radius * 2
        )
        start_angle = math.degrees(math.atan2(start_point[1] - center[1], start_point[0] - center[0]))
        end_angle = math.degrees(math.atan2(end_point[1] - center[1], end_point[0] - center[0]))
        span_angle = end_angle - start_angle
        painter.drawArc(*rect, int(start_angle * 16), int(span_angle * 16))

    @staticmethod
    def draw_circle(painter: QPainter, coords: list, radius: float) -> None:
        center = WindowUtils.convert_float_to_int_list(coords[0])
        radius = int(radius/100)
        rect = (
            center[0] + PRESENTATION_OFFSET, center[1] + PRESENTATION_OFFSET,
            radius * 2, radius * 2
        )
        painter.drawEllipse(*rect)

    @staticmethod
    def draw_point(painter: QPainter, coords: list) -> None:
        x, y = WindowUtils.convert_float_to_int_list(coords[0])
        painter.drawPoint(x, y)

    @staticmethod
    def draw_ellipse(painter: QPainter, coords: list, params) -> None:
        coords = WindowUtils.convert_float_to_int_list(coords[0])
        x, y = coords
        major_axis, ratio, start_param, end_param = params
        maj_x, maj_y = major_axis
        major_length = math.sqrt(int(maj_x) ** 2 + int(maj_y) ** 2)
        minor_length = major_length * ratio

        top_left = QPointF(
            x - major_length / 2,
            y - minor_length / 2
        )
        size = (major_length, minor_length)

        painter.drawEllipse(top_left, size[0], size[1])


    @staticmethod
    def draw_lwpolyline(painter: QPainter, coords: list) -> None:
        pass

    @staticmethod
    def draw_polyline(painter: QPainter, center: list, params: list) -> None:
        pass
