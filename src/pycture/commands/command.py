from PyQt5.QtWidgets import QAction, QWidget, QMainWindow
from PyQt5.QtCore import QCoreApplication

from ..events import ExecuteCommandEvent

class Command(QAction):
    def __init__(self, parent: QWidget, text: str):
        super().__init__(parent)
        self.setText(text)
        self.triggered.connect(self.clicked)
    
    def clicked(self):
        QCoreApplication.sendEvent(self.parent(), ExecuteCommandEvent(self))
    
    def execute(self, main_window: QMainWindow):
        print("Executing base command")

    def get_active_image(self, main_window: QMainWindow):  
        active_editor = main_window.getActiveEditor()
        if active_editor:
            return active_editor.widget()

    def get_active_title(self, main_window: QMainWindow):  
        active_editor = main_window.getActiveEditor()
        if active_editor:
            return active_editor.windowTitle()