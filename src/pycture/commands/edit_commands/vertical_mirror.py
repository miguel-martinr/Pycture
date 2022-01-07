from PyQt5.QtWidgets import QWidget, QMainWindow

from ..command import Command


class VerticalMirror(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Vertical Mirror")

    def execute(self, main_window: QMainWindow):
        image, title = self.get_active_image_and_title(main_window)
        if image is None:
            return

        mirrored_image = image.mirrored(False, True)
        main_window.add_editor(mirrored_image, title + "(vertical mirrored)")
