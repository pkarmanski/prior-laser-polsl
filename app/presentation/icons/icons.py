from enum import Enum

from PyQt5.QtGui import QIcon


class Icons(Enum):
    WINDOW_ICON = "app/resources/LaserPlaceHolder.jpg"
    Success = "app/resources/success.png"
    Error = "app/resources/error.png"
    Choice = "app/resources/choice.png"
    def __init__(self, path):
        self.__path = path

    @property
    def get_icon(self):
        return QIcon(self.__path)
