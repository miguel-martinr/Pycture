from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt

class InformationWindow(QWidget):
    def __init__(self, parent: QWidget, title: str, text: str):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.text = QLabel(self)
        self.text.setAlignment(Qt.AlignCenter)

        self.setParent(parent, Qt.WindowType.Window)
        self.text.setText(text)
        self.setFixedSize(self.text.minimumSizeHint())
        self.show()
    