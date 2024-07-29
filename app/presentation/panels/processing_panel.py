from app.presentation.components.basic_grid import BasicGrid
from app.presentation.components.canvas import Canvas


class ProcessingPanel(BasicGrid):
    def __init__(self):
        super().__init__()
        self.canvas = Canvas()
        self.init_grid()

    def init_grid(self):
        self.frame_layout.addWidget(self.canvas)
