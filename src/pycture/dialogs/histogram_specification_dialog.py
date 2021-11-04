from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QSlider
from PyQt5.QtCore import Qt, Signal


class HistogramSpecificationDialog(QDialog):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Specify Histogram")
        self.show()