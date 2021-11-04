from PyQt5.QtCore import Qt, Signal
from PyQt5.QtGui import QDoubleValidator, QValidator
from PyQt5.QtWidgets import QDialog, QGridLayout, QLineEdit, QMainWindow, QPushButton, QSlider
import re

class GammaCorrectionDialog(QDialog):
    
    applied = Signal(float)
    plot = Signal(float)

    def __init__(self, parent: QMainWindow, top = 20) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self._setup_(top)
        self.show()


    def _setup_(self, top):
        self.setFixedWidth(300)
        self.setWindowTitle("Gamma correction")
        layout = QGridLayout()
        self.setLayout(layout)

        self._set_inputs_(top)
        self._set_buttons_()
        pass

    def _set_inputs_(self, top):
        layout = QGridLayout()
        self.layout().addLayout(layout, 0, 0)
    
        self._slider_ = QSlider(Qt.Orientation.Horizontal, self)
        self._slider_.setMaximum(top / 0.02)
        layout.addWidget(self._slider_, 0, 0, Qt.AlignmentFlag.AlignCenter)

        self._numeric_input_ = QLineEdit("0.5", self)
        self._numeric_input_.setFixedWidth(40)
        self._numeric_input_.setValidator(DoubleValidator(0, top, 2))
        layout.addWidget(self._numeric_input_, 0, 1, Qt.AlignmentFlag.AlignCenter)
        
        
        self._slider_.sliderMoved.connect(lambda value: self._numeric_input_.setText(f"{(value * 0.02):.2f}"))
        self._numeric_input_.textEdited.connect(lambda text: self._slider_.setValue(round(self._to_double_(text) / 0.02)))

    def _set_buttons_(self):
        layout = QGridLayout()
        self.layout().addLayout(layout, 1, 0)

        accept_btn = QPushButton("Apply", self)
        accept_btn.clicked.connect(lambda: self.applied.emit(self.get_gamma()))
        layout.addWidget(accept_btn, 0, 0, Qt.AlignmentFlag.AlignCenter)

        plot_btn = QPushButton("Plot", self)
        plot_btn.clicked.connect(lambda: self.plot.emit(self.get_gamma()))
        layout.addWidget(plot_btn, 0, 1, Qt.AlignmentFlag.AlignCenter)

    def get_gamma(self):
        return self._to_double_(self._numeric_input_.text())

    def _to_double_(self, text):
        return 0.0 if text == "" else float(text)

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

