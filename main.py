from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QDockWidget
from PyQt5.QtGui import QPixmap
from classes.controls_bar import ControlsBar
from PyQt5.QtCore import QEvent
from sys import argv

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pycture")
        self.setMenuBar(ControlsBar(self))
    
    def customEvent(self, e):
        print("Event reached MainWindow")

app = QApplication(argv)
window = MainWindow()
window.show()
app.exec()
