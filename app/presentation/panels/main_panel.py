import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, \
    QGridLayout, QToolBar, QAction, QStatusBar, QMenuBar
from PyQt5 import QtGui, QtCore
from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap

from PyQt5.QtGui import QCursor

from app.presentation.components.menu_bar import MenuBar
from app.presentation.icons.icons import Icons
from app.presentation.window_utils.window_utils import WindowUtils


class MainWindow(QMainWindow):
    def __init__(self):
        # glowne okno
        super(MainWindow, self).__init__()
        self.menu_bar = MenuBar(self.menuBar(), self)
        self.selected_files = []
        self.customize_init()

        # grid i layout
        self.grid = QGridLayout()
        self.centerWidget = QWidget()
        self.centerWidget.setLayout(self.grid)
        self.setCentralWidget(self.centerWidget)

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

    def customize_init(self):
        self.setMinimumSize(1200, 700)
        self.setWindowTitle("Beta-Aplikacja-Lasera")
        self.setStyleSheet("background: #313338;")
        self.setWindowIcon(Icons.WINDOW_ICON.value)

        self.menu_bar.customize_init()
        self.menu_bar.add_actions()

    def add_textbox(self):
        self.add_textbox()



#w = MainWindow()
#w.show()

