import PyQt5.QtWidgets as qtw

class Additional_Windows_Text(qtw.QWidget):
    def __init__(self):
        super().__init__()
        layout = qtw.QVBoxLayout()
        self.label = qtw.QLabel("")
        layout.addWidget(self.label)
        self.setLayout(layout)
        my_text = qtw.QTextEdit(self,
                                lineWrapMode=qtw.QTextEdit.FixedColumnWidth,
                                lineWrapColumnOrWidth=50,
                                placeholderText="Hellow World!"
                                )