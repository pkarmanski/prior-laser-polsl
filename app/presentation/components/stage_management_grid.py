from PyQt5.QtWidgets import QPushButton

from app.presentation.components.basic_grid import BasicGrid


class StageManagementGrid(BasicGrid):
    def __init__(self):
        super().__init__()
        self.init_management_grid()

    def init_management_grid(self):
        # self.frame.setObjectName('frame-stage-management')

        button_calibration = QPushButton('Calibrate')
        button_calibration.setObjectName("button-stage-management")
        button_start = QPushButton('Start')
        button_start.setObjectName("button-stage-management")

        self.frame_layout.addWidget(button_calibration)
        self.frame_layout.addWidget(button_start)
