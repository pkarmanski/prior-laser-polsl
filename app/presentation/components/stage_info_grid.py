from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel

from app.presentation.components.basic_grid import BasicGrid


class StageInfoGrid(BasicGrid):
    def __init__(self):
        super().__init__()
        self.is_stage_moving = False
        self.stage_position = [0, 0]
        self.texts = ['Position X: {}', 'Position Y: {}', 'Stage moving: {}']
        self.label_pos_x = QLabel('Position X')
        self.label_pos_y = QLabel('Position Y')
        self.label_stage_moving = QLabel('Stage moving')
        self.init_grid()
        self.timer = None

    def init_grid(self):
        # self.frame.setObjectName("frame-stage-info")

        self.label_pos_x.setObjectName('stage-info-element')
        self.label_pos_y.setObjectName('stage-info-element')
        self.frame_layout.addWidget(self.label_pos_x)
        self.frame_layout.addWidget(self.label_pos_y)

        self.label_stage_moving.setObjectName('stage-info-element')
        self.frame_layout.addWidget(self.label_stage_moving)
        self.frame.setMinimumSize(300, 200)

    def update_stage_info(self, stage_info: list):
        self.label_pos_x.setText(self.texts[0].format(stage_info[0]))
        self.label_pos_y.setText(self.texts[1].format(stage_info[1]))
        self.label_stage_moving.setText(self.texts[2].format(stage_info[2]))

    def start_timer(self, fun):
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.update_stage_info(fun()))
        self.timer.start(1000)
