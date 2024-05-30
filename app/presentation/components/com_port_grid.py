from PyQt5.QtWidgets import QComboBox, QLabel, QHBoxLayout, QPushButton

from app.presentation.components.basic_grid import BasicGrid
from app.stage_utils.utils import StageUtils


class ComPortsGrid(BasicGrid):
    def __init__(self):
        super().__init__()
        self.com_ports = []
        self.combo_box_laser = QComboBox()
        self.combo_box_stage = QComboBox()
        self.get_com_ports()

        # buttons:
        self.button_connect_laser = QPushButton('Connect')
        self.button_connect_stage = QPushButton('Connect')

        self.init_grid()

    def init_grid(self):
        label_laser = QLabel("Com Port Laser:")
        label_laser.setObjectName("label-information")
        self.frame_layout.addWidget(label_laser)

        self.combo_box_laser.addItems(self.com_ports)
        self.combo_box_stage.addItems(self.com_ports)

        self.button_connect_stage.setObjectName('button-connect')
        self.button_connect_laser.setObjectName('button-connect')

        self.frame_layout.addWidget(self.combo_box_laser)
        self.frame_layout.addWidget(self.button_connect_laser)
        label_stage = QLabel("Com Port Stage:")
        label_stage.setObjectName("label-information")
        self.frame_layout.addWidget(label_stage)
        self.frame_layout.addWidget(self.combo_box_stage)
        self.frame_layout.addWidget(self.button_connect_stage)

    def get_com_ports(self):
        self.com_ports = StageUtils().get_coms()

    @property
    def get_stage_com(self) -> str:
        return self.combo_box_stage.currentText()

    @property
    def get_laser_com(self) -> str:
        return self.combo_box_laser.currentText()
