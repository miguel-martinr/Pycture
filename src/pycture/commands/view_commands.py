from io import BytesIO
from typing import List

from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from PIL.ImageQt import ImageQt
from PIL import Image

from .command import Command, InsiderCommand
from ..editor.image import Color



class ViewHistogramCommand(InsiderCommand):
    def __init__(self, parent: QWidget, color: str):
        super().__init__(parent, color)

    def execute(self, main_window: QMainWindow):
        image, title = self.get_active_image_with_title(main_window)
        if image == None:
            print("Can't create histogram if there is not an active editor")
            return # TODO: Notify the user (can't create histogram if there isn't an active editor)
        
        histogram = self.get_histogram(image)
        mean = self.get_mean(image)

        figure = plt.figure()
        bars = plt.bar(list(range(256)), histogram)
        for index, bar in enumerate(bars):
            bar.set_color(self.get_bar_color(index))

        self.write_mean(mean)
        pixmap = self.save_figure_to_pixmap(figure)
        main_window.addEditor(pixmap, title + "." + self.text() + "-hist")

    def write_mean(self, mean: float):
        plt.axvline(mean)
        plt.title(f"Mean: {mean:.2f}")

    def save_figure_to_pixmap(self, figure) -> QPixmap:
        buffer = BytesIO()
        figure.savefig(buffer)
        return QPixmap.fromImage(ImageQt(Image.open(buffer)))

    def get_bar_color(self, val: int) -> List[float]:
        pass

    def get_histogram(self, image: QLabel) -> List[int]:
        pass

    def get_mean(self, image: QLabel) -> float:
        pass


class ViewRedHistogram(ViewHistogramCommand):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Red")

    def get_bar_color(self, val: int) -> List[float]:
        return (val / 255, 0, 0)

    def get_histogram(self, image: QLabel) -> List[int]:
        return image.get_histogram(Color.Red)

    def get_mean(self, image: QLabel) -> float:
        return image.get_mean(Color.Red)

class ViewGreenHistogram(ViewHistogramCommand):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Green")

    def get_bar_color(self, val: int) -> List[float]:
        return (0, val / 255, 0)

    def get_histogram(self, image: QLabel) -> List[int]:
        return image.get_histogram(Color.Green)

    def get_mean(self, image: QLabel) -> float:
        return image.get_mean(Color.Green)

class ViewBlueHistogram(ViewHistogramCommand):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Blue")

    def get_bar_color(self, val: int) -> List[float]:
        return (0, 0, val / 255)

    def get_histogram(self, image: QLabel) -> List[int]:
        return image.get_histogram(Color.Blue)

    def get_mean(self, image: QLabel) -> float:
        return image.get_mean(Color.Blue)


class ViewGrayScaleHistogram(ViewHistogramCommand):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Gray Scale (NTSC)")

    def get_bar_color(self, val: int) -> List[float]:
        return (val / 255, 0, val / 255) # So the whity values can be seen in the histogram

  
    def get_histogram(self, image: QLabel) -> List[int]:
        return image.get_histogram(3) # Gray isn't included in the Color enum to avoid breaking de loops based on such enum

    def get_mean(self, image: QLabel) -> float:
        return image.get_mean(3) # Gray sn't included in the Color enum to avoid breaking de loops based on such enum

        

