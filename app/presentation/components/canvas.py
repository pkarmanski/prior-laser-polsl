import sys
from typing import List, Tuple

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPen, QPainter


class Canvas(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)
        self.setObjectName('widget-canvas')

        self.last_pos = None
        self.current_pos = None
        self.pen_color = QtGui.QColor('#000000')

        self.__lines = []
        self.__current_line = []

    def set_pen_color(self, color='#000000'):
        self.pen_color = QtGui.QColor(color)

    def paintEvent(self, event):
        painter = QPainter(self)
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
        self.__current_line = [(event.pos().x(), event.pos().y())]
        self.update()

    def mouseMoveEvent(self, event):
        self.__current_line.append((event.pos().x(), event.pos().y()))
        self.update()

    def mouseReleaseEvent(self, event):
        self.__lines.append(self.__current_line)
        self.__current_line = []
        self.update()

    @property
    def get_points(self) -> List[List[Tuple[int, int]]]:
        return self.__lines
    