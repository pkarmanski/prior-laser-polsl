from PyQt5.QtWidgets import QPushButton, QLineEdit, QCheckBox, QHBoxLayout

from app.presentation.components.basic_grid import BasicGrid
from app.presentation.components.import_file import ImportFileView
from typing import List


class StageManagementGrid(BasicGrid):
    def __init__(self):
        super().__init__()

        # buttons
        self.button_start = QPushButton('Start')
        self.button_calibration = QPushButton('Calibrate')
        self.button_load_file = QPushButton('File')
        self.from_canvas_checkbox: QCheckBox = QCheckBox('From Canvas')
        self.list_files = ImportFileView()
        self.init_grid()

    def init_grid(self):
        load_file_layout = QHBoxLayout()
        load_file_layout.addWidget(self.button_load_file)
        load_file_layout.addWidget(self.list_files)

        self.button_calibration.setObjectName("button-stage-management")
        self.button_start.setObjectName("button-stage-management")
        self.button_load_file.setObjectName("button-stage-management")
        self.frame_layout.addLayout(load_file_layout)
        self.frame_layout.addWidget(self.button_calibration)
        self.frame_layout.addWidget(self.button_start)
        self.frame_layout.addWidget(self.from_canvas_checkbox)

    @property
    def get_selected_file(self) -> str:
        if self.list_files.selectedItems():
            return self.list_files.selectedItems()[0].text()
        return ""

    def upload_file(self, path: str):
        self.list_files.addItem(path)
        last_index = self.list_files.count() - 1
        self.list_files.setCurrentRow(last_index)

    def get_from_canvas_checkbox_state(self) -> bool:
        return self.from_canvas_checkbox.isChecked()

    # def get_value(self) -> str:
    #     input_value = self.intput_field.text()
    #     try:
    #         value = str(input_value)
    #     except ValueError:
    #         value = '0'
    #     return value
