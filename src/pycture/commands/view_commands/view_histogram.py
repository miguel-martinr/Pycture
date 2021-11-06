from typing import List

from PyQt5.QtWidgets import QWidget, QMainWindow 

import matplotlib.pyplot as plt

from ..command import Command
from pycture.editor.image import Color, Image


class ViewHistogram(Command):
    def __init__(self, parent: QWidget, color: str):
        super().__init__(parent, color)

    def execute(self, main_window: QMainWindow):
        image, title = self.get_active_image_and_title(main_window)
        if image is None:
            return

        histogram = self.get_histogram(image)
        mean = self.get_mean(image)

        self.show_histogram(histogram, mean, title)
        
    def show_histogram(self, histogram: List[int], mean: float, title: str):
        plt.style.use('dark_background')
        new_title = self.get_title(title)
        plt.figure(new_title)
        plt.title(new_title)
        self.draw_histogram(histogram)
        self.write_mean(mean)
        plt.show()


    def draw_histogram(self, histogram: List[int]):
        bars = plt.bar(list(range(256)), histogram)
        for index, bar in enumerate(bars):
            color = self.get_bar_color(index)
            # This scaling is made so the values don't reach pure black and can
            # be seen
            color = list(map(lambda val: 0 if val ==
                         0 else (val * 200 + 55) / 255, color))
            bar.set_color(color)

    def write_mean(self, mean: float):
        plt.axvline(mean)
        plt.title(f"Mean: {mean:.2f}")
        
    def get_title(self, old_title: str):
        return old_title + "." + self.text() + "-hist"

    def get_bar_color(self, val: int) -> List[float]:
        pass

    def get_histogram(self, image: Image) -> List[int]:
        return image.get_histogram(self.color)

    def get_mean(self, image: Image) -> float:
        return image.get_mean(self.color)


class ViewRedHistogram(ViewHistogram):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Red")
        self.color = Color.Red

    def get_bar_color(self, val: int) -> List[float]:
        return (val / 255, 0, 0)


class ViewGreenHistogram(ViewHistogram):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Green")
        self.color = Color.Green

    def get_bar_color(self, val: int) -> List[float]:
        return (0, val / 255, 0)


class ViewBlueHistogram(ViewHistogram):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Blue")
        self.color = Color.Blue

    def get_bar_color(self, val: int) -> List[float]:
        return (0, 0, val / 255)


class ViewGrayScaleHistogram(ViewHistogram):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Gray Scale (NTSC)")
        self.color = Color.Gray

    def get_bar_color(self, val: int) -> List[float]:
        val = val / 255
        return (val, val, val)
