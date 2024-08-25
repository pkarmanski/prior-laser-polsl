
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QPainter, QBrush
from PyQt5.QtWidgets import QMainWindow

from app.presentation.components.canvas.basic_canvas import BasicCanvas
from app.consts.presentation_consts import (
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
)


class Canvas(BasicCanvas):
    def __init__(self, draw_in_canvas: callable):
        super().__init__()

        self.last_pos = None
        self.current_pos = None

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
            self.paint_not_from_canvas(painter)

    def paint_not_from_canvas(self, painter: QPainter):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)

        center_x = CANVAS_WIDTH // 2
        center_y = CANVAS_HEIGHT // 2
        for line in self.lines_preview:
            x1, x2, y1, y2 = line

            centered_line = (
                x1 + center_x, y1 + center_y,
                x2 + center_x, y2 + center_y
            )
            painter.drawLine(*centered_line)
        for circle in self.circles_preview:
            x, y, width, height = circle
            centered_circle = (
                x + center_x - width // 2,
                y + center_y - height // 2,
                width, height
            )
            painter.drawEllipse(*centered_circle)

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

    def paint_start(self):
        painter = QPainter(self)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(0, 0, 200, 200)
        self.update()

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
