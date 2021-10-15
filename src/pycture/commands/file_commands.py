from os import path

from PyQt5.QtWidgets import QWidget, QFileDialog, QMainWindow
from PyQt5.QtGui import QPixmap

from .command import Command

class OpenFileCommand(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Open")

    def execute(self, main_window: QMainWindow):
        file_path, _ = QFileDialog.getOpenFileName(None, "Open an image", "/home", "Images (*.png *.jpg *.jpeg *.bmp)")
        if not file_path:
            return
        (_, filename) = path.split(file_path)
        main_window.add_editor(QPixmap(file_path), filename)

class SaveFileCommand(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Save")

    def execute(self, main_window: QMainWindow):
        image = self.get_active_image(main_window)
        if image == None:
            return # TODO: Notify the user (can't save if there isn't images)
        file_path, _ = QFileDialog.getSaveFileName(None, "Save an image", "/home", "Images (*.png *.jpg *.jpeg *.bmp)")
        if not file_path:
            return
        _, extension = path.splitext(file_path)
        if not extension:
            extension = ".png"
        elif extension not in [".png", ".jpg", ".jpeg", ".bmp"]:
            return # TODO: Notify the user about the supported formats
        image.pixmap().save(file_path, extension[1:])