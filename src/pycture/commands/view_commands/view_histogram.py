from io import BytesIO
from typing import List

from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap

import matplotlib.pyplot as plt
from PIL.ImageQt import ImageQt
from PIL import Image

from ..command import Command
from pycture.dialogs import Notification
from pycture.editor.image import Color


class ViewHistogramCommand(Command):
    def __init__(self, parent: QWidget, color: str):
        super().__init__(parent, color)

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
        histogram = self.get_histogram(image)
        mean = self.get_mean(image)

        figure = self.draw_histogram(histogram, mean)
        self.write_mean(mean)
        pixmap = self.save_figure_to_pixmap(figure)
        main_window.add_editor(pixmap, title + "." + self.text() + "-hist")

    def draw_histogram(self, histogram: List[int], mean: float) -> plt.figure:
        plt.style.use('dark_background')
        figure = plt.figure()
        bars = plt.bar(list(range(256)), histogram)
        for index, bar in enumerate(bars):
            color = self.get_bar_color(index)
            # This scaling is made so the values don't reach pure black and can
            # be seen
            color = list(map(lambda val: 0 if val ==
                         0 else (val * 240 + 15) / 255, color))
            bar.set_color(color)
        return figure

    def write_mean(self, mean: float):
        plt.axvline(mean)
        plt.title(f"Mean: {mean:.2f}")

    def save_figure_to_pixmap(self, figure: plt.figure) -> QPixmap:
        buffer = BytesIO()
        figure.savefig(buffer)
        return QPixmap.fromImage(ImageQt(Image.open(buffer)))

    def get_bar_color(self, val: int) -> List[float]:
        pass

    def get_histogram(self, image: QLabel) -> List[int]:
        return image.get_histogram(self.color)

    def get_mean(self, image: QLabel) -> float:
        return image.get_mean(self.color)


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
