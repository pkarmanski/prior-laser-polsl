from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, \
    QGridLayout, QToolBar, QAction, QStatusBar, QMenuBar
from PyQt5 import QtGui, QtCore
from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap

from PyQt5.QtGui import QCursor

def OpenFile(self):
    dialog = QFileDialog()
    # dialog.setNameFilter("Wszystkie pliki")
    dialog.setFileMode(QFileDialog.FileMode.AnyFile)
    dialogSucces = dialog.exec()
    if dialogSucces:
        file_path = dialog.selectedFiles()
        print(file_path)

    else:
        print("Nie udane")
def Test(self):
    print(file_path)
