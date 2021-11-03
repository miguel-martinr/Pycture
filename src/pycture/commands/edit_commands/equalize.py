from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtGui import QPixmap

from ..command import Command
from pycture.editor.image import RGBColor, Image


class Equalize(Command):
    def __init__(self, parent: QWidget, color: str):
        super().__init__(parent, color)

    def execute(self, main_window: QMainWindow):
        image, title = self.get_active_image_and_title(main_window)
        if image is None:
            return

        luts = (list(range(256)), list(range(256)), list(range(256)))
        for color in self.get_colors():
            lut = luts[color.value]
            for index, val in enumerate(image.get_cumulative_histogram(color)):
                lut[index] = max(0, round(val * 256) - 1)
        new_image = image.apply_LUTs(luts)

        main_window.add_editor(
            new_image, title + "(" + self.text() + "Equalized)")

    def get_colors(self):
        pass


class EqualizeRed(Equalize):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Red")

    def get_colors(self):
        return [RGBColor.Red]


class EqualizeGreen(Equalize):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Green")

    def get_colors(self):
        return [RGBColor.Green]


class EqualizeBlue(Equalize):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Blue")

    def get_colors(self):
        return [RGBColor.Blue]


class EqualizeRGB(Equalize):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "RGB")

    def get_colors(self):
        return RGBColor
