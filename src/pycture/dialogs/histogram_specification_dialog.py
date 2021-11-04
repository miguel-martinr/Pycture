from PyQt5.QtWidgets import QDialog, QVBoxLayout, QMainWindow 
from PyQt5.QtCore import Qt 

from .rgb_checkboxes import RGBCheckboxes
from .dropdown_list import DropdownList

class HistogramSpecificationDialog(QDialog):
    def __init__(self, parent: QMainWindow, options: [str]):
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Specify Histogram")
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.checkboxes = RGBCheckboxes(self)
        layout.addWidget(self.checkboxes)
        label1 = QLabel("Base image:", self)
        layout.addWidget(label1)
        base_dropdown = DropdownList(self, options)
        layout.addWidget(self.base_dropdown)
        label2 = QLabel("Image to sample from:", self)
        layout.addWidget(label2)
        self.sample_dropdown = DropdownList(self, options)
        layout.addWidget(self.sample_dropdown)
        self.setFixedSize(self.minimumSizeHint())
        self.show()
