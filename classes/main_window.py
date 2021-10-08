from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout
from classes.controls_bar import ControlsBar
from classes.editor import Editor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pycture")
        self.setMenuBar(ControlsBar(self))
        placeholder_widget = QWidget()
        placeholder_widget.setLayout(QGridLayout())
        self.setCentralWidget(placeholder_widget)
        self.editors = []
        self.activeEditor = None
    
    def customEvent(self, event):
        self.editors.append(Editor(self, event.image, event.image_name))