from math import ceil, log2, sqrt, floor, trunc, sin, cos, pi
from typing import List
from PyQt5 import QtCore
from PyQt5 import QtGui
import numpy as np

from PyQt5.QtGui import QColor, QImage, QPixmap
from PyQt5.QtCore import QPoint, QThread, QSize, Signal

from .image_loader import ImageLoader
from .color import Color, RGBColor, GrayScaleLUT
from .pixel import Pixel

from datetime import datetime
from .get_argb import get_argb


class Image(QImage):

    def __init__(self, image: QImage):
        image = image.convertToFormat(QImage.Format_ARGB32)
        super().__init__(image)
        self.then = None
        self.setup_image_data()
        self.load_finished = False

    def setup_image_data(self):
        self.thread = QThread()
        self.loader = ImageLoader(self)
        self.loader.moveToThread(self.thread)

        self.thread.started.connect(self.loader.run)
        self.loader.finished.connect(self.print_time)
        self.loader.finished.connect(self.thread.quit)
        self.loader.finished.connect(self.loader.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.then = datetime.now()

    # This function needs to be separated to allow other elements
    # to connect signals to ImageLoader's slots. Trying to connect
    # the signal after the thread has started is unsafe
    def start_load(self):
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
            if lut is not None and len(lut) != 256:
                print("LUT length must be 256")
                return
        image = QImage(self.copy(0, 0, self.width(), self.height()))

        size = image.width() * image.height()
        pixels = image.constBits().asstring(size * 4)
        def get_qpoint(i): return QPoint(i % self.width(), i // self.width())
        for i in range(size):
            color_bytes = pixels[i * 4:i * 4 + 4]
            color_ints = [int.from_bytes(
                color_bytes[j:j + 1], 'big') for j in range(4)]
            argb_values = get_argb(color_ints)

            new_pixel = int.from_bytes(argb_values, 'big')
            for color in RGBColor:
                lut = luts[color.value]
                if lut is None:
                    continue
                # we add one to the index to account for the alpha channel
                color_value = argb_values[color.value + 1]
                argb_values[color.value + 1] = lut[color_value]
                new_pixel = int.from_bytes(argb_values, 'big')
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

    def rotate(self, angle_deg: float, interpolation_technique):

        def rotation_matrix(angle_rad: float):
            return np.array(
                ((cos(angle_rad), -sin(angle_rad)),
                 (sin(angle_rad), cos(angle_rad)))
            )

        angle_rad = angle_deg * (pi / 180)
        old_top_left = (0, 0)
        old_top_right = (self.width() - 1, 0)
        old_bottom_left = (0, self.height() - 1)
        old_bottom_right = (self.width() - 1, self.height() - 1)

        dt_rotation_matrix = rotation_matrix(angle_rad)
        it_rotation_matrix = rotation_matrix(-angle_rad)

        new_top_left = np.array(
            [floor(value) for value in np.dot(dt_rotation_matrix, old_top_left)])
        new_top_right = np.dot(dt_rotation_matrix, old_top_right)
        new_bottom_left = np.dot(dt_rotation_matrix, old_bottom_left)
        new_bottom_right = np.dot(dt_rotation_matrix, old_bottom_right)

        xs = [new_top_left[0], new_top_right[0],
              new_bottom_left[0], new_bottom_right[0]]
        ys = [new_top_left[1], new_top_right[1],
              new_bottom_left[1], new_bottom_right[1]]

        max_x = max(xs)
        max_y = max(ys)
        min_x = min(xs)
        min_y = min(ys)

        new_width = floor(abs(max_x - min_x))
        new_height = floor(abs(max_y - min_y))

        new_image = QImage(new_width, new_height, self.format())
        for indexXp in range(new_width):
            for indexYp in range(new_height):
                xp, yp = (indexXp + min_x, indexYp + min_y)
                x, y = np.dot(it_rotation_matrix, (xp, yp))

                if (0 <= x < self.width() and 0 <= y < self.height()):
                    new_image.setPixel(
                        indexXp, indexYp, interpolation_technique(self, (x, y)))
                else:
                    # Background pixels are transparent
                    new_image.setPixel(indexXp, indexYp, 0x00000000)
        return new_image

    def scale(self, new_size: (int, int), interpolation_technique):
        (new_width, new_height) = new_size
        new_image = QImage(new_width, new_height, self.format())
        actual_width = self.width()
        actual_height = self.height()
        width_ratio = new_width / actual_width
        height_ratio = new_height / actual_height
        for x in range(new_width):
            actual_x = x / width_ratio
            for y in range(new_height):
                actual_y = y / height_ratio
                new_image.setPixel(x, y, interpolation_technique(
                    self, (actual_x, actual_y)))
        return new_image

    def rotate90_clockwise(self):
        new_image = QImage(self.height(), self.width(), self.format())
        for new_x in range(self.height()):
            for new_y in range(self.width()):
                old_x = new_y
                old_y = self.height() - new_x - 1
                new_image.setPixel(new_x, new_y, self.pixel(old_x, old_y))
        return new_image

    def transpose(self):
        new_image = QImage(self.height(), self.width(), self.format())
        for new_x in range(self.height()):
            for new_y in range(self.width()):
                old_x = new_y
                old_y = new_x
                new_image.setPixel(new_x, new_y, self.pixel(old_x, old_y))
        return new_image

    def rotate_simple(self, angle_deg: float):
        def rotation_matrix(angle_rad: float):
            return np.array(
                ((cos(angle_rad), -sin(angle_rad)),
                 (sin(angle_rad), cos(angle_rad)))
            )

        angle_rad = angle_deg * (pi / 180)
        old_top_left = (0, 0)
        old_top_right = (self.width(), 0)
        old_bottom_left = (0, self.height())
        old_bottom_right = (self.width(), self.height())

        dt_rotation_matrix = rotation_matrix(angle_rad)
        
        new_top_left = np.array(np.dot(dt_rotation_matrix, old_top_left))
        new_top_right = np.dot(dt_rotation_matrix, old_top_right)
        new_bottom_left = np.dot(dt_rotation_matrix, old_bottom_left)
        new_bottom_right = np.dot(dt_rotation_matrix, old_bottom_right)

        xs = [new_top_left[0], new_top_right[0],
              new_bottom_left[0], new_bottom_right[0]]
        ys = [new_top_left[1], new_top_right[1],
              new_bottom_left[1], new_bottom_right[1]]

        max_x = max(xs)
        max_y = max(ys)
        min_x = min(xs)
        min_y = min(ys)

        new_width = ceil(abs(max_x - min_x)) + 1
        new_height = ceil(abs(max_y - min_y)) + 1

        new_image = QImage(new_width, new_height, self.format())
        new_image.fill(QtGui.QColorConstants.Transparent)
        
        for X in range(self.width()):
            for Y in range(self.height()):
                xp, yp = np.dot(dt_rotation_matrix, (X, Y)) - np.array([min_x, min_y])
                Xp, Yp = [trunc(round(val, 8)) for val in [xp, yp]]
                new_image.setPixel(Xp, Yp, self.pixel(X, Y))

        return new_image
