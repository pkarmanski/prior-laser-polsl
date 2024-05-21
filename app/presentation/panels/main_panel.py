from typing import Callable, List, Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout

from app.enums.service_errors import ServiceError
from app.presentation.components.canvas import Canvas
from app.presentation.components.com_port_grid import ComPortsGrid
from app.presentation.components.menu_bar import MenuBar
from app.presentation.components.notification import NotificationWindow
from app.presentation.components.stage_info_grid import StageInfoGrid
from app.presentation.components.stage_management_grid import StageManagementGrid
from app.presentation.enums.notification_variant import NotificationVariant
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
        self.port_coms_grid = ComPortsGrid()

        self.customize_init()
        self.buttons_list = []

    def customize_init(self):
        self.canvas.setAttribute(Qt.WA_StyledBackground, True)

        widget = QWidget()
        outer_layout = QHBoxLayout()
        stage_layout = QVBoxLayout()

        stage_layout.addWidget(self.stage_info_grid)
        stage_layout.addWidget(self.stage_management_grid)
        stage_layout.addWidget(self.port_coms_grid)
        stage_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        outer_layout.addLayout(stage_layout)
        outer_layout.addWidget(self.canvas)
        outer_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        widget.setLayout(outer_layout)
        self.setCentralWidget(widget)

        self.setMinimumSize(1200, 700)
        self.setWindowTitle("Beta-Aplikacja-Lasera")
        self.setWindowIcon(Icons.WINDOW_ICON.get_icon)
        self.setGeometry(100, 100, 100, 500)
        self.menu_bar.add_actions()

        self.buttons_list = [self.stage_management_grid.button_start,
                             self.stage_management_grid.button_calibration,
                             self.port_coms_grid.button_connect_laser,
                             self.port_coms_grid.button_connect_stage]

    def get_com_arduino(self) -> str:
        return self.port_coms_grid.get_laser_com

    def handle_calibration_result(self, calibration: Callable[[int, int], ServiceError]):
        self.enable_buttons(False)

        calibration_result = calibration(self.canvas.width(), self.canvas.height())
        notification_variant = NotificationVariant.Error
        message = "ERROR"
        if calibration_result == ServiceError.OK:
            notification_variant = NotificationVariant.Success
            message = "SUCCESS"
        self.show_notification(message, notification_variant)

        self.enable_buttons(True)

    def setup_button_actions(self,
                             calibration: Callable[[int, int], ServiceError],
                             laser_write: Callable[[List[List[Tuple[int, int]]]], None],
                             prior_init: Callable[[str], ServiceError],
                             laser_init: Callable[[str], None]):

        self.stage_management_grid.button_calibration.clicked.connect(
            lambda: self.handle_calibration_result(calibration)
        )
        self.stage_management_grid.button_start.clicked.connect(
            lambda: laser_write(self.canvas.get_points)
        )
        self.port_coms_grid.button_connect_stage.clicked.connect(
            lambda: prior_init(self.port_coms_grid.get_stage_com)
        )
        self.port_coms_grid.button_connect_laser.clicked.connect(
            lambda: laser_init(self.port_coms_grid.get_laser_com)
        )

    def show_notification(self, message: str, notification_variant: NotificationVariant, timeout=3000):
        notification = NotificationWindow(message, timeout)
        notification.setObjectName(notification_variant.object_name)
        notification.show_notification()

    def enable_buttons(self, enabled: bool = True):
        for button in self.buttons_list:
            button.setEnabled(enabled)
