from typing import List
from enum import Enum

from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPixmap

class Color(Enum):
    Red = 0
    Green = 1
    Blue = 2

class Image(QLabel):
    def __init__(self, parent: QWidget, image: QPixmap):
        super().__init__(parent)
        self.setPixmap(image)
        self.setup_histogram_data()
        
    def setup_histogram_data(self) -> List[float]:
        image = self.pixmap().toImage()
        histograms = [[0] * 256, [0] * 256, [0] * 256]
        means = [0] * 3
        for x in range(image.width()):
          for y in range(image.height()):
            pixel = image.pixel(x, y)
            get_value = [self.get_red_value, self.get_green_value, self.get_blue_value]
            for color in Color:
                value = get_value[color.value](pixel)
                histograms[color.value][value] += 1
                means[color.value] += value

        total_pixels = image.width() * image.height()
        self.histograms = list(map(lambda histogram:
            list(map(lambda x: x / total_pixels, histogram)),
            histograms
        ))
        self.means = list(map(lambda mean: mean / total_pixels, means))

    def get_red_value(self, pixel):
        return (pixel & 0x00ff0000) >> 16
    
    def get_green_value(self, pixel):
        return (pixel & 0x0000ff00) >> 8

    def get_blue_value(self, pixel):
        return pixel & 0x000000ff 

    def get_histogram(self, color: Color):
        return self.histograms[color.value]

    def get_mean(self, color: Color):
        return self.means[color.value]


