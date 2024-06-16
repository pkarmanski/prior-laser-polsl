from PyQt5.QtWidgets import QComboBox, QLabel, QHBoxLayout, QPushButton
from app.stage_utils.yaml_manager import YamlData

from app.presentation.components.basic_grid import BasicGrid
from app.stage_utils.utils import StageUtils


class ComPortsGrid(BasicGrid):
    def __init__(self):
        super().__init__()
        self.com_ports = []
        self.combo_box_laser = QComboBox()
        self.combo_box_stage = QComboBox()
        self.__yaml_manager = YamlData()
        self.get_com_ports()

        # buttons:
        self.button_connect_laser = QPushButton('Connect')
        self.button_connect_stage = QPushButton('Connect')

        self.init_grid()

    def init_grid(self):
        label_laser = QLabel("Com Port Laser:")
        label_laser.setObjectName("label-information")
        self.frame_layout.addWidget(label_laser)

        self.button_connect_stage.setObjectName('button-connect')
        self.button_connect_laser.setObjectName('button-connect')

        self.frame_layout.addWidget(self.combo_box_laser)
        self.frame_layout.addWidget(self.button_connect_laser)
        label_stage = QLabel("Com Port Stage:")
        label_stage.setObjectName("label-information")
        self.frame_layout.addWidget(label_stage)
        self.frame_layout.addWidget(self.combo_box_stage)
        self.frame_layout.addWidget(self.button_connect_stage)

    def update_com_ports(self):
        self.com_ports = StageUtils.get_coms()
        self.combo_box_laser.clear()
        self.combo_box_stage.clear()
        self.combo_box_stage.addItems(self.com_ports)
        self.combo_box_laser.addItems(self.com_ports)

    def get_com_ports(self):
        self.com_ports = StageUtils().get_coms()
        self.combo_box_laser.addItems(self.com_ports)
        self.combo_box_stage.addItems(self.com_ports)

        default_com_ports = self.__yaml_manager.get_default_com_ports()
        try:
            default_laser = self.com_ports.index(default_com_ports["laser"])
            default_stage = self.com_ports.index(default_com_ports["stage"])

            self.combo_box_stage.setCurrentText(default_stage)
            self.combo_box_laser.setCurrentText(default_laser)
        except ValueError:
            pass

    def save_default_com_ports(self):
        if len(self.combo_box_stage.currentText()) and len(self.combo_box_laser.currentText()):
            self.__yaml_manager.save_data(
                stage_port=self.combo_box_stage.currentText(),
                laser_port=self.combo_box_laser.currentText(),
            )

    @property
    def get_stage_com(self) -> str:
        return self.combo_box_stage.currentText()

    @property
    def get_laser_com(self) -> str:
        return self.combo_box_laser.currentText()
