from PyQt5.QtWidgets import QMessageBox, QWidget


class Notification(QMessageBox):
    def __init__(self, parent: QWidget, message: str):
        super().__init__(parent)
        self.setText(message)
        self.addButton(QMessageBox.StandardButton.Ok)
        self.setWindowTitle("Pycture")
