"""
Purpose of this class to communicate between service and main_panel which supposed to have
all visible components for render.
This class should not be communicating directly with stage.
"""

from app.presentation.panels.main_panel import MainPanel
from app.service.service import Service


class WindowController:
    def __init__(self):
        self.__service = Service()
        self.__main_panel = MainPanel()

    def run(self):  # method for start of the application
        pass
