from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from .image import Image

class Container(QWidget):
    def __init__(self, parent: QWidget, image: QPixmap):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.image = Image(self, image)
        layout.addWidget(self.image)
        layout.addWidget(Image(self, image))
        self.setLayout(layout)
