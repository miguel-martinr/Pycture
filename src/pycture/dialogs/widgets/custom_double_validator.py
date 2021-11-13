from PyQt5.QtCore import Qt, Signal
from PyQt5.QtGui import QDoubleValidator, QValidator
from PyQt5.QtWidgets import QDialog, QGridLayout, QLineEdit, QMainWindow, QPushButton, QSlider
import re

class CustomDoubleValidator(QDoubleValidator):
    def __init__(self, lower_limit: int, upper_limit: int, decimals: int):
        super().__init__()
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.decimals = decimals

    def validate(self, input: str, pos: int):
        State = QValidator.State

        if (input == ""):
            return State.Intermediate, input, pos

        if (input[-1] == ','):
            return State.Invalid, input, pos

        matched_float = re.match('^\\d+(\\.)?(\\d{1,2})?$', input)
        if (not matched_float):
            return State.Invalid, input, pos

        if (not (self.lower_limit <= float(input) <= self.upper_limit)):
            return State.Invalid, input, pos
        return State.Acceptable, input, pos
