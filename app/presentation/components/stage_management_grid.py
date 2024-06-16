from PyQt5.QtWidgets import QPushButton, QLineEdit, QCheckBox

from app.presentation.components.basic_grid import BasicGrid
from app.presentation.components.import_file import ImportFileView
from typing import List

class StageManagementGrid(BasicGrid):
    def __init__(self):
        super().__init__()

        # buttons
        self.button_start = QPushButton('Start')
        self.button_calibration = QPushButton('Calibrate')
        self.check_box = QCheckBox('From Canvas')
        self.list_files = ImportFileView()
        self.init_grid()

    def init_grid(self):

        self.button_calibration.setObjectName("button-stage-management")

        self.button_start.setObjectName("button-stage-management")
        self.frame_layout.addWidget(self.list_files)
        self.frame_layout.addWidget(self.button_calibration)
        self.frame_layout.addWidget(self.button_start)
        self.frame_layout.addWidget(self.check_box)

    @property
    def get_selected_file(self):
        try:
            return self.list_files.selectedItems()[0].text()
        except IndexError:
            pass

    def upload_file(self, path: str):
        self.list_files.addItem(path)

    # def get_value(self) -> str:
    #     input_value = self.intput_field.text()
    #     try:
    #         value = str(input_value)
    #     except ValueError:
    #         value = '0'
    #     return value
