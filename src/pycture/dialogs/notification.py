from PyQt5.QtWidgets import QMessageBox

class Notification(QMessageBox):
    def __init__(self, message: str):
        super().__init__()
        self.setText(message)
        self.addButton(QMessageBox.StandardButton.Ok)
        self.setWindowTitle("Pycture")