from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, \
    QGridLayout, QToolBar, QAction, QStatusBar, QMenuBar
from PyQt5 import QtGui, QtCore
from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
import sys
from PyQt5.QtGui import QCursor

class MainWindow(QMainWindow):
    def init(self):
        # glowne okno
        super(MainWindow, self).__init__()
        self.setMinimumSize(1200, 700)
        self.setWindowTitle("Beta-Aplikacja-Lasera")
        self.setStyleSheet("background: #313338;")
        self.setWindowIcon(QIcon("LaserPlaceHolder.jpg"))
        # akcje
        act1 = QAction("  Plik  ", self)
        act1.triggered.connect(self.OpenFile)
        act2 = QAction(" Notatki ", self)

        # menubar
        menu = self.menuBar()
        menu.setStyleSheet(
            "{border: 1px solid '#64646c';" +
            "border-radius: 2px;" +
            "background: #24242C;" +
            "font-size: 12px;" +
            "color: 'white';}"
        )
        file_menu = menu.addMenu("&File")
        file_menu.addAction(act1)
        file_menu.addSeparator()
        file_menu.addAction(act2)
        file_menu.setStyleSheet("{border: 1px solid '#64646c';" +
            "border-radius: 2px;" +
            "background: #24242C;" +
            "font-size: 12px;" +
            "color: 'white';}"
            ":hover{background: #323844;}"
                                )

        # grid i layout
        grid = QGridLayout()
        centerWidget = QWidget()
        centerWidget.setLayout(grid)
        self.setCentralWidget(centerWidget)

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

        #FUNKCJE AKCJI
    def OpenFile(self):
        dialog = QFileDialog()
        #dialog.setNameFilter("Wszystkie pliki")
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        dialogSucces = dialog.exec()
        if dialogSucces:
            SELECTED_FILE_PATH = dialog.selectedFiles()
            print(SELECTED_FILE_PATH)
        else:
            print("Nie udane")


app = QApplication(sys.argv)

button2 = QPushButton('Ok')
button1 = QPushButton("Plik")
button1.setStyleSheet(
"border: 10px solid '#F3F0E7';" +
"border-radius: 10px;" +
"font-size: 30px;" +
"color: 'white';"
)
#
#grid.addWidget(button1, 0, 0)
#grid.addWidget(button2, 0, 1))
w = MainWindow()
w.show()
sys.exit(app.exec())