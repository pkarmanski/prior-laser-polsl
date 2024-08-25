import math
from typing import List

from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPen

from app.files_processing.enums import Figures
from app.presentation.components.canvas.canvas import Canvas
from app.presentation.window_utils.window_utils import WindowUtils


class CanvasDrawingService:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas

    def draw(self, entities, scale: int):
        painter = QPainter(self.canvas)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        for entity in entities:
            coords, radius, entity_type, params = entity.coords, entity.radius, entity.entity_type, entity.params

            scaled_coords = [(x * scale, y * scale) for x, y in coords]

            if radius is not None:
                scaled_radius = radius * scale

            match entity_type:
                case Figures.LINE:
                    self.draw_line(painter, scaled_coords)

                case Figures.CIRCLE:
                    self.draw_circle(painter, scaled_coords, scaled_radius)

                case Figures.ARC:
                    self.draw_arc(painter, scaled_coords, scaled_radius)

                case _:
                    pass
        self.canvas.update()

    def draw_line(self, painter: QPainter, coords: list) -> None:
        start, end = coords
        start = WindowUtils.convert_float_to_int_list(start)
        end = WindowUtils.convert_float_to_int_list(end)

        painter.drawLine(start[0], start[1],
                         end[0], end[1])

        self.canvas.lines_preview.append((start[0], start[1], end[0], end[1]))

    def draw_arc(self, painter: QPainter, coords: list, radius: float) -> None:
        start_point, center, end_point = coords
        start_point = WindowUtils.convert_float_to_int_list(start_point)
        end_point = WindowUtils.convert_float_to_int_list(end_point)
        center = WindowUtils.convert_float_to_int_list(center)

        radius = int(radius)
        rect = (
            center[0] - radius, center[1] - radius,
            radius * 2, radius * 2
        )
        start_angle = math.degrees(math.atan2(start_point[1] - center[1], start_point[0] - center[0]))
        end_angle = math.degrees(math.atan2(end_point[1] - center[1], end_point[0] - center[0]))
        span_angle = end_angle - start_angle
        painter.drawArc(*rect, int(start_angle * 16), int(span_angle * 16))

    def draw_circle(self, painter: QPainter, coords: list, radius: float) -> None:
        center = WindowUtils.convert_float_to_int_list(coords[0])
        radius = int(radius/100)
        rect = (
            center[0], center[1],
            radius * 2, radius * 2
        )
        self.canvas.circles_preview.append(rect)
        painter.drawEllipse(*rect)
