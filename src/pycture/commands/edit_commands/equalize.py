from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtGui import QPixmap

from ..command import Command
from pycture.editor.image import RGBColor, Image


class Equalize(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Equalize")

    def execute(self, main_window: QMainWindow):
        image, title = self.get_active_image_and_title(main_window)
        if image is None:
            return
    
        new_image = Image(image)
        for color in RGBColor:
            lut = []
            for val in image.get_cumulative_histogram(color):
                lut.append(max(0, round(val * 256) - 1))
            rgb_bools = (color == RGBColor.Red, color == RGBColor.Green, color == RGBColor.Blue)
            new_image = new_image.apply_LUT(lut, rgb_bools)

        main_window.add_editor(new_image, title + "(Equalized)")
