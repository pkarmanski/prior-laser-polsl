import time
from typing import Callable, List, Tuple
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
from threading import Thread

from app.consts.presentation_consts import MAIN_PANEL_MIN_X, MAIN_PANEL_MIN_Y
from app.enums.service_errors import ServiceError
from app.files_processing.models import Entity
from app.presentation.components.canvas.canvas import Canvas
from app.presentation.components.com_port_grid import ComPortsGrid
from app.presentation.components.menu_bar import MenuBar
from app.presentation.components.notification import Notification
from app.presentation.components.slider import Slider
from app.presentation.components.stage_info_grid import StageInfoGrid
from app.presentation.components.stage_management_grid import StageManagementGrid
from app.presentation.enums.notification_variant import NotificationVariant
from app.presentation.icons.icons import Icons
from app.presentation.panels.processing_panel import ProcessingPanel
from app.presentation.window_utils.window_utils import WindowUtils


class MainWindow(QMainWindow):
    def __init__(self, close_event: Callable):

        # main window
        super(MainWindow, self).__init__()
        self.menu_bar = MenuBar(self.menuBar(), self)
        self.selected_files = []
        self.stage_info_grid = StageInfoGrid()
        self.stage_management_grid = StageManagementGrid()
        self.canvas: Canvas = Canvas(draw_in_canvas=self.stage_management_grid.get_from_canvas_checkbox_state)
        self.port_coms_grid = ComPortsGrid()
        self.slider = Slider()
        self.buttons_list = []
        self.customize_init()
        self.connected_items = {'prior': False, 'laser': False}
        self.close_event = close_event
        self.progress_window = ProcessingPanel()

    def customize_init(self):
        self.canvas.setAttribute(Qt.WA_StyledBackground, True)

        widget = QWidget()
        outer_layout = QHBoxLayout()
        stage_layout = QVBoxLayout()

        stage_layout.addWidget(self.stage_info_grid)
        stage_layout.addWidget(self.stage_management_grid)
        stage_layout.addWidget(self.port_coms_grid)
        stage_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        canvas_layout = QVBoxLayout()
        canvas_layout.addWidget(self.canvas)
        canvas_layout.addLayout(self.slider)

        outer_layout.addLayout(stage_layout)
        outer_layout.addLayout(canvas_layout)
        outer_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        widget.setLayout(outer_layout)
        self.setCentralWidget(widget)

        self.setMinimumSize(MAIN_PANEL_MIN_X, MAIN_PANEL_MIN_Y)
        self.setWindowTitle("LASER")
        self.setWindowIcon(Icons.WINDOW_ICON.get_icon)
        self.setGeometry(100, 100, 100, 500)
        self.menu_bar.add_actions()

        self.buttons_list = [self.stage_management_grid.button_start,
                             self.stage_management_grid.button_calibration,
                             self.port_coms_grid.button_connect_laser,
                             self.port_coms_grid.button_connect_stage]

        # disabling other buttons but connect
        self.enable_buttons(False)
        self.port_coms_grid.button_connect_laser.setEnabled(True)
        self.port_coms_grid.button_connect_stage.setEnabled(True)

    def closeEvent(self, a0):
        self.port_coms_grid.save_default_com_ports()
        self.close_event()

    def get_com_arduino(self) -> str:
        return self.port_coms_grid.get_laser_com

    def handle_calibration_result(self, calibration: Callable[[int, int], ServiceError]):
        self.enable_buttons(False)

        calibration_result = calibration(self.canvas.width(), self.canvas.height())
        time.sleep(5)
        if calibration_result == ServiceError.OK:
            self.show_notification(title="CALIBRATION",
                                   message="Calibration is finished successfully",
                                   notification_variant=NotificationVariant.Success)

            self.enable_buttons(True)
            return
        self.show_notification(title="CALIBRATION",
                               message="An error occurred during calibration",
                               informative_text=calibration_result.STAGE_CALIBRATION_ERROR.value,
                               notification_variant=NotificationVariant.Error)

    def handle_connection_laser(self, connect: Callable[[str], ServiceError]):
        response = connect(self.port_coms_grid.get_laser_com)
        if response == ServiceError.OK:
            self.connected_items['laser'] = True
            if self.connected_items['prior']:
                self.enable_buttons(True)
            self.show_notification(message="Successfully connected to the laser",
                                   notification_variant=NotificationVariant.Success)
        else:
            message = response.description
            self.show_notification(title="ERROR",
                                   message="Unable to connect to the laser",
                                   informative_text=message,
                                   notification_variant=NotificationVariant.Error)

    def handle_connection_prior(self, connect: Callable[[str], ServiceError]):
        response = connect(self.port_coms_grid.get_stage_com)

        if response == ServiceError.OK:
            self.connected_items['prior'] = True
            if self.connected_items['laser']:
                self.enable_buttons(True)
        else:
            message = response.description
            self.show_notification(title="ERROR",
                                   message="Unable to connect to the stage",
                                   informative_text=message,
                                   notification_variant=NotificationVariant.Error)

    def setup_actions(self, calibration: Callable[[int, int], ServiceError],
                      laser_write: Callable[[List[List[Tuple[int, int]]], List[Entity], bool, int], None],
                      prior_init: Callable[[str], ServiceError],
                      laser_init: Callable[[str], ServiceError],
                      stage_info: Callable[[], List],
                      draw_file_preview: Callable[[bool, str, Canvas, int], None]):

        def on_slider_value_changed(value: int):
            draw_file_preview(
                self.stage_management_grid.from_canvas_checkbox.isChecked(),
                self.stage_management_grid.get_selected_file,
                self.canvas,
                value
            )

        self.slider.print_scale_slider.valueChanged.connect(on_slider_value_changed)

        self.stage_management_grid.button_calibration.clicked.connect(
            lambda: Thread(target=self.handle_calibration_result, args=(calibration,), daemon=True).start()
        )
        self.stage_management_grid.button_start.clicked.connect(
            lambda: laser_write(self.canvas.get_points,
                                self.canvas.get_scaled_figures,
                                self.stage_management_grid.from_canvas_checkbox.isChecked(),
                                self.slider.print_scale_slider.value())
        )

        self.stage_info_grid.start_timer(stage_info)

        self.port_coms_grid.button_connect_stage.clicked.connect(
            lambda: self.handle_connection_prior(prior_init)
        )
        self.port_coms_grid.button_connect_laser.clicked.connect(
            lambda: self.handle_connection_laser(laser_init)
        )

        self.stage_management_grid.button_load_file.clicked.connect(lambda x: WindowUtils.open_file(self))

    @staticmethod
    def show_notification(title: str = "SUCCESS",
                          message: str = "",
                          informative_text: str = None,
                          notification_variant: NotificationVariant = NotificationVariant.Success,
                          timeout=3000):
        pass
        # FIXME: test and fix notifications
        # notification = Notification(notification_variant)
        # notification.notify(title, message, informative_text)

    def enable_buttons(self, enabled: bool = True):
        for button in self.buttons_list:
            button.setEnabled(enabled)

    def upload_file(self, paths: List[str]):
        for path in paths:
            self.stage_management_grid.upload_file(path)
