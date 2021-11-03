from typing import List

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage

from .view_histogram import ViewHistogram
from pycture.editor.image import Color, Image


class ViewCumulativeHistogram(ViewHistogram):
    def __init__(self, parent: QWidget, color: str):
        super().__init__(parent, color)

    def get_histogram(self, image: Image) -> List[int]:
        return image.get_cumulative_histogram(self.color)

    def get_title(self, old_title: str):
        return old_title + "." + self.text() + "-cumulative-hist"


class ViewCumulativeRedHistogram(ViewCumulativeHistogram):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Red")
        self.color = Color.Red

    def get_bar_color(self, val: int) -> List[float]:
        return (val / 255, 0, 0)


class ViewCumulativeGreenHistogram(ViewCumulativeHistogram):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Green")
        self.color = Color.Green

    def get_bar_color(self, val: int) -> List[float]:
        return (0, val / 255, 0)


class ViewCumulativeBlueHistogram(ViewCumulativeHistogram):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Blue")
        self.color = Color.Blue

    def get_bar_color(self, val: int) -> List[float]:
        return (0, 0, val / 255)


class ViewCumulativeGrayScaleHistogram(ViewCumulativeHistogram):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Gray Scale (NTSC)")
        self.color = Color.Gray

    def get_bar_color(self, val: int) -> List[float]:
        val = val / 255
        return (val, val, val)
