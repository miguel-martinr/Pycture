from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPixmap

class Image(QLabel):
    def __init__(self, parent: QWidget, image: QPixmap):
        super().__init__(parent)
        self.setPixmap(image)
        self.setup_histogram_data()
        
    def setup_histogram_data(self) -> [float]:
        image = self.pixmap().toImage()
        histograms = [[0] * 256] * 3
        self.means = [0] * 3
        for x in range(image.width()):
          for y in range(image.height()):
            pixel = image.pixel(x, y)
            get_value = [get_red_value, get_green_value, get_blue_value]
            for i in [0, 1, 2]:
                value = get_value[i](pixel)
                histograms[i][value] += 1
                self.means[i] += value
        total_pixels = image.width() * image.height()
        self.histograms =  list(map(
            lambda histogram: list(map(lambda x: x / total_pixels, histogram))
        ))
        self.means = list(map(lambda mean: mean /total_pixels))

    def get_red_value(pixel):
        return (pixel & 0x00ff0000) >> 16
    
    def get_green_value(pixel):
        return (pixel & 0x0000ff00) >> 8

    def get_blue_value(pixel):
        return pixel & 0x000000ff 

