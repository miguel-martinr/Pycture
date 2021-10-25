from PyQt5.QtCore import QObject, Signal
from PyQt5.QtWidgets import QLabel

from .color import Color, GrayScaleLUT


class ImageLoader(QObject):
    finished = Signal()

    def __init__(self, image: QLabel):
        super().__init__()
        self.image = image

    def run(self):
        image = self.image
        pixmap = image.pixmap().toImage()
        image.histograms = [[0] * 256, [0] * 256, [0] * 256, [0] * 256]
        image.ranges = [[255, 0], [255, 0], [255, 0], [255, 0]]
        image.means = [0] * 4
        for x in range(pixmap.width()):
            for y in range(pixmap.height()):
                gray_value = 0
                pixel = pixmap.pixel(x, y)
                get_value = [image.get_red_value,
                             image.get_green_value, image.get_blue_value]
                for color in [Color.Red, Color.Green, Color.Blue]:
                    value = get_value[color.value](pixel)
                    image.histograms[color.value][value] += 1
                    image.means[color.value] += value
                    gray_value += GrayScaleLUT[color.value][value]

                gray_value = round(gray_value)
                image.histograms[Color.Gray.value][gray_value] += 1
                image.means[Color.Gray.value] += gray_value

        total_pixels = pixmap.width() * pixmap.height()
        image.histograms = list(map(lambda histogram:
                                    list(
                                        map(lambda x: x / total_pixels, histogram)),
                                    image.histograms
                                    ))
        image.means = list(map(lambda mean: mean / total_pixels, image.means))
        self.finished.emit()
        image.load_finished = True
