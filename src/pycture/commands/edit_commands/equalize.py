from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtGui import QPixmap

from ..command import Command
from pycture.editor.image import Color


class Equalize(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Equalize")

    def execute(self, main_window: QMainWindow):
        image = self.get_active_image(main_window)
        title = self.get_active_title(main_window)
        if image is None:
            notification = Notification(
                main_window, "There isn't an active editor!").exec()
            return
        if not image.load_finished:
            notification = Notification(main_window,
                                        "The image is still loading. Please wait a bit").exec()
            return

        image = image.get_equalized([Color.Red, Color.Green, Color.Blue])
        main_window.add_editor(QPixmap.fromImage(image), title + "(Equalized)")
