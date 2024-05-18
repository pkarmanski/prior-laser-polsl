"""
Purpose of this class to communicate between service and main_panel which supposed to have
all visible components for render.
This class should not be communicating directly with stage.
"""
import sys

from PyQt5.QtWidgets import QApplication

from app.presentation.panels.main_panel import MainWindow
from app.service.service import Service
import threading


class WindowController:
    def __init__(self):
        self.__service = Service()
        self.__main_panel = None

    def run(self):  # method for start of the application
        pass
        app = QApplication(sys.argv)
        self.__main_panel = MainWindow()
        self.__main_panel.show()
        sys.exit(app.exec())

        # open_session_response = self.__service.open_session()
        #
        # self.__service.calibrate()
        # #
        # check_position_thread = threading.Thread(target=self.__service.check_position, daemon=True)
        #
        # check_position_thread.start()
        # self.__service.go_to_position(r'C:\Users\blach\PycharmProjects\prior-laser-polsl\test_postiotions.csv')
        # check_position_thread.join()
        # self.__service.close_session()
