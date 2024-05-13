from PyQt5.QtWidgets import QFileDialog


class WindowUtils:
    @staticmethod
    def open_file(main_window):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)  #FIXME dodać ograniczenie na pliki CAD
        dialog_success = dialog.exec()
        main_window.selected_files = dialog.selectedFiles() if dialog_success else []

    @staticmethod
    def test(main_window):  # Fixme to jest zmodyfikowana twoja funkcja test która wcześniej była w pliku functions
        print(main_window.selected_files)
