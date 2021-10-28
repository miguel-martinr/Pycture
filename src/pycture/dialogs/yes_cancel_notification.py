from PyQt5.QtWidgets import QMessageBox, QWidget


class YesCancelNotification(QMessageBox):
    def __init__(self, parent: QWidget, message: str):
        super().__init__(parent)
        self.setText(message)
        self.setWindowTitle("Pycture")
        Yes = QMessageBox.StandardButton.Yes
        Cancel = QMessageBox.StandardButton.Cancel
        self.setStandardButtons(
            QMessageBox.StandardButtons(Yes | Cancel)
        )

    def exec(self):
        answer = super().exec()
        return answer == QMessageBox.StandardButton.Yes
