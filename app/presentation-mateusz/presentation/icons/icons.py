from enum import Enum

from PyQt5.QtGui import QIcon


class Icons(Enum):
    WINDOW_ICON = "app/resources/LaserPlaceHolder.jpg"

    def __init__(self, path):
        self.__path = path

    @property
    def get_icon(self):
        return QIcon(self.__path)
