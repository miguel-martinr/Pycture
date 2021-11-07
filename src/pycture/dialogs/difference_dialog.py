from PyQt5.QtCore import Qt, Signal
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout
from pycture.dialogs import Notification

from pycture.dialogs.dropdown_list import DropdownList
from pycture.dialogs.map_of_changes_dialog import MapOfChangesDialog


class DifferenceDialog(QDialog):
    applied = Signal(str, str)
    map_of_changes = Signal(str, str)

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

    def _apply_(self, map_of_changes: bool = False):
        image_a = self.dropwdown_a.currentText()
        image_b = self.dropwdown_b.currentText()

        if (len(image_a) == 0 or len(image_b) == 0):
            Notification(self, "You have to choose the images you want to use")
            return

        signal = self.map_of_changes if map_of_changes else self.applied
        signal.emit(image_a, image_b)
  
    def _set_btns_(self):
        layout = QHBoxLayout()
        self.layout().addLayout(layout)

        apply_btn = QPushButton("View Difference", self)
        layout.addWidget(apply_btn)
        apply_btn.pressed.connect(self._apply_)

        map_of_changes_btn = QPushButton("Map of changes", self)
        layout.addWidget(map_of_changes_btn)
        map_of_changes_btn.pressed.connect(lambda: self._apply_(map_of_changes=True))
