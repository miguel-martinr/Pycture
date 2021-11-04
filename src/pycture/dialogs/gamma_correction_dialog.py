from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator, QValidator
from PyQt5.QtWidgets import QDialog, QGridLayout, QLineEdit, QMainWindow, QSlider
import re

class GammaCorrectionDialog(QDialog):
    def __init__(self, parent: QMainWindow, top = 20) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self._setup_(top)
        self.show()

    def _setup_(self, top):
        layout = QGridLayout()
        self.setLayout(layout)

        self._set_inputs_(top)
        self._set_buttons_()
        pass

    def _set_inputs_(self, top):
        layout = QGridLayout()
        self.layout().addLayout(layout, 0, 0)
    
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setMaximum(top / 0.02)
        layout.addWidget(self.slider, 0, 0, Qt.AlignmentFlag.AlignCenter)

        self.numeric_input = QLineEdit("0.5", self)
        self.numeric_input.setFixedWidth(40)
        self.numeric_input.setValidator(DoubleValidator(0, top, 2))
        layout.addWidget(self.numeric_input, 0, 1, Qt.AlignmentFlag.AlignRight)
        
        to_double = lambda text: 0.0 if text == "" else float(text)
        self.slider.sliderMoved.connect(lambda value: self.numeric_input.setText(f"{(value * 0.02):.2f}"))
        self.numeric_input.textEdited.connect(lambda text: self.slider.setValue(round(to_double(text) / 0.02)))

    def _set_buttons_(self):
        pass


class DoubleValidator(QDoubleValidator):
    def __init__(self, bottom: int, top: int, decimals: int):
        super().__init__()
        self.bottom = bottom
        self.top = top
        self.decimals = decimals

    def validate(self, input: str, pos: int):
        State = QValidator.State

        if (input == ""):
            return State.Intermediate, input, pos

        if (input[-1] == ','):
            return State.Invalid, input, pos 

        matched_float = re.match('^\d+(\.)?(\d{1,2})?$', input)
        if (not matched_float):
            return State.Invalid, input, pos

        if (not (self.bottom <= float(input) <= self.top)):
            return State.Invalid, input, pos
        return State.Acceptable, input, pos

