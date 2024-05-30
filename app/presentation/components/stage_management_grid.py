from PyQt5.QtWidgets import QPushButton, QLineEdit

from app.presentation.components.basic_grid import BasicGrid


class StageManagementGrid(BasicGrid):
    def __init__(self):
        super().__init__()

        self.intput_field = QLineEdit()
        # buttons
        self.button_start = QPushButton('Start')
        self.button_calibration = QPushButton('Calibrate')

        self.init_grid()

    def init_grid(self):
        # self.frame.setObjectName('frame-stage-management')

        self.button_calibration.setObjectName("button-stage-management")
        # button_calibration.clicked.connect(self.change_com_fun)

        self.button_start.setObjectName("button-stage-management")
        # button_start.clicked.connect(lambda: self.start_connection_fun(self.get_value()))

        self.frame_layout.addWidget(self.button_calibration)
        self.frame_layout.addWidget(self.button_start)
        self.frame_layout.addWidget(self.intput_field)

    def get_value(self) -> str:
        input_value = self.intput_field.text()
        try:
            value = str(input_value)
        except ValueError:
            value = '0'
        return value
