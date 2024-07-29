from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QApplication

from app.presentation.components.canvas import Canvas


class ProcessingPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.canvas = Canvas()
        self.init_grid()
        self.setup_window()
        self.setObjectName('processing-panel')

    def init_grid(self):
        self.canvas.setAttribute(Qt.WA_StyledBackground, True)
        layout = QHBoxLayout()
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def setup_window(self):
        self.setWindowTitle("Progress")

        self.setMinimumSize(1200, 700)

        self.resize(1200, 700)

        screen = QApplication.primaryScreen().availableGeometry()
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)
