from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QEvent, QCoreApplication

from .image import Image
from .data_bar import DataBar, DATA_BAR_HEIGHT


class Container(QWidget):
    def __init__(self, parent: QWidget, image: QPixmap):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.image = Image(self, image)
        layout.addWidget(self.image)
        layout.setSpacing(0)
        self.data_bar = DataBar(self)
        layout.addWidget(self.data_bar)
        self.setFixedHeight(self.image.height() + DATA_BAR_HEIGHT * 2)
        self.setLayout(layout)

    def update_data_bar(self, pos: (int, int), rgb: (int, int, int)):
        self.data_bar.update_data(pos, rgb)

    def customEvent(self, event: QEvent):
        QCoreApplication.sendEvent(self.parent(), event)
