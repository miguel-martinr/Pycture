from typing import List
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPixmap

class Image(QLabel):
    def __init__(self, parent: QWidget, image: QPixmap):
        super().__init__(parent)
        self.setPixmap(image)
        self.setup_histogram_data()
        
    def setup_histogram_data(self) -> List[float]:
        image = self.pixmap().toImage()
        histograms = [[0] * 256] * 3
        means = [0] * 3
        for x in range(image.width()):
          for y in range(image.height()):
            pixel = image.pixel(x, y)
            get_value = [self.get_red_value, self.get_green_value, self.get_blue_value]
            for i in [0, 1, 2]:
                value = get_value[i](pixel)
                histograms[i][value] += 1
                means[i] += value
        total_pixels = image.width() * image.height()
        self.histograms = []
        
        # TODO: Error on histogram calculation (histogram[i][x] > total_pixels)(?)
        for h in histograms:
          self.histograms.append(list(map(lambda x: x / total_pixels, h)))


        self.means = list(map(lambda mean: mean /total_pixels, means))

    def get_red_value(self, pixel):
        return (pixel & 0x00ff0000) >> 16
    
    def get_green_value(self, pixel):
        return (pixel & 0x0000ff00) >> 8

    def get_blue_value(self, pixel):
        return pixel & 0x000000ff 

    def redHistWMean(self):
        return (self.histograms[0], self.means[0])

    def greenHistWMean(self):
        return (self.histograms[1], self.means[1])

    def blueHistWMean(self):
        return (self.histograms[2], self.means[2])

