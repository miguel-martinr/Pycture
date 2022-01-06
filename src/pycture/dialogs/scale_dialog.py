from typing import List
from PyQt5.QtWidgets import QDialog, QLabel, QLayout, QLineEdit, QMainWindow, QPushButton, QSizePolicy, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, Signal
from . import Notification

from .widgets import CustomIntValidator, DropdownList


class ScaleDialog(QDialog):
    #                img  interpolation  size(int, int)
    applied = Signal(str, str, tuple)
    
    def __init__(self, parent: QMainWindow, editors: List[str], interpolation_techniques: List[str]):
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Scale")
        self.layout = QVBoxLayout()
        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(self.layout)
        self.setup(editors, interpolation_techniques)
        self.show()
        
    def setup(self, editors: List[str], interpolation_techniques: List[str]):
        layout = QVBoxLayout()
        self.layout.addLayout(layout)

        self.editors_dropdown = DropdownList(self, editors)
        layout.addWidget(self.editors_dropdown)
        
        self.interpolation_dropdown = DropdownList(self, interpolation_techniques)
        layout.addWidget(self.interpolation_dropdown)

        self.width = QLineEdit("1", self)
        validator = CustomIntValidator(0, 10000)
        self.width.setValidator(validator)
        layout.addWidget(self.width)

        self.height = QLineEdit("1", self)
        validator = CustomIntValidator(0, 10000)
        self.height.setValidator(validator)
        layout.addWidget(self.height)
        
        separator = QWidget()
        separator.setMinimumSize(0, 0)
        separator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(separator)

        apply_button = QPushButton("Scale", self)
        apply_button.clicked.connect(self.emit_applied)
        layout.addWidget(apply_button)
        
    def emit_applied(self):
        editor = self.editors_dropdown.currentText()
        if self.parent().get_editor(editor) is None:
            Notification(self, "An active image must be chosen")
            return
        size = (int(self.width.text()), int(self.height.text()))
        self.applied.emit(self.editors_dropdown.currentText(), 
                          self.interpolation_dropdown.currentText(), 
                          size)
        
    def set_editor(self, editor: str):
        self.editors_dropdown.set_selected(editor)
        
    def set_interpolation_technique(self, technique: str):
        self.interpolation_dropdown.set_selected(technique)
        
    