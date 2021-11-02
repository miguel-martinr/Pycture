from math import log2, sqrt
from typing import List, Tuple

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, QSize

from .image_loader import ImageLoader
from .color import Color, RGBColor, GrayScaleLUT
from .pixel import Pixel

class Image(QImage):
    def __init__(self, image: QImage):
        super().__init__(image)
        self.setup_image_data()
        self.load_finished = False

    def setup_image_data(self):
        self.thread = QThread()
        self.worker = ImageLoader(self)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def get_brightness(self):
        return list(map(lambda color: self.get_mean(color), Color))

    def get_contrast(self):
        return list(map(lambda color: self.get_sd(color), Color))

    def get_histogram(self, color: Color):
        return self.histograms[color.value]

    def get_mean(self, color: Color):
        return self.means[color.value]

    def get_sd(self, color: Color):
        return sqrt(self.get_variance(color))

    def get_ranges(self, color: Color):
        histogram = self.histograms[color.value]
        min = 0
        max = 255
        for index, val in enumerate(histogram):
            if val != 0:
                min = index
                break
        for index, val in enumerate(reversed(histogram)):
            if val != 0:
                max = 255 - index
                break
        return (min, max)

    def get_entropy(self, color: Color):
        histogram = self.get_histogram(color)
        entropy = 0
        for i in range(256):
            p = histogram[i]
            if (p != 0):
                entropy += p * log2(p)

        return -entropy

    def get_entropies(self):
        return list(map(lambda color: self.get_entropy(color), Color))

    def get_variance(self, color: Color):
        histogram = self.get_histogram(color)
        mean = self.get_mean(color)
        variance = 0
        for i in range(256):
            variance += histogram[i] * (i - mean) ** 2
        return variance

    def get_pixel_rgb(self, x: int, y: int) -> (int, int, int):
        if not self.valid(x, y):
            return None
        return Pixel(self.pixel(x, y)).get_rgb()

    def get_gray_scaled_image(self) -> QImage:
        width = self.width()
        heigth = self.height()
        gray_scaled = QPixmap(width, heigth).toImage()

        for x in range(width):
            for y in range(heigth):
                pixel = Pixel(self.pixel(x, y))
                gray_value = 0
                for color in RGBColor:
                    value = pixel.get_color(color)
                    gray_value += GrayScaleLUT[color.value][value]

                gray_value = round(gray_value)
                gray_scaled.setPixel(x, y, pixel.set_rgb(gray_value).value)

        return gray_scaled

    def apply_LUT(self, lut: List[int], colors: (bool, bool, bool) = (True, True, True)) -> QImage:
        if (len(lut) != 256):
            print("LUT length must be 256")
            return

        for x in range(self.width()):
            for y in range(self.height()):
                new_pixel = Pixel(self.pixel(x, y))
                for color in RGBColor:
                    if  not colors[color.value]:
                        continue
                    color_value = new_pixel.get_color(color)
                    new_value = lut[color_value]
                    new_pixel = new_pixel.set_color(new_value, color.value)
                self.setPixel(x, y, new_pixel.value)
        return self
