from PyQt5.QtWidgets import QAction, QWidget, QLabel, QFileDialog, QDockWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QEvent


class Command(QAction):
    def __init__(self, text: str, parent: QWidget) -> None:
        super(QAction, self).__init__(parent)
        self.setText(text)

    def run(self):  # Metaclass issue when making it abstract
        pass

class OpenFile(Command):
    def __init__(self, parent: QWidget) -> None:
        super(Command, self).__init__("Open", parent)
        self.triggered.connect(self.run)

    def run(self):
        filename, _ = QFileDialog.getOpenFileName(None, "Open an image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        label = QLabel()
        label.setPixmap(QPixmap(filename))
        print(label)
        # dock = QDockWidget("AAAAh", self.parent)

class SaveFile(Command):
    def __init__(self, parent: QWidget) -> None:
        super(Command, self).__init__("Save", parent)
        self.triggered.connect(self.run)

    def run(self):
        print("Saves File")

file_cmds = [OpenFile, SaveFile]



class EditBright(Command):
    def __init__(self, parent: QWidget) -> None:
        super(Command, self).__init__("Bright", parent)
        self.triggered.connect(self.run)

    def run(self):
        print("Edits bright")





edit_cmds = [EditBright]