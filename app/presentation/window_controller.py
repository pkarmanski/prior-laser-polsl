"""
Purpose of this class to communicate between service and main_panel which supposed to have
all visible components for render.
This class should not be communicating directly with stage.
"""

from app.presentation.panels.main_panel import MainPanel
from app.service.service import Service
import threading


class WindowController:
    def __init__(self):
        self.__service = Service()
        self.__main_panel = MainPanel()

    def run(self):  # method for start of the application
        open_session_response = self.__service.open_session()
        self.__service.calibrate()

        check_position_thread = threading.Thread(target=self.__service.check_position, daemon=True)

        self.__service.go_to_position('test_positions.csv')
        check_position_thread.start()
        self.__service.close_session()
