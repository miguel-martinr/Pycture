from typing import List
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QBoxLayout, QDialog, QHBoxLayout, QLabel, QLayout, QLineEdit, QMainWindow, QPushButton, QSizePolicy, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, Signal
from pycture.dialogs.notification import Notification

from pycture.dialogs.widgets.custom_double_validator import CustomDoubleValidator
from .widgets import DropdownList


class RotateDialog(QDialog):
    #                img  interpolation  angle
    applied = Signal(str, str, float)
    
    def __init__(self, parent: QMainWindow, editors: List[str], angle_limit = 180) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Rotate")
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
        layout.addWidget(self.editors_dropdown)
        
        self.interpolation_dropdown = DropdownList(self, ["Nearest neighbour"])
        layout.addWidget(self.interpolation_dropdown)


        label = QLabel("Angle:", self)
        layout.addWidget(label)

        self.numeric_input = QLineEdit("1", self)
        self.numeric_input.setValidator(CustomDoubleValidator(-self.angle_limit, self.angle_limit, 2))
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
                          self.interpolation_dropdown.currentText(), 
                          float(self.numeric_input.text()))
        
    def set_editor(self, editor: str):
        self.editors_dropdown.set_selected(editor)
        
    def set_interpolation_technique(self, technique: str):
        self.interpolation_dropdown.set_selected(technique)
        
    