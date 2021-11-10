from PyQt5.QtCore import QObject, Signal
from .color import Color, RGBColor, GrayScaleLUT
from .pixel import Pixel


class ImageLoader(QObject):
    finished = Signal()

    def __init__(self, image):
        super().__init__()
        self.image = image

    def run(self):
        image = self.image
        image.histograms = [[0] * 256, [0] * 256, [0] * 256, [0] * 256]
        image.ranges = [[255, 0], [255, 0], [255, 0], [255, 0]]
        # image.means = [0] * 4
        
        
        for x in range(image.width()):
            for y in range(image.height()):
                gray_value = 0
                pixel = Pixel(image.pixel(x, y))
                for color in RGBColor:
                    value = pixel.get_color(color)
                    image.histograms[color.value][value] += 1
                    # image.means[color.value] += value
                    gray_value += GrayScaleLUT[color.value][value]

                gray_value = round(gray_value)
                image.histograms[Color.Gray.value][gray_value] += 1
                # image.means[Color.Gray.value] += gray_value

        total_pixels = image.width() * image.height()
        image.histograms = list(map(lambda histogram:
                                    list(
                                        map(lambda x: x / total_pixels, histogram)),
                                    image.histograms
                                    ))
        self.load_means()
        image.load_finished = True
        
        self.finished.emit()

    def load_means(self):
        image = self.image
        image.means = [self.calculate_mean(hist) for hist in image.histograms]



    def calculate_mean(self, normalized_histogram):
        mean = sum([normalized_histogram[i] * i for i in range(len(normalized_histogram))])
        return mean
