from typing import Union

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from app.presentation.enums.notification_variant import NotificationVariant


class Notification(QWidget):
    def __init__(self, variant: NotificationVariant):
        super(QWidget, self).__init__(parent=None)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background: #d3d7cf; padding: 0;")
        self.message_box = QMessageBox()
        self.message_box.setWindowFlags(Qt.FramelessWindowHint)
        self.customize(variant)

    def customize(self, variant: NotificationVariant):
        self.message_box.setObjectName(variant.object_name)

    def notify(self, title: str, message: str, informative_text: Union[str, None] = None):
        self.message_box.setWindowTitle(title)
        if informative_text is not None:
            self.message_box.setInformativeText(informative_text)
        self.message_box.setText(message)
        self.message_box.setDefaultButton(QMessageBox.Ok)
        self.message_box.exec_()

    def close_self(self):
        self.close()
        self.m.close()

    def clicked(self):
        self.close()
