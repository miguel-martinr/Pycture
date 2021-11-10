from PyQt5.QtCore import QObject, Signal
from PyQt5.QtGui import QImage
from .color import Color, GrayScaleLUT
import sys


class ImageLoader(QObject):
    finished = Signal()

    def __init__(self, image):
        super().__init__()
        self.image = image

    def run(self):

        image: QImage = self.image
        image.histograms = [[0] * 256, [0] * 256, [0] * 256, [0] * 256]
        image.ranges = [[255, 0], [255, 0], [255, 0], [255, 0]]
     
        size = image.width() * image.height()

        pixels = image.constBits().asstring(size * 4)
  
        if sys.byteorder == 'little':
            get_rgb = lambda bgra: (bgra[2], bgra[1], bgra[0])
        else:
            get_rgb = lambda argb: (argb[1], argb[2], argb[3])
              
        for i in range(size):
            i_ = i * 4
            
            color_bytes = pixels[i_:i_+3]
            color_ints = [int.from_bytes(color_bytes[j:j+1], 'big') for j in range(3)]

            gray_value = 0
            rgb_values = get_rgb(color_ints)

            for i, value in enumerate(rgb_values):
                
                image.histograms[i][value] += 1

                gray_value += GrayScaleLUT[i][value]
            gray_value = round(gray_value)
            image.histograms[Color.Gray.value][gray_value] += 1
    
        
        image.histograms = list(map(lambda histogram:
                                    list(
                                        map(lambda x: x / size, histogram)),
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
