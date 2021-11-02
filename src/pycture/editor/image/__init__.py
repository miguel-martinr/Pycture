from math import log2, sqrt
from typing import List, Tuple

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, QSize

from .image_loader import ImageLoader
from .color import Color, GrayScaleLUT

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
        def prob(i): return histogram[i] / self.width() * self.height()
        entropy = 0
        for i in range(256):
            p = prob(i)
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

    def get_color_from_pixel(self, pixel: int, color: Color) -> int:
        if color == Color.Red:
            return (pixel & 0x00ff0000) >> 16
        elif color == Color.Green:
            return (pixel & 0x0000ff00) >> 8
        else:
            return pixel & 0x000000ff

    def get_pixel_rgb(self, x: int, y: int) -> (int, int, int):
        if not self.valid(x, y):
            return None
        pixel_val = self.pixel(x, y)
        red_val = self.get_color_from_pixel(pixel_val, Color.Red)
        green_val = self.get_color_from_pixel(pixel_val, Color.Green)
        blue_val = self.get_color_from_pixel(pixel_val, Color.Blue)
        return (red_val, green_val, blue_val)

    def set_green_value(self, green_value: int, pixel_value: int) -> int:
        green_value = (green_value & 0x000000ff) << 8
        return (green_value | (pixel_value & 0xffff00ff))

    def set_blue_value(self, blue_value: int, pixel_value: int) -> int:
        blue_value &= 0x000000ff
        return (blue_value | (pixel_value & 0xffffff00))

    def set_red_value(self, red_value: int, pixel_value: int) -> int:
        red_value = (red_value & 0x000000ff) << 16
        return (red_value | (pixel_value & 0xff00ffff))

    def set_green_value(self, green_value: int, pixel_value: int) -> int:
        green_value = (green_value & 0x000000ff) << 8
        return (green_value | (pixel_value & 0xffff00ff))

    def set_blue_value(self, blue_value: int, pixel_value: int) -> int:
        blue_value &= 0x000000ff
        return (blue_value | (pixel_value & 0xffffff00))

    def get_gray_pixel(self, gray_value: int, alpha: int = 0) -> int:
        gray_value &= 0x000000ff
        for _ in range(2):
            gray_value = gray_value | (gray_value << 8)
        return (gray_value | (alpha & 0xff000000))
    
    def get_selection(self, x: int, y: int, width: int, height: int) -> QImage:
        return self.copy(x, y, width, height)

    def get_gray_scaled_image(self) -> QImage:
        width = self.width()
        heigth = self.height()
        gray_scaled = QPixmap(width, heigth).toImage()

        for x in range(width):
            for y in range(heigth):
                pixel = self.pixel(x, y)
                gray_value = 0
                for color in (Color.Red, Color.Green, Color.Blue):
                    value = self.get_color_from_pixel(pixel, color)
                    gray_value += GrayScaleLUT[color.value][value]

                gray_value = round(gray_value)
                gray_scaled.setPixel(x, y, self.get_gray_pixel(gray_value, pixel))

        return gray_scaled

    # Color.Gray shouldn't be passed as a color since it's represented as the
    # (Color.Red ,Color.Green, Color.Blue) tuple
    def apply_LUT(self, lut: List[int], colors: Tuple[Color] = (
            Color.Red, Color.Green, Color.Blue)) -> QImage:

        if (len(lut) != 256):
            print("LUT length must be 256")
            return

        set_value = [self.set_red_value,
                     self.set_green_value, self.set_blue_value]

        for x in range(self.width()):
            for y in range(self.height()):
                new_pixel = self.pixel(x, y)
                for color in colors:
                    color_value = self.get_color_from_pixel(new_pixel, color)
                    new_value = lut[color_value]
                    new_pixel = set_value[color.value](new_value, new_pixel)
                self.setPixel(x, y, new_pixel)
        return self
