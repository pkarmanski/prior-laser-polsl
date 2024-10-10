from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QSlider, QLabel
from app.consts.presentation_consts import SLIDER_MAX, SLIDER_MIN, SLIDER_TIC


class Slider(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.print_scale_slider: QSlider = QSlider(Qt.Horizontal)
        self.print_scale_slider_label: QLabel = QLabel("Scale 1")

        self.config()

    def config(self):
        self.print_scale_slider.setMinimum(SLIDER_MIN)
        self.print_scale_slider.setMaximum(SLIDER_MAX)
        self.print_scale_slider.setTickPosition(QSlider.TicksBelow)
        self.print_scale_slider.setTickInterval(SLIDER_TIC)
        self.print_scale_slider_label.setObjectName('scale-info-element')
        self.addWidget(self.print_scale_slider_label)
        self.addWidget(self.print_scale_slider)
