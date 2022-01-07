from PyQt5.QtWidgets import QWidget, QMainWindow

from ..command import Command


class HorizontalMirror(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Horizontal Mirror")

    def execute(self, main_window: QMainWindow):
        image, title = self.get_active_image_and_title(main_window)
        if image is None:
            return

        mirrored_image = image.mirrored(True, False)
        main_window.add_editor(mirrored_image, title + "(horizontal mirrored)")
