from PyQt5.QtCore import Qt, Signal
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout
from pycture.dialogs import Notification

from pycture.dialogs.dropdown_list import DropdownList

class DifferenceDialog(QDialog):
    applied = Signal(str, str)

    def __init__(self, parent: QMainWindow, options: [str]) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self._setup_(options)
        self.show()

    def _setup_(self, options: [str]):
        layout = QVBoxLayout(self)
        self.setWindowTitle("Image difference")
        self.setLayout(layout)
        self._set_dropdowns_(options)
        self._set_btns_()

        maximum_width = 300
        self.setMinimumWidth(maximum_width)
        self.setMaximumWidth(maximum_width)

    def _set_dropdowns_(self, options: [str]):
        layout = self.layout()
        
        label_a = QLabel("Image A:", self)
        layout.addWidget(label_a)
        self.dropwdown_a = DropdownList(self, options)
        layout.addWidget(self.dropwdown_a)

        label_b = QLabel("Image B:", self)
        layout.addWidget(label_b)
        self.dropwdown_b = DropdownList(self, options)
        layout.addWidget(self.dropwdown_b)
    
    def _apply_(self):
        image_a = self.dropwdown_a.currentText()
        image_b = self.dropwdown_b.currentText()

        if (len(image_a) == 0 or len(image_b) == 0):
            Notification(self, "You have to choose the images you want to use")
            return

        self.applied.emit(image_a, image_b)

    def _set_btns_(self):
        layout = QHBoxLayout()
        self.layout().addLayout(layout)
        
        apply_btn = QPushButton("Apply", self)
        layout.addWidget(apply_btn)

        map_of_changes_btn = QPushButton("Map of changes", self)
        layout.addWidget(map_of_changes_btn)
        
        apply_btn.pressed.connect(self._apply_)

        


