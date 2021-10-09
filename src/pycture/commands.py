from os import path

from PyQt5.QtWidgets import QAction, QWidget, QFileDialog, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QCoreApplication

from .events import NewEditorEvent

class Command(QAction):
    def __init__(self, text: str, parent: QWidget):
        super().__init__(parent)
        self.setText(text)
        self.triggered.connect(self.clicked)
    
    def clicked(self):
        QCoreApplication.sendEvent(self.parent(), NewEditorEvent(self))
    
    def execute(self, main_window: QMainWindow):
        print("Executing base command")

class OpenFile(Command):
    def __init__(self, parent: QWidget):
        super().__init__("Open", parent)

    def execute(self, main_window: QMainWindow):
        file_path, _ = QFileDialog.getOpenFileName(None, "Open an image", "/home", "Images (*.png *.jpg *.jpeg *.bmp)")
        (_, filename) = path.split(file_path)
        main_window.addEditor(QPixmap(file_path), filename)

class SaveFile(Command):
    def __init__(self, parent: QWidget):
        super().__init__("Save", parent)

    def execute(self, main_window: QMainWindow):
        print("Saves File")

file_commands = [OpenFile, SaveFile]



class EditBright(Command):
    def __init__(self, parent: QWidget):
        super().__init__("Bright", parent)

    def execute(self, main_window: QMainWindow):
        print("Edits bright")


edit_commands = [EditBright]