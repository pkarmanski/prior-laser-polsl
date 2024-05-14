from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, \
    QGridLayout, QToolBar, QAction, QStatusBar, QMenuBar
from PyQt5.uic.properties import QtCore

from app.presentation.components.canvas import Canvas
from app.presentation.components.menu_bar import MenuBar
from app.presentation.components.stage_info_grid import StageInfoGrid
from app.presentation.components.stage_management_grid import StageManagementGrid
from app.presentation.icons.icons import Icons


class MainWindow(QMainWindow):
    def __init__(self):

        # main window
        super(MainWindow, self).__init__()
        self.menu_bar = MenuBar(self.menuBar(), self)
        self.selected_files = []
        self.canvas = Canvas()
        self.stage_info_grid = StageInfoGrid()
        self.stage_management_grid = StageManagementGrid()

        self.customize_init()

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
        self.canvas.setAttribute(Qt.WA_StyledBackground, True)

        widget = QWidget()
        layout = QGridLayout()
        layout.addWidget(self.canvas, 0, 1)
        layout.addWidget(self.stage_info_grid, 0, 0)
        layout.addWidget(self.stage_management_grid, 1, 0)

        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.setMinimumSize(1200, 700)
        self.setWindowTitle("Beta-Aplikacja-Lasera")
        self.setWindowIcon(Icons.WINDOW_ICON.get_icon)
        self.setGeometry(100, 100, 100, 500)
        self.menu_bar.add_actions()
