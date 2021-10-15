from functools import reduce
from math import sqrt
from typing import List
from enum import Enum

from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtCore import Qt


class Color(Enum):
    Red = 0
    Green = 1
    Blue = 2
    Gray = 3


# LUT stands for LookUpTable
# These gray scale transformation values correspond to the NTSC method
GrayScaleLUT = [list(map(lambda r: 0.299 * r, list(range(256)))),
                list(map(lambda r: 0.587 * r, list(range(256)))),
                list(map(lambda r: 0.114 * r, list(range(256))))]


class Image(QLabel):
    def __init__(self, parent: QWidget, image: QPixmap):
        super().__init__(parent)
        self.setPixmap(image)
        self.setup_histogram_data()
        self.setup_info()

        self.setMouseTracking(True)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setMaximumHeight(image.height())
        self.setMaximumWidth(image.width())

    def setup_info(self):
        pixmap = self.pixmap()
        self.info = {
            "width": self.get_width(),
            "heigth": self.get_height(),
            "ranges": self.get_ranges(),
            "brightness": self.get_brightness(),
        }

    def get_width(self):
        return self.pixmap().width()

    def get_height(self):
        return self.pixmap().height()

    def get_ranges(self):
        """Returns a list with RGB-GrayScale ranges (in that order): 
             R            G           B         Gray scale
        [[min, max], [min, max], [min, max], [min, max]]
        """
        return self.ranges

    def get_brightness(self):
        return list(map(lambda color: self.get_mean(color), Color))

    def get_contrast(self):
        return list(map(lambda color: self.get_sd(color), Color))

    def get_info(self):
        return self.info

    def setup_histogram_data(self) -> List[float]:
        image = self.pixmap().toImage()
        histograms = [[0] * 256, [0] * 256, [0] * 256, [0] * 256]
        self.ranges = [[255, 0], [255, 0], [255, 0], [255, 0]]
        means = [0] * 4
        for x in range(image.width()):
            for y in range(image.height()):
                gray_value = 0
                pixel = image.pixel(x, y)
                get_value = [self.get_red_value,
                             self.get_green_value, self.get_blue_value]
                for color in [Color.Red, Color.Green, Color.Blue]:
                    value = get_value[color.value](pixel)
                    histograms[color.value][value] += 1
                    means[color.value] += value
                    gray_value += GrayScaleLUT[color.value][value]

                    # RGB Ranges
                    if (value < self.ranges[color.value][0]):
                        self.ranges[color.value][0] = value
                    if (value > self.ranges[color.value][1]):
                        self.ranges[color.value][1] = value

                gray_value = round(gray_value)
                # GrayScale range
                if (value < self.ranges[Color.Gray.value][0]):
                    self.ranges[Color.Gray.value][0] = value
                if (value > self.ranges[Color.Gray.value][1]):
                    self.ranges[Color.Gray.value][1] = value

                # GrayScale histogram and mean
                histograms[Color.Gray.value][gray_value] += 1
                means[Color.Gray.value] += gray_value

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
        if (color == 3):  # Gray scale temp fix
            return self.histograms[3]
        return self.histograms[color.value]

    def get_mean(self, color: Color):
        return self.means[color.value]

    def get_sd(self, color: Color):
        return sqrt(self.get_variance(color))

    def get_variance(self, color: Color):
        histogram = self.get_histogram(color)
        mean = self.get_mean(color)
        variance = 0
        for i in range(256):
            variance += histogram[i] * (i - mean) ** 2
        return variance

    def get_gray_scaled_image(self):
        image = self.pixmap().toImage()
        width = image.width()
        heigth = image.height()

        gray_scaled = QPixmap(width, heigth).toImage()

        for x in range(width):
            for y in range(heigth):
                color_value = image.pixel(x, y)
                red_comp = GrayScaleLUT[Color.Red.value][self.get_red_value(
                    color_value)]
                green_comp = GrayScaleLUT[Color.Green.value][self.get_green_value(
                    color_value)]
                blue_comp = GrayScaleLUT[Color.Blue.value][self.get_blue_value(
                    color_value)]

                gray_value = round(red_comp + green_comp + blue_comp)
                for _ in range(2):
                    gray_value = gray_value | (gray_value << 8)

                # Alpha correction
                gray_value = gray_value | (color_value & 0xff000000)
                gray_scaled.setPixel(x, y, gray_value)

        return gray_scaled

    def mouseMoveEvent(self, event: QMouseEvent):
        x = event.x()
        y = event.y()
        image = self.pixmap().toImage()
        if x >= image.width() or y >= image.height():
            return
        pixel_val = image.pixel(x, y)
        red_val = self.get_red_value(pixel_val)
        green_val = self.get_green_value(pixel_val)
        blue_val = self.get_blue_value(pixel_val)
        self.parent().data_bar.update_color((red_val, green_val, blue_val))
