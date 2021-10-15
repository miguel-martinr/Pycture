from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt

class DataBar(QLabel):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.update_color((0, 0, 0))
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    def update_color(self, rgb: (int, int, int)):
        self.setText(f"R: {rgb[0]} G: {rgb[1]} B: {rgb[2]}")
