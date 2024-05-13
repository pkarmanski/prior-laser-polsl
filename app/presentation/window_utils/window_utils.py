from PyQt5.QtWidgets import QFileDialog
from app.presentation.components.additional_windows import Additional_Windows_Text

class WindowUtils:
    @staticmethod
    def open_file(main_window):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        dialog.setNameFilter("CAD (*.DWG *.DWF *.DXF")
        dialog_success = dialog.exec()
        main_window.selected_files = dialog.selectedFiles() if dialog_success else []

    @staticmethod
    def test(main_window):  # Fixme to jest zmodyfikowana twoja funkcja test która wcześniej była w pliku functions
        print(main_window.selected_files)

    @staticmethod # FIXME nie wiem czy to powinno byc statyczna metoda
    def text_editor(main_window):   # FIXME zastanawiam sie czy napisac to jako funkcjie czy oddzielna klase, do okna
        main_window.text = Additional_Windows_Text
        main_window.text.show()