from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QIcon


# class Notification(QWidget):
#     def __init__(self, message, timeout=3000):
#         super().__init__()
#         self.setWindowTitle('Notification')
#         self.setGeometry(100, 100, 300, 100)
#         layout = QVBoxLayout()
#
#         self.label = QLabel(message)
#         layout.addWidget(self.label)
#
#         self.close_button = QPushButton('Close')
#         self.close_button.clicked.connect(self.close)
#         layout.addWidget(self.close_button)
#
#         self.setLayout(layout)
#
#     def show_notification(self):
#         self.show()
#
class Message(QWidget):
    def __init__(self, title, message, parent=None):
        QWidget.__init__(self, parent)
        self.setLayout(QGridLayout())
        self.titleLabel = QLabel(title, self)
        self.titleLabel.setStyleSheet("font-size: 18px; font-weight: bold; padding: 0;")
        self.messageLabel = QLabel(message, self)
        self.messageLabel.setStyleSheet("font-size: 12px; font-weight: normal; padding: 0;")
        self.buttonClose = QPushButton(self)
        self.buttonClose.setIcon(QIcon.fromTheme("window-close"))
        self.buttonClose.setFlat(True)
        self.buttonClose.setFixedSize(32, 32)
        self.buttonClose.setIconSize(QSize(16, 16))
        self.layout().addWidget(self.titleLabel)
        self.layout().addWidget(self.messageLabel, 2, 0)
        self.layout().addWidget(self.buttonClose, 0, 1)


class Notification(QWidget):
    def __init__(self, parent = None):
        super(QWidget, self).__init__(parent = None)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background: #d3d7cf; padding: 0;")
        self.mainLayout = QVBoxLayout(self)
        self.m = None

    def notify(self, title, message, timeout):
        self.m = Message(title, message)
        self.mainLayout.addWidget(self.m)
        self.m.buttonClose.clicked.connect(self.clicked)
        self.show()
        QTimer.singleShot(timeout, 0, self.close_self)

    def close_self(self):
        self.close()
        self.m.close()

    def clicked(self):
        self.close()
