from os import path

from PyQt5.QtWidgets import QWidget, QFileDialog, QMainWindow
from PyQt5.QtGui import QPixmap

from .command import Command

class OpenFileCommand(Command):
    def __init__(self, parent: QWidget):
        super().__init__("Open", parent)

    def execute(self, main_window: QMainWindow):
        file_path, _ = QFileDialog.getOpenFileName(None, "Open an image", "/home", "Images (*.png *.jpg *.jpeg *.bmp)")
        (_, filename) = path.split(file_path)
        main_window.addEditor(QPixmap(file_path), filename)

class SaveFileCommand(Command):
    def __init__(self, parent: QWidget):
        super().__init__("Save", parent)

    def execute(self, main_window: QMainWindow):
        activeEditor = main_window.getActiveEditor()
        if activeEditor == None:
            return # TODO: Notify the user (can't save if there isn't images)
        file_path, _ = QFileDialog.getSaveFileName(None, "Save an image", "/home", "Images (*.png *.jpg *.jpeg *.bmp)")
        (_, extension) = path.splitext(file_path)
        if not extension:
            extension = ".png"
        elif extension not in [".png", ".jpg", ".jpeg", ".bmp"]:
            return # TODO: Notify the user about the supported formats
        pixmap = activeEditor.widget().pixmap()
        pixmap.save(file_path, extension[1:])