from io import BytesIO
from typing import List

from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QImage, QPixmap

import matplotlib.pyplot as plt
from PIL.ImageQt import ImageQt
from PIL import Image

from ..command import Command
from pycture.dialogs import Notification
from pycture.editor.image import Color


class ViewCumulativeHistogramCommand(Command):
    def __init__(self, parent: QWidget, color: str):
        super().__init__(parent, color)

    def execute(self, main_window: QMainWindow):
        image, title = self.get_active_image_and_title(main_window)
        histogram = self.get_histogram(image)
        mean = self.get_mean(image)

        figure = self.draw_histogram(histogram, mean)
        self.write_mean(mean)
        pixmap = self.save_figure_to_image(figure)
        main_window.add_editor(pixmap, title + "." + self.text() + "-hist")

    def get_histogram(self, image: QLabel) -> List[int]:
        return image.get_cumulative_histogram(self.color)


class ViewRedHistogram(ViewHistogramCommand):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Red")
        self.color = Color.Red

    def get_bar_color(self, val: int) -> List[float]:
        return (val / 255, 0, 0)


class ViewGreenHistogram(ViewHistogramCommand):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Green")
        self.color = Color.Green

    def get_bar_color(self, val: int) -> List[float]:
        return (0, val / 255, 0)


class ViewBlueHistogram(ViewHistogramCommand):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Blue")
        self.color = Color.Blue

    def get_bar_color(self, val: int) -> List[float]:
        return (0, 0, val / 255)


class ViewGrayScaleHistogram(ViewHistogramCommand):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Gray Scale (NTSC)")
        self.color = Color.Gray

    def get_bar_color(self, val: int) -> List[float]:
        val = val / 255
        return (val, val, val)
