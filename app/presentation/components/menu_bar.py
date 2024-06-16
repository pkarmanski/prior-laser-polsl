from PyQt5.QtWidgets import QMenuBar, QAction
from app.stage_utils.utils import StageUtils
from app.presentation.window_utils.window_utils import WindowUtils


class MenuBar:
    def __init__(self, q_menu_bar: QMenuBar, main_window):
        self.menu_bar = q_menu_bar
        self.file_menu = self.menu_bar.addMenu("&File")
        self.parent = main_window

        # actions
        self.action_file_selection = QAction("  File  ", main_window)
        self.action_refresh = QAction(" Update COMs ", main_window)

    def add_actions(self):
        self.action_file_selection.triggered.connect(lambda x: WindowUtils.open_file(self.parent))
        self.action_refresh.triggered.connect(self.parent.port_coms_grid.update_com_ports)
        self.file_menu.addAction(self.action_file_selection)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.action_refresh)
