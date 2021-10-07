from PyQt5.QtWidgets import QApplication, QMainWindow
from classes.controls_bar import ControlsBar
from sys import argv

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pycture")
        self.setMenuBar(ControlsBar(self))

app = QApplication(argv)
window = MainWindow()
window.show()
app.exec()
