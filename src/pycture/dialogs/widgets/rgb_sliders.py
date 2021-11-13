from typing import Tuple

from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QSlider, QWidget
from PyQt5.QtCore import Qt

from .custom_int_validator import CustomIntValidator

class RGBSliders(QWidget):
    def __init__(self, parent: QWidget, lower_limit: int, upper_limit: int):
        super().__init__(parent)
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.number_inputs = []
        self.sliders = []
        
        for color in ["#ff0000", "#00ff00", "#0000ff"]:
            self.add_color_input(color)

    def add_color_input(self, color: str):
        slider = QSlider(Qt.Orientation.Horizontal, self)
        slider.setMinimum(self.lower_limit)
        slider.setMaximum(self.upper_limit)
        number_input = QLineEdit("0", self)
        number_input.setValidator(CustomIntValidator(0, self.upper_limit))
        slider.setStyleSheet(
            "QSlider::handle:horizontal {background-color: " + color + ";}"
        )

        slider.valueChanged.connect(lambda value: number_input.setText(str(value)))
        text_value_to_int = lambda text: 0 if text == "" else int(text)
        number_input.textChanged.connect(
            lambda text: slider.setValue(text_value_to_int(text))
        )

        self.sliders.append(slider)
        self.number_inputs.append(number_input)
        self.layout.addWidget(slider)
        self.layout.addWidget(number_input)
            
    def get_values(self) -> (int, int, int):
        return tuple(map(lambda number_input: int(number_input.text())))