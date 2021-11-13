import re

from PyQt5.QtCore import Qt, Signal
from PyQt5.QtWidgets import (
    QDialog, QHBoxLayout, QVBoxLayout, QLineEdit, QMainWindow, QPushButton,
    QSlider, QLayout, QLabel
)

from .widgets import CustomDoubleValidator


class GammaCorrectionDialog(QDialog):
    applied = Signal(float)
    plot = Signal(float)

    # Slider limit should never be less than or equal to 0
    def __init__(self, parent: QMainWindow, slider_limit: int = 30) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Gamma correction")
        self.layout = QVBoxLayout()
        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(self.layout)

        label = QLabel("Gamma value:", self)
        self.layout.addWidget(label)

        self.slider_limit = slider_limit
        self.setup_slider()
        self.setup_buttons()
        self.show()

    def setup_slider(self):
        layout = QHBoxLayout()
        self.layout.addLayout(layout)

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setMinimum(2 - self.slider_limit)
        self.slider.setMaximum(self.slider_limit)
        self.slider.setValue(1)
        self.slider.setFixedWidth(200)
        layout.addWidget(self.slider)

        self.numeric_input = QLineEdit("1", self)
        self.numeric_input.setValidator(CustomDoubleValidator(0, self.slider_limit, 4))
        layout.addWidget(self.numeric_input)

        self.slider.sliderMoved.connect(self.update_text_value)
        self.numeric_input.textEdited.connect(self.update_slider_value)
            
    # These changes are needed to smooth the values in the slider
    def update_text_value(self, slider_value: int):
        new_text_value = slider_value
        if slider_value < 1:
            new_text_value = 1 / (2 - slider_value)
        self.numeric_input.setText(str(round(new_text_value, 4)))
        
    # These changes are needed to smooth the values in the slider
    def update_slider_value(self, text_value: str):
        value = self.text_to_double(text_value)
        if value < 1 / self.slider_limit:
            value = 2 - self.slider_limit
        elif value < 1:
            value = 2 - 1 / value
        self.slider.setValue(round(value))

    def setup_buttons(self):
        layout = QHBoxLayout()
        self.layout.addLayout(layout)

        accept_button = QPushButton("Apply", self)
        accept_button.clicked.connect(lambda: self.applied.emit(self.get_gamma()))
        layout.addWidget(accept_button)

        plot_button = QPushButton("Plot", self)
        plot_button.clicked.connect(lambda: self.plot.emit(self.get_gamma()))
        layout.addWidget(plot_button)

    def get_gamma(self):
        return max(self.text_to_double(self.numeric_input.text()), 1 / self.slider_limit)

    def text_to_double(self, text):
        return 0.0 if text == "" else float(text)
