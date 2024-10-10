from typing import List
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QPainter
from app.files_processing.models import Entity
from app.presentation.components.canvas.basic_canvas import BasicCanvas
from app.presentation.services.canvas_drawing import CanvasDrawingService


class Canvas(BasicCanvas):
    def __init__(self, draw_in_canvas: callable):
        super().__init__()

        self.last_pos = None
        self.current_pos = None

        self.__scale = 1
        self.__lines = []
        self.__current_line = []
        self.__figures = []
        self.lines_preview = []
        self.circles_preview = []
        self.draw_in_canvas = draw_in_canvas
        self.update()

    @property
    def paint_in_canvas(self) -> bool:
        return self.__parent.from_canvas_button_state

    def paintEvent(self, event):
        painter = QPainter(self)
        super().draw_grid(painter)

        if self.draw_in_canvas():
            self.paint_from_canvas(painter)
        else:
            self.clearMask()
            CanvasDrawingService().draw(
                painter=painter, entities=self.__figures, scale=self.__scale
            )

    def paint_from_canvas(self, painter: QPainter):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        for point in range(len(self.__current_line) - 1):
            painter.drawLine(self.__current_line[point][0], self.__current_line[point][1],
                             self.__current_line[point + 1][0], self.__current_line[point + 1][1])
        for line in self.__lines:
            for point in range(len(line) - 1):
                painter.drawLine(line[point][0], line[point][1],
                                 line[point + 1][0], line[point + 1][1])

    def mousePressEvent(self, event):
        if self.draw_in_canvas():
            self.__current_line = [(event.pos().x(), event.pos().y())]
        self.update()

    def mouseMoveEvent(self, event):
        if self.draw_in_canvas():
            self.__current_line.append((event.pos().x(), event.pos().y()))
        self.update()

    def mouseReleaseEvent(self, event):
        if self.draw_in_canvas():
            self.__lines.append(self.__current_line)
            self.__current_line = []
            self.update()

    def update_figures(self, figures: list):
        self.__figures = figures

    def clear_canvas(self):
        self.__lines = []
        self.__current_line = []
        self.__figures = []
        self.lines_preview = []
        self.circles_preview = []
        self.update()

    def update_scale(self, scale: int) -> None:
        self.__scale = scale

    @property
    def get_scaled_figures(self) -> List[Entity]:
        return CanvasDrawingService().get_scaled_figures(self.__figures, self.__scale)
