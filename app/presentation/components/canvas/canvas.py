
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QPainter

from app.presentation.components.canvas.basic_canvas import BasicCanvas


class Canvas(BasicCanvas):
    def __init__(self):
        super().__init__()

        self.last_pos = None
        self.current_pos = None

        self.__lines = []
        self.__current_line = []

    def paintEvent(self, event):
        painter = QPainter(self)
        super().draw_grid(painter)

        self.paint_from_canvas(painter)

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
        self.__current_line = [(event.pos().x(), event.pos().y())]
        self.update()

    def mouseMoveEvent(self, event):
        self.__current_line.append((event.pos().x(), event.pos().y()))
        self.update()

    def mouseReleaseEvent(self, event):
        self.__lines.append(self.__current_line)
        self.__current_line = []
        self.update()
    