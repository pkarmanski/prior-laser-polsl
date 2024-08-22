from typing import Callable, List, Tuple
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QSlider, QLabel
from threading import Thread
from app.enums.service_errors import ServiceError
from app.presentation.components.canvas.canvas import Canvas
from app.presentation.components.com_port_grid import ComPortsGrid
from app.presentation.components.menu_bar import MenuBar
from app.presentation.components.notification import Notification
from app.presentation.components.stage_info_grid import StageInfoGrid
from app.presentation.components.stage_management_grid import StageManagementGrid
from app.presentation.enums.notification_variant import NotificationVariant
from app.presentation.icons.icons import Icons
from app.presentation.panels.processing_panel import ProcessingPanel
from app.files_processing.file_reading import DXFReader
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
        self.print_scale_slider: QSlider = QSlider(Qt.Horizontal)
        self.print_scale_slider_label: QLabel = QLabel("Scale 1")
        self.port_coms_grid = ComPortsGrid()

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


        #TODO spiąć to w jedną klaskę od skali
        self.print_scale_slider.setMinimum(1) #TODO może pobierać to z configa?
        self.print_scale_slider.setMaximum(5)
        self.print_scale_slider.setTickPosition(QSlider.TicksBelow)
        self.print_scale_slider.setTickInterval(1)

        self.print_scale_slider_label.setObjectName('scale-info-element')

        canvas_layout = QVBoxLayout()
        # scale_range_label_layout = QHBoxLayout()
        # scale_range_label_layout.setObjectName("scale-info-element-number-layout")
        # for i in range(1, 6):
        #     scale_number_label = QLabel(str(i))
        #     scale_number_label.setObjectName("scale-info-element-number")
        #     scale_range_label_layout.addWidget(scale_number_label)
        canvas_layout.addWidget(self.canvas)
        canvas_layout.addWidget(self.print_scale_slider_label)
        canvas_layout.addWidget(self.print_scale_slider)
        # canvas_layout.addLayout(scale_range_label_layout)




        outer_layout.addLayout(stage_layout)
        outer_layout.addLayout(canvas_layout)
        outer_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        widget.setLayout(outer_layout)
        self.setCentralWidget(widget)

        self.setMinimumSize(1200, 700)
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
        if calibration_result == ServiceError.OK:
            self.show_notification(title="CALIBRATION",
                                   message="Calibration is finished successfully",
                                   notification_variant=NotificationVariant.Success)

            self.enable_buttons(True)
        self.show_notification(title="CALIBRATION",
                               message="An error occurred during calibration",
                               informative_text=calibration_result.STAGE_CALIBRATION_ERROR.value,
                               notification_variant=NotificationVariant.Error)

    def update_print_scale_label(self, value):
        self.print_scale_slider_label.setText(f"Scale: {value}")


    # TODO: add laser Errors
    def handle_connection_laser(self, ):
        # self.progress_window.show()
        dxf = DXFReader(self.stage_management_grid.get_selected_file)
        figures = dxf.get_figures()
        self.canvas.update_figures(figures)
        # response = connect(self.port_coms_grid.get_laser_com)
        # if response == ServiceError.OK:
        #     self.connected_items['laser'] = True
        #     if self.connected_items['prior']:
        #         self.enable_buttons(True)
        #     self.show_notification(message="Successfully connected to the laser",
        #                            notification_variant=NotificationVariant.Success)
        # else:
        #     message = response.description
        #     self.show_notification(title="ERROR",
        #                            message="Unable to connect to the laser",
        #                            informative_text=message,
        #                            notification_variant=NotificationVariant.Error)

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
                      laser_write: Callable[[List[List[Tuple[int, int]]], str, bool, int], None],
                      prior_init: Callable[[str], ServiceError],
                      laser_init: Callable[[str], ServiceError],
                      stage_info: Callable[[], List],
                      draw_file_preview: Callable[[bool, str, Canvas, int], None]):

        self.stage_management_grid.button_calibration.clicked.connect(
            lambda: Thread(target=self.handle_calibration_result, args=(calibration,), daemon=True).start()
        )
        self.stage_management_grid.button_start.clicked.connect(
            lambda: laser_write(self.canvas.get_points,
                                self.stage_management_grid.get_selected_file,
                                self.stage_management_grid.from_canvas_checkbox.isChecked(),
                                self.print_scale_slider.value())
        )
        self.port_coms_grid.button_connect_stage.clicked.connect(
            lambda: self.handle_connection_prior(prior_init)
        )

        def on_slider_value_changed(value: int):
            self.update_print_scale_label(value)
            draw_file_preview(
                self.stage_management_grid.from_canvas_checkbox.isChecked(),
                self.stage_management_grid.get_selected_file,
                self.canvas,
                value
            )

        self.print_scale_slider.valueChanged.connect(on_slider_value_changed)



        # self.port_coms_grid.button_connect_laser.clicked.connect(
        #     lambda: self.handle_connection_laser()
        # )
        self.stage_info_grid.start_timer(stage_info) # TODO think later about how to run it in different thread

        self.port_coms_grid.button_connect_laser.clicked.connect(
            lambda: draw_file_preview(self.stage_management_grid.from_canvas_checkbox.isChecked(),
                                      self.stage_management_grid.get_selected_file,
                                      self.canvas,
                                      self.print_scale_slider.value())
        )

        self.stage_management_grid.button_load_file.clicked.connect(lambda x: WindowUtils.open_file(self))

    @staticmethod
    def show_notification(title: str = "SUCCESS",
                          message: str = "",
                          informative_text: str = None,
                          notification_variant: NotificationVariant = NotificationVariant.Success,
                          timeout=3000):
        notification = Notification(notification_variant)
        notification.notify(title, message, informative_text)

    def enable_buttons(self, enabled: bool = True):
        for button in self.buttons_list:
            button.setEnabled(enabled)

    def upload_file(self, paths: List[str]):
        for path in paths:
            self.stage_management_grid.upload_file(path)
