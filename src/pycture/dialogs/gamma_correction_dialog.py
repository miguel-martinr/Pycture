import re

from PyQt5.QtCore import Qt, Signal
from PyQt5.QtWidgets import (
    QDialog, QHBoxLayout, QVBoxLayout, QLineEdit, QMainWindow, QPushButton, QSlider, QLayout
)

from .widgets import CustomDoubleValidator


class GammaCorrectionDialog(QDialog):
    applied = Signal(float)
    plot = Signal(float)

    def __init__(self, parent: QMainWindow, upper_limit=20) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Gamma correction")
        self.setFixedWidth(300)
        self.layout = QVBoxLayout()
        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(self.layout)

        self.setup_slider(upper_limit)
        self.setup_buttons()
        self.show()


    def setup_slider(self, upper_limit):
        layout = QHBoxLayout()
        self.layout.addLayout(layout)

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setMaximum(upper_limit / 0.02)
        layout.addWidget(self.slider)

        self.numeric_input = QLineEdit("0.5", self)
        self.numeric_input.setFixedWidth(40)
        self.numeric_input.setValidator(CustomDoubleValidator(0, upper_limit, 2))
        layout.addWidget(self.numeric_input)

        self.slider.sliderMoved.connect(
            lambda value: self.numeric_input.setText(f"{(value * 0.02):.2f}"))
        self.numeric_input.textEdited.connect(
            lambda text: self.slider.setValue(
                round(
                    self.text_to_double(text) /
                    0.02)))

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
        return self.text_to_double(self.numeric_input.text())

    def text_to_double(self, text):
        return 0.0 if text == "" else float(text)
