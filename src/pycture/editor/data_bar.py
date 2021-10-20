from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt

DATA_BAR_HEIGHT = 35

class DataBar(QLabel):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.update_color((255, 255, 255)) # Get the correct needed width for the label
        self.setFixedWidth(self.minimumSizeHint().width())
        self.update_color((0, 0, 0))
        self.setFixedHeight(DATA_BAR_HEIGHT)

    def update_color(self, rgb: (int, int, int)):
        self.setText(f"R: {rgb[0]}\tG: {rgb[1]}\tB: {rgb[2]}")
