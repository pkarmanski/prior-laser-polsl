from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton


class NotificationWindow(QWidget):
    def __init__(self, message, timeout=3000):
        super().__init__()
        self.setWindowTitle('Notification')
        self.setGeometry(100, 100, 300, 100)
        layout = QVBoxLayout()

        self.label = QLabel(message)
        layout.addWidget(self.label)

        self.close_button = QPushButton('Close')
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def show_notification(self):
        self.show()



