from typing import List, Tuple

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPen, QPainter

from app.consts.presentation_consts import (
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
    CANVAS_PEN_COLOR,
    GRAY_COLOR,
    GRID_WIDTH,
    GRID_STEP,
)


class BasicCanvas(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(CANVAS_WIDTH, CANVAS_HEIGHT)
        self.setObjectName("widget-canvas")
        self.penColor = QtGui.QColor(CANVAS_PEN_COLOR)

        self.__lines = []

    def set_pen_color(self, color: str = CANVAS_PEN_COLOR):
        self.penColor = QtGui.QColor(color)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_grid(painter)
        pass

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass

    @staticmethod
    def draw_grid(painter: QPainter):
        grid_color = QtGui.QColor(GRAY_COLOR)
        pen = QPen(grid_color)
        pen.setWidthF(GRID_WIDTH)
        painter.setPen(pen)

        step = GRID_STEP
        for x in range(0, CANVAS_WIDTH, step):
            painter.drawLine(x, 0, x, CANVAS_HEIGHT)

        for y in range(0, CANVAS_HEIGHT, step):
            painter.drawRect(0, y, CANVAS_WIDTH, CANVAS_HEIGHT)

    @property
    def get_points(self) -> List[Tuple[float, float]]:
        return self.__lines
