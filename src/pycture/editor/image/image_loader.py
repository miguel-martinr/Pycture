from PyQt5.QtCore import QObject, Signal
from PyQt5.QtGui import QImage
from .color import Color, GrayScaleLUT
from .get_argb import get_argb


class ImageLoader(QObject):
    finished = Signal()
    progress = Signal(int) # number between 0 and 100

    def __init__(self, image):
        super().__init__()
        self.image = image
        self.current_progress = 0

    def run(self):
        image: QImage = self.image
        image.histograms = [[0] * 256, [0] * 256, [0] * 256, [0] * 256]
        image.ranges = [[255, 0], [255, 0], [255, 0], [255, 0]]

        size = image.width() * image.height()
        non_transparent_size = size
        pixels = image.constBits().asstring(size * 4)
  
        for i in range(size):
            progress_percentage = (i + 1) * 100 / size
            if progress_percentage > self.current_progress:
                self.current_progress = round(progress_percentage)
                self.progress.emit(self.current_progress)
            color_bytes = pixels[i * 4:i * 4 + 4]
            color_ints = [int.from_bytes(
                color_bytes[j:j + 1], 'big') for j in range(4)
            ]
            gray_value = 0
            argb_values = get_argb(color_ints)
            if argb_values[0] == 0:
                non_transparent_size -= 1
                continue # Don't count transparent pixels
            rgb_values = argb_values[1:]

            for i, value in enumerate(rgb_values):
                image.histograms[i][value] += 1
                gray_value += GrayScaleLUT[i][value]

            gray_value = round(gray_value)
            image.histograms[Color.Gray.value][gray_value] += 1

        image.histograms = list(map(lambda histogram:
            list(map(lambda x: x / non_transparent_size, histogram)),
            image.histograms
        ))
        self.load_means()
        image.load_finished = True

        self.finished.emit()

    def load_means(self):
        image = self.image
        image.means = [self.calculate_mean(hist) for hist in image.histograms]

    def calculate_mean(self, normalized_histogram):
        mean = sum([normalized_histogram[i] *
                    i for i in range(len(normalized_histogram))])
        return mean
