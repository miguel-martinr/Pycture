from typing import List
from PyQt5.QtWidgets import QDialog, QLabel, QLayout, QLineEdit, QMainWindow, QPushButton, QSizePolicy, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, Signal
from . import Notification

from .widgets import CustomDoubleValidator, DropdownList


class RotateSimpleDialog(QDialog):
    #                img   angle
    applied = Signal(str, float)

    def __init__(self, parent: QMainWindow, editors: List[str], angle_limit = 180):
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Rotate and Paint")
        self.layout = QVBoxLayout()
        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(self.layout)
        self.angle_limit = angle_limit

        self.setup(editors)
        
        self.show()
        
        

    def setup(self, editors: List[str]):
        layout = QVBoxLayout()
        self.layout.addLayout(layout)

        self.editors_dropdown = DropdownList(self, editors)
        self.editors_dropdown.setMinimumWidth(250)
        layout.addWidget(self.editors_dropdown)
        

        label = QLabel("Angle:", self)
        layout.addWidget(label)

        self.numeric_input = QLineEdit("1", self)
        self.numeric_input.setValidator(
            CustomDoubleValidator(-self.angle_limit, self.angle_limit, 2))
        layout.addWidget(self.numeric_input)

        separator = QWidget()
        separator.setMinimumSize(0, 0)
        separator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(separator)

        apply_button = QPushButton("Rotate", self)
        apply_button.clicked.connect(self.emit_applied)
        layout.addWidget(apply_button)

    def emit_applied(self):
        editor = self.editors_dropdown.currentText()
        if self.parent().get_editor(editor) is None:
            Notification(self, "An active image must be chosen")
            return
        self.applied.emit(self.editors_dropdown.currentText(),
                          float(self.numeric_input.text()))

    def set_editor(self, editor: str):
        self.editors_dropdown.set_selected(editor)
