from PyQt5.QtWidgets import QWidget, QMainWindow

from ..command import Command


class RotateClockwise(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Rotate 90º clockwise")

    def execute(self, main_window: QMainWindow):
        image, title = self.get_active_image_and_title(main_window)
        if image is None:
            return

        mirrored_image = image.rotate90_clockwise()
        main_window.add_editor(mirrored_image, title + "(rotated)")
