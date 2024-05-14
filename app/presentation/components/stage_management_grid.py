from PyQt5.QtWidgets import QPushButton, QLineEdit

from app.presentation.components.basic_grid import BasicGrid


class StageManagementGrid(BasicGrid):
    def __init__(self, fun_com, fun_start):
        super().__init__()
        self.change_com_fun = fun_com
        self.start_connection_fun = fun_start
        self.intput_field = QLineEdit()
        self.init_grid()

    def init_grid(self):
        # self.frame.setObjectName('frame-stage-management')

        button_calibration = QPushButton('Calibrate')
        button_calibration.setObjectName("button-stage-management")
        button_calibration.clicked.connect(self.change_com_fun)

        button_start = QPushButton('Start')
        button_start.setObjectName("button-stage-management")
        button_start.clicked.connect(lambda: self.start_connection_fun(self.get_value()))

        self.frame_layout.addWidget(button_calibration)
        self.frame_layout.addWidget(button_start)
        self.frame_layout.addWidget(self.intput_field)

    def get_value(self) -> int:
        input_value = self.intput_field.text()
        try:
            value = int(input_value)
        except ValueError:
            value = 0
        return value
