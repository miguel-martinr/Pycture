from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt

class InformationWindow(QWidget):
    def __init__(self, parent: QWidget, title: str, text: str):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.text = QLabel()
        self.text.setText(text)
        self.layout.addWidget(self.text)

        self.setParent(parent, Qt.WindowType.Window)
        self.text.setMinimumSize(self.text.minimumSizeHint())
        self.setMinimumWidth(300)
        self.show()
    