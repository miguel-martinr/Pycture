from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt

DATA_BAR_HEIGHT = 35


class DataBar(QLabel):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        # Get the correct needed width for the label
        self.update_data((1000, 1000), (255, 255, 255))
        self.setFixedWidth(self.minimumSizeHint().width())
        self.update_data((0, 0), (0, 0, 0))
        self.setFixedHeight(DATA_BAR_HEIGHT)

    def update_data(self, pos: (int, int), rgb: (int, int, int)):
        self.setText(
            f"X:{pos[0]}\tY:{pos[1]}\tR:{rgb[0]}\tG:{rgb[1]}\tB:{rgb[2]}")
