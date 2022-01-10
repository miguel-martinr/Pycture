from PyQt5.QtWidgets import QWidget, QMainWindow

from ..command import Command


class Transpose(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Transpose")

    def execute(self, main_window: QMainWindow):
        image, title = self.get_active_image_and_title(main_window)
        if image is None:
            return

        mirrored_image = image.transpose()
        main_window.add_editor(mirrored_image, title + "(transposed)")
