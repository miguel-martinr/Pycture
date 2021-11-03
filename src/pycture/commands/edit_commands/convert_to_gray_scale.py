from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QMainWindow

from ..command import Command
from pycture.dialogs import Notification, SegmentsInput


class ConvertToGrayScale(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Gray scale (NTSC)")

    def execute(self, main_window: QMainWindow):
        image, title = self.get_active_image_and_title(main_window)
        if image is None:
            return

        gray_scaled_image = image.get_gray_scaled_image()
        main_window.add_editor(gray_scaled_image, title + "(GrayScaled)")
