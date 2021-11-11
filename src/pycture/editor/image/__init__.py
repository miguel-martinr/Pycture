from math import log2, sqrt
from typing import List, Tuple
from functools import reduce

from PyQt5.QtGui import QColor, QImage, QPixmap
from PyQt5.QtCore import QPoint, QThread, QSize

from .image_loader import ImageLoader
from .color import Color, RGBColor, GrayScaleLUT
from .pixel import Pixel

from datetime import datetime
from .get_rgb import get_rgb


class Image(QImage):

    def __init__(self, image: QImage):
        super().__init__(image)
        self.then = None
        self.setup_image_data()
        self.load_finished = False

    def setup_image_data(self):
        self.thread = QThread()
        self.worker = ImageLoader(self)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)

        self.worker.finished.connect(self.print_time)

        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.then = datetime.now()

        self.thread.start()

    def print_time(self):
        delta = datetime.now() - self.then
        print("Loading time: ", delta)

    def get_brightness(self):
        return list(map(lambda color: self.get_mean(color), Color))

    def get_contrast(self):
        return list(map(lambda color: self.get_sd(color), Color))

    def get_histogram(self, color: Color):
        return self.histograms[color.value]

    def get_cumulative_histogram(self, color: Color):
        return self.convert_histogram_to_cumulative(
            self.histograms[color.value])

    def convert_histogram_to_cumulative(
            self, histogram: List[float]) -> List[float]:
        accumulator = 0
        cumulative = []
        for val in histogram:
            accumulator += val
            cumulative.append(accumulator)
        return cumulative

    def get_mean(self, color: Color):
        return self.means[color.value]

    # Standard deviation
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

    def apply_LUTs(self, luts: (List[int], List[int], List[int])) -> QImage:

        for lut in luts:
            if (len(lut) != 256):
                print("LUT length must be 256")
                return
        image = QImage(self.copy(0, 0, self.width(), self.height()))

        size = image.width() * image.height()
        pixels = image.constBits().asstring(size * 4)
        get_qpoint = lambda i: QPoint(i % self.width(), i // self.width())
        for i in range(size):
            i_ = i * 4
            
            color_bytes = pixels[i_:i_+3]
            color_ints = [int.from_bytes(color_bytes[j:j+1], 'big') for j in range(3)]
            rgb_values = get_rgb(color_ints)

            for color in RGBColor:
                lut = luts[color.value]
                if lut is None:
                    continue
                color_value = rgb_values[color.value]
                rgb_values[color.value] = lut[color_value]
                new_pixel = int.from_bytes([255, *rgb_values], 'big')
            image.setPixel(get_qpoint(i), new_pixel)
              
        return image

    def get_difference(self, image_b: QImage):

        if (self.height() != image_b.height()
                or self.width() != image_b.width()):
            print("Image difference: Both images must have the same dimensions")
            return

        result = QImage(self.width(), self.height(), self.format())

        for x in range(self.width()):
            for y in range(self.height()):
                pixel_a = self.pixel(x, y)
                pixel_b = image_b.pixel(x, y)

                rgb_a = pixel_a.to_bytes(4, 'big')[1:]
                rgb_b = pixel_b.to_bytes(4, 'big')[1:]

                new_pixel = 0xff000000  # opacity = 255
                new_pixel |= int.from_bytes(
                    [abs(rgb_a[i] - rgb_b[i]) for i in range(3)], 'big')

                result.setPixel(x, y, new_pixel)

        return result

    def mark_pixels(self, pixels_coordinates: [
                    (int, int)], _marker_color: QColor) -> QImage:
        marked_image = QImage(self.copy())
        marker_color = _marker_color.rgb()

        for x, y in pixels_coordinates:
            if (not (0 <= x < self.width())):
                print("Mark pixels: x out of range")
                return

            if (not (0 <= y < self.height())):
                print("Mark pixels: y out of range")
                return
        
            marked_image.setPixel(x, y, marker_color)

        return marked_image

    def get_pixels_coordinates(self, treshold: int, rgb_plane: Color):
        coordinates = []
        for x in range(self.width()):
            for y in range(self.height()):
                pixel = Pixel(self.pixel(x, y))
                if pixel.get_color(rgb_plane) > treshold:
                    coordinates.append((x, y))
        return coordinates
