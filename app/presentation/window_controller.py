"""
Purpose of this class to communicate between service and main_panel which supposed to have
all visible components for render.
This class should not be communicating directly with stage.
"""
import sys
from typing import Union

from PyQt5.QtWidgets import QApplication

from app.presentation.panels.main_panel import MainWindow
from app.service.service import Service


class WindowController:
    def __init__(self):
        self.__service = Service()
        self.__main_panel: Union[MainWindow, None] = None
        self.app = QApplication(sys.argv)
        self.style_panel()

    def set_laser_com_port(self):
        self.__service.init_laser(self.__main_panel.get_com_arduino())

    def write_laser(self, value: str):
        self.__service.laser_write(value)

    def run(self):  # method for start of the application
        self.__main_panel = MainWindow()
        self.__main_panel.setup_button_actions(self.__service.calibrate,
                                               self.__service.print_lines,
                                               self.__service.init_prior,
                                               self.__service.init_laser,
                                               self.__service.get_stage_info)
        self.__main_panel.show()
        self.app.exec_()

    def style_panel(self):
        with open('app/presentation/styling/main.css', 'r') as f:
            style = f.read()
            self.app.setStyleSheet(style)

