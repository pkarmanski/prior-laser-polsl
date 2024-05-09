import sys
from Functions import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, \
    QGridLayout, QToolBar, QAction, QStatusBar, QMenuBar
from PyQt5 import QtGui, QtCore
from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap

from PyQt5.QtGui import QCursor


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
        act1.triggered.connect(OpenFile)
        act2 = QAction(" Notatki ", self)
        act2.triggered.connect(Test)

        # menubar
        menu = self.menuBar()
        menu.setStyleSheet(
            "{border: 1px solid '#64646c';" +
            "border-radius: 2px;" +
            "background: #24242C;" +
            "font-size: 12px;" +
            "color: 'WHITE';}"
            ":hover{background: #323844;}")
        file_menu = menu.addMenu("&File")
        file_menu.addAction(act1)
        file_menu.addSeparator()
        file_menu.addAction(act2)
        file_menu.setStyleSheet("{border: 1px solid '#64646c';" +
            "border-radius: 2px;" +
            "background: #24242C;" +
            "font-size: 12px;" +
            "color: 'WHITE';}"
            ":hover{background: #323844;}")

        # grid i layout
        grid = QGridLayout()
        centerWidget = QWidget()
        centerWidget.setLayout(grid)
        self.setCentralWidget(centerWidget)

        # #toolbar
        # toolbar = QToolBar()
        # toolbar.setMovable(False)
        # toolbar.setStyleSheet(
        #     "{border: 1px solid '#64646c';" +
        #     "border-radius: 2px;"
        #     "background: #24242C;" +
        #     "font-size: 11px;" +
        #     "color: 'white';}"
        #     ":hover{background: #323844;}"
        # )
        # self.addToolBar(toolbar)
        # toolbar.addAction(act1)
        # toolbar.addAction(act2)


app = QApplication(sys.argv)

w = MainWindow()
w.show()
sys.exit(app.exec())