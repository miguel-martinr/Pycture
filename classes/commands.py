from PyQt5.QtWidgets import QAction, QWidget, QFileDialog 
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QCoreApplication
from classes.events import NewEditorEvent


class Command(QAction):
    def __init__(self, text: str, parent: QWidget) -> None:
        super().__init__(parent)
        self.setText(text)

class OpenFile(Command):
    def __init__(self, parent: QWidget) -> None:
        super().__init__("Open", parent)
        self.triggered.connect(self.run)

    def run(self):
        path, _ = QFileDialog.getOpenFileName(None, "Open an image", "/home", "Images (*.png *.jpg *.jpeg *.bmp)")
        QCoreApplication.sendEvent(self.parent(), NewEditorEvent(QPixmap(path), path))

class SaveFile(Command):
    def __init__(self, parent: QWidget) -> None:
        super().__init__("Save", parent)
        self.triggered.connect(self.run)

    def run(self):
        print("Saves File")

file_commands = [OpenFile, SaveFile]



class EditBright(Command):
    def __init__(self, parent: QWidget) -> None:
        super().__init__("Bright", parent)
        self.triggered.connect(self.run)

    def run(self):
        print("Edits bright")


edit_commands = [EditBright]