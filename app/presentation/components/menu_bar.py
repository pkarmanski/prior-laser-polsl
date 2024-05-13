from PyQt5.QtWidgets import QMenuBar, QAction

from app.presentation.window_utils.window_utils import WindowUtils


class MenuBar:
    def __init__(self, q_menu_bar: QMenuBar, main_window):
        self.menu_bar = q_menu_bar
        self.file_menu = self.menu_bar.addMenu("&File")

        # actions
        self.action_file_selection = QAction("  Plik  ", main_window)
        self.action_notes = QAction(" Notatki ", main_window)

    def customize_init(self):

        # Fixme !!! to chyba nie działa bo
        # Fixme !!! jak wchodzisz dośrodka funcki setStyleSheet to tam jest po prostu pass XD
        self.menu_bar.setStyleSheet(
            "{border: 1px solid '#64646c';" +
            "border-radius: 2px;" +
            "background: #24242C;" +
            "font-size: 12px;" +
            "color: 'WHITE';}"
            ":hover{background: #323844;}")

        self.file_menu.setStyleSheet(
            "{border: 1px solid '#64646c';" +
            "border-radius: 2px;" +
            "background: #24242C;" +
            "font-size: 12px;" +
            "color: 'WHITE';}"
            ":hover{background: #323844;}")

    def add_actions(self):

        self.action_file_selection.triggered.connect(lambda x: WindowUtils.open_file(self))
        self.action_notes.triggered.connect(lambda x: WindowUtils.test(self))
        self.file_menu.addAction(self.action_file_selection)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.action_notes)
