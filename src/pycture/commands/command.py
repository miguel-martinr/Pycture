from PyQt5.QtWidgets import QAction, QWidget, QMainWindow
from PyQt5.QtCore import QCoreApplication

from ..events import ExecuteCommandEvent

class Command(QAction):
    def __init__(self, text: str, parent: QWidget):
        super().__init__(parent)
        self.setText(text)
        self.triggered.connect(self.clicked)
    
    def clicked(self):
        QCoreApplication.sendEvent(self.parent(), ExecuteCommandEvent(self))
    
    def execute(self, main_window: QMainWindow):
        print("Executing base command")

