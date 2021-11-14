from PyQt5.QtCore import Qt, Signal
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout

from pycture.dialogs.widgets import DropdownList
from .notification import Notification


class SelectTwoImagesDialog(QDialog):
    applied = Signal(str, str)

    def __init__(self, parent: QMainWindow, options: [str], button_text: str = "Accept") -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self._setup_(options, button_text)
        self.show()

    def _setup_(self, options: [str], button_text: str):
        layout = QVBoxLayout(self)
        self.setWindowTitle("Select two images")
        self.setLayout(layout)
        self._set_dropdowns_(options)
        self._set_btn_(button_text)

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

    def _set_btn_(self, button_text: str):
        layout = QHBoxLayout()
        self.layout().addLayout(layout)

        apply_btn = QPushButton(button_text, self)
        layout.addWidget(apply_btn)
        apply_btn.pressed.connect(self._apply_)

