import math
from typing import List

from PyQt5.QtCore import Qt, QPoint, QRect, QPointF
from PyQt5.QtGui import QPainter, QPen, QTransform

from app.files_processing.enums import Figures
from app.files_processing.models import Entity
from app.presentation.window_utils.window_utils import WindowUtils
from app.consts.presentation_consts import PRESENTATION_OFFSET, SCALE_MAPPING


class CanvasDrawingService:
    @classmethod
    def draw(cls, painter: QPainter, entities: List[Entity], scale: int) -> None:
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        scaling_factor = SCALE_MAPPING[scale]
        x_offset, y_offset = 0, 0
        if entities:
            x_offset, y_offset = WindowUtils.get_offset(entities)

        for entity in entities:
            coords, radius, entity_type, params = entity.coords, entity.radius, entity.entity_type, entity.params
            scaled_coords = [((x / scaling_factor) + PRESENTATION_OFFSET - (x_offset / scaling_factor),
                              (-y / scaling_factor) + PRESENTATION_OFFSET - (y_offset / scaling_factor))
                             for x, y in coords]

            if radius is not None:
                radius = radius / scaling_factor
            match entity_type:
                case Figures.LINE:
                    cls.draw_line(painter, scaled_coords)

                case Figures.CIRCLE:
                    cls.draw_circle(painter, scaled_coords, radius)

                case Figures.ARC:
                    cls.draw_arc(painter, scaled_coords, radius, params)

                case Figures.ELLIPSE:
                    cls.draw_ellipse(painter, scaled_coords, params, scaling_factor)

                case Figures.POLYLINE:
                    cls.draw_polyline(painter, scaled_coords)

                case Figures.LWPOLYLINE:
                    cls.draw_lwpolyline(painter, scaled_coords)

                case Figures.SPLINE:
                    cls.draw_spline(painter, scaled_coords)

                case _:
                    pass

    @staticmethod
    def draw_line(painter: QPainter, coords: list) -> None:
        start, end = coords
        start = WindowUtils.convert_float_to_int_list(start)
        end = WindowUtils.convert_float_to_int_list(end)
        painter.drawLine(start[0], start[1],
                         end[0], end[1])

    @staticmethod
    def draw_spline(painter: QPainter, coords: list) -> None:

        for i in range(len(coords) - 1):
            p1 = QPointF(*coords[i])
            p2 = QPointF(*coords[i + 1])
            painter.drawLine(p1, p2)

    @staticmethod
    def draw_arc(painter: QPainter, coords: list, radius: float, params: tuple) -> None:

        center = WindowUtils.convert_float_to_int_list(coords[0])
        start_angle, end_angle = params
        radius = int(radius)

        start_angle_degrees = start_angle * 16
        end_angle_degrees = end_angle * 16

        rect = QRect(center[0],
                     center[1],
                     2 * radius,
                     2 * radius)

        painter.drawArc(rect, int(start_angle_degrees), int(end_angle_degrees - start_angle_degrees),)

    @staticmethod
    def draw_circle(painter: QPainter, coords: list, radius: float) -> None:
        center = WindowUtils.convert_float_to_int_list(coords[0])
        radius = int(radius)
        rect = (
            center[0], center[1],
            radius * 2, radius * 2
        )
        painter.drawEllipse(*rect)

    @staticmethod
    def draw_point(painter: QPainter, coords: list) -> None:
        x, y = WindowUtils.convert_float_to_int_list(coords[0])
        painter.drawPoint(x, y)

    @staticmethod
    def draw_ellipse(painter: QPainter, coords: list, params, angle: float, scale: float) -> None:
        coords = WindowUtils.convert_float_to_int_list(coords[0])
        x, y = coords
        major_len, minor_len = params

        size = (major_len / scale, minor_len / scale)
        top_left = QPoint(x, y)
        transform = QTransform()
        transform.rotate(angle)
        painter.setTransform(transform)
        painter.drawEllipse(top_left, size[0], size[1])

    @staticmethod
    def draw_lwpolyline(painter: QPainter, coords: list) -> None:
        pass

    @staticmethod
    def draw_polyline(painter: QPainter, coords: list) -> None:
        coords = WindowUtils.convert_list_of_list_float_to_int(coords)

        for i in range(len(coords) - 1):
            painter.drawLine(coords[i][0], coords[i][1],
                             coords[i + 1][0], coords[i + 1][1])
