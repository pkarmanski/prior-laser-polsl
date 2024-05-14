from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from app.presentation.components.basic_grid import BasicGrid


class StageInfoGrid(BasicGrid):
    def __init__(self):
        super().__init__()
        self.is_stage_moving = False
        self.stage_position = [0, 0]
        self.init_stage_grid()

    def init_stage_grid(self):
        # self.frame.setObjectName("frame-stage-info")

        position_x = QLabel(f'Position X: {self.stage_position[0]}')
        position_x.setObjectName('stage-info-element')
        position_y = QLabel(f'Position Y: {self.stage_position[1]}')
        position_y.setObjectName('stage-info-element')
        self.frame_layout.addWidget(position_x)
        self.frame_layout.addWidget(position_y)

        stage_moving = QLabel(f'Stage moving: {self.is_stage_moving}')
        stage_moving.setObjectName('stage-info-element')
        self.frame_layout.addWidget(stage_moving)
        self.frame.setMinimumSize(300, 200)
