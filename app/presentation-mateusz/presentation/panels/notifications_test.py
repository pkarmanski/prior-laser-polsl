import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, \
    QGridLayout, QToolBar, QAction, QStatusBar, QMenuBar, QMessageBox
from PyQt5 import QtGui, QtCore
from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap

from PyQt5.QtGui import QCursor

SELECTED_FILE_PATH = []


class MainWindow(QMainWindow):
    def __init__(self):
        # glowne okno
        super(MainWindow, self).__init__()
        self.setMinimumSize(1200, 700)
        self.setWindowTitle("Beta-Aplikacja-Lasera")
        self.setStyleSheet("background: #313338;")
        self.setWindowIcon(QIcon("LaserPlaceHolder.jpg"))
        # akcje
        act1 = QAction("  Plik  ", self)
        act1.triggered.connect(self.OpenFile)
        act2 = QAction(" Notatki ", self)

        # menubar
        menu = self.menuBar()
        menu.setStyleSheet(
            "{border: 1px solid '#64646c';" +
            "border-radius: 2px;" +
            "background: #24242C;" +
            "font-size: 12px;" +
            "color: 'white';}"
            ":hover{background: #323844;}"
        )
        file_menu = menu.addMenu("&File")
        file_menu.addAction(act1)
        file_menu.addSeparator()
        file_menu.addAction(act2)
        file_menu.setStyleSheet("{border: 1px solid '#64646c';" +
                                "border-radius: 2px;" +
                                "background: #24242C;" +
                                "font-size: 12px;" +
                                "color: 'white';}"
                                ":hover{background: #323844;}"
                                )

        grid = QGridLayout()
        centerWidget = QWidget()
        centerWidget.setLayout(grid)
        self.setCentralWidget(centerWidget)

    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Ok?")
        msg.setText("This is bad")
        x = msg.exec_()

    def OpenFile(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        dialogSucces = dialog.exec()
        if dialogSucces:
            SELECTED_FILE_PATH = dialog.selectedFiles()
            print(SELECTED_FILE_PATH)
        else:
            self.show_popup()
            print("Nie udane")


app = QApplication(sys.argv)

#

w = MainWindow()
w.show()
sys.exit(app.exec())
