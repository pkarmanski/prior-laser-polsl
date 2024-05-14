from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout


class BasicGrid(QWidget):
    def __init__(self):
        super().__init__()
        self.frame = QFrame()
        self.layout = QVBoxLayout()
        self.frame_layout = None
        self.init_grid()

    def init_grid(self):
        self.frame.setObjectName("basic-frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame_layout = QVBoxLayout(self.frame)
        self.layout.addWidget(self.frame)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
