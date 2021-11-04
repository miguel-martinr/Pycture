from PyQt5.QtWidgets import QDialog, QVBoxLayout, QMainWindow 
from PyQt5.QtCore import Qt 

from .rgb_checkboxes import RGBCheckboxes

class HistogramSpecificationDialog(QDialog):
    def __init__(self, parent: QMainWindow, title: str) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Specify Histogram")
        self.show()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.checkboxes = RGBCheckboxes(self)
        layout.addWidget(self.checkboxes)