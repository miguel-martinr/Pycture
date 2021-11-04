from PyQt5.QtWidgets import QDialog, QVBoxLayout, QMainWindow, QPushButton, QLabel
from PyQt5.QtCore import Qt, Signal

from .rgb_checkboxes import RGBCheckboxes
from .dropdown_list import DropdownList
from pycture.dialogs import Notification


class HistogramSpecificationDialog(QDialog):
    # (str, str, (bool, bool, bool))
    # (base, sample, (r, g, b))
    editors_selected = Signal(tuple)

    def __init__(self, parent: QMainWindow, options: [str]):
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Specify Histogram")
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.checkboxes = RGBCheckboxes(self)
        layout.addWidget(self.checkboxes)

        label1 = QLabel("Base image:", self)
        layout.addWidget(label1)
        self.base_dropdown = DropdownList(self, options)
        layout.addWidget(self.base_dropdown)
        label2 = QLabel("Image to sample from:", self)
        layout.addWidget(label2)
        self.sample_dropdown = DropdownList(self, options)
        layout.addWidget(self.sample_dropdown)

        button = QPushButton("Accept", self)
        layout.addWidget(button)
        button.pressed.connect(self.select_editors)
        self.setFixedSize(self.minimumSizeHint())
        self.show()

    def select_editors(self):
        base = self.base_dropdown.currentText()
        sample = self.sample_dropdown.currentText()
        if len(base) == 0 or len(sample) == 0:
            Notification(self, "You have to choose the images you want to use")
            return
        if sample == base:
            Notification(self, "Can't use the same image as sample and base")
            return
        self.editors_selected.emit((base, sample, self.checkboxes.get_checked()))