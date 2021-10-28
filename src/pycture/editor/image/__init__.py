from functools import reduce
from math import log2, sqrt
from typing import List, Tuple
from PIL.ImageQt import QImage

from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPixmap, QMouseEvent, QKeyEvent, QGuiApplication
from PyQt5.QtCore import Qt, QCoreApplication, QThread, Signal

from ...events import UpdateMousePositionEvent
from .image_loader import ImageLoader
from .color import Color, GrayScaleLUT


class Image(QLabel):
    mouse_position_updated = Signal(int, int, int, int, int)
    new_selection = Signal(QPixmap)

    def __init__(self, parent: QWidget, image: QPixmap):
        super().__init__(parent)
        self.setPixmap(image)
        self.setup_image_data()

        self.setMouseTracking(True)
        self.setFixedHeight(image.height())
        self.setFixedWidth(image.width())
        self.press_pos = None
        self.load_finished = False

    def get_width(self):
        return self.pixmap().width()

    def get_height(self):
        return self.pixmap().height()

    def get_brightness(self):
        return list(map(lambda color: self.get_mean(color), Color))

    def get_contrast(self):
        return list(map(lambda color: self.get_sd(color), Color))

    def get_info(self):
        return self.info

    def setup_image_data(self):
        self.thread = QThread()
        self.worker = ImageLoader(self)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def get_red_value(self, pixel):
        return (pixel & 0x00ff0000) >> 16

    def get_green_value(self, pixel):
        return (pixel & 0x0000ff00) >> 8

    def get_blue_value(self, pixel):
        return pixel & 0x000000ff

    def get_pixel_rgb(self, x, y):
        image = self.pixmap().toImage()
        if not image.valid(x, y):
            return None
        pixel_val = image.pixel(x, y)
        red_val = self.get_red_value(pixel_val)
        green_val = self.get_green_value(pixel_val)
        blue_val = self.get_blue_value(pixel_val)
        return (red_val, green_val, blue_val)

    def set_red_value(self, red_value: int, pixel_value: int) -> int:
        red_value &= 0x000000ff
        red_value <<= 16
        return (red_value | (pixel_value & 0xff00ffff))

    def set_green_value(self, green_value: int, pixel_value: int) -> int:
        green_value &= 0x000000ff
        green_value <<= 8
        return (green_value | (pixel_value & 0xffff00ff))

    def set_blue_value(self, blue_value: int, pixel_value: int) -> int:
        blue_value &= 0x000000ff
        return (blue_value | (pixel_value & 0xffffff00))

    def set_gray_value(self, gray_value: int, pixel_value: int) -> int:
        gray_value &= 0x000000ff
        for _ in range(2):
            gray_value = gray_value | (gray_value << 8)
        return gray_value | (pixel_value & 0xff000000)

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
        def prob(i): return histogram[i] / self.get_width() * self.get_height()
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

    def get_gray_scaled_image(self) -> QImage:
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
                gray_scaled.setPixel(x, y, self.set_gray_value(gray_value, color_value))

        return gray_scaled

    def mouseMoveEvent(self, event: QMouseEvent):
        pos = (event.x(), event.y())
        rgb = self.get_pixel_rgb(pos[0], pos[1])
        if rgb is not None:
            self.mouse_position_updated.emit(*pos, *rgb)

    def mousePressEvent(self, event: QMouseEvent):
        if (event.button() == Qt.LeftButton and
                QGuiApplication.keyboardModifiers() == Qt.ControlModifier):
            self.press_pos = (event.x(), event.y())
        else:
            self.press_pos = None
        event.ignore()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if (event.button() != Qt.LeftButton or not self.press_pos or
                QGuiApplication.keyboardModifiers() != Qt.ControlModifier):
            return
        x_values = sorted([event.x(), self.press_pos[0]])
        y_values = sorted([event.y(), self.press_pos[1]])
        new_image = self.pixmap().copy(
            x_values[0],
            y_values[0],
            x_values[1] - x_values[0],
            y_values[1] - y_values[0]
        )
        self.new_selection.emit(new_image)
        event.ignore()

    def apply_LUT(self, lut: List[int], colors: Tuple[Color]) -> QImage:
        if (len(lut) != 256):
            print("LUT length must be 256")
            return

        get_value = [self.get_red_value,
                     self.get_green_value, self.get_blue_value,
                     self.get_blue_value]  # Gray

        set_value = [self.set_red_value,
                     self.set_green_value, self.set_blue_value,
                     self.set_gray_value]

        img = self.pixmap().toImage()
        for x in range(img.width()):
            for y in range(img.height()):
                new_pixel = img.pixel(x, y)
                for color in colors:
                    color_value = get_value[color.value](new_pixel)
                    new_value = lut[color_value]
                    new_pixel = set_value[color.value](new_value, new_pixel)
                img.setPixel(x, y, new_pixel)
        return img
