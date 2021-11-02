from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QMainWindow

from ..command import Command
from pycture.dialogs import Notification, SegmentsInput


class ConvertToGrayScale(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Gray scale (NTSC)")

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

        gray_scaled_image = image.get_gray_scaled_image()
        main_window.add_editor(gray_scaled_image, title + "(GrayScaled)")
