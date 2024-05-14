import PyQt5.QtWidgets as Qtw

class Additional_Windows_Text(Qtw.QWidget):
    def __init__(self):
        super().__init__()
        layout = Qtw.QVBoxLayout()
        self.label = Qtw.QLabel("")
        layout.addWidget(self.label)
        self.setLayout(layout)
        my_text = Qtw.QTextEdit(self,
                                lineWrapMode=Qtw.QTextEdit.FixedColumnWidth,
                                lineWrapColumnOrWidth=50,
                                placeholderText="Hellow World!"
                                )