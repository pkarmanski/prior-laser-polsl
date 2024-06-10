from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QTimer


class Notification(QWidget):
    def __init__(self):
        super(QWidget, self).__init__(parent=None)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background: #d3d7cf; padding: 0;")
        self.mainLayout = QVBoxLayout(self)

    def notify(self, title: str, message: str):
        message_box = QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setText(message)

    def close_self(self):
        self.close()
        self.m.close()

    def clicked(self):
        self.close()
