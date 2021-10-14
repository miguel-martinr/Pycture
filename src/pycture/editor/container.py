from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

from .image import Image
from .data_bar import DataBar

class Container(QWidget):
    def __init__(self, parent: QWidget, image: QPixmap):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.image = Image(self, image)
        layout.addWidget(self.image)
        layout.setSpacing(0)
        self.data_bar = DataBar(self)
        layout.addWidget(self.data_bar)
        self.setLayout(layout)
