from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPixmap

class Image(QLabel):
    def __init__(self, parent: QWidget, image: QPixmap):
        super().__init__(parent)
        self.setPixmap(image)
        self.setup_histogram_data()
        
    def setup_histogram_data(self) -> [float]:
        image = self.pixmap().toImage()
        histogram = [0] * 256
        self.mean = 0
        for x in range(image.width()):
          for y in range(image.height()):
            red_value = (0x00ffffff & image.pixel(x, y)) >> 16
            histogram[red_value] += 1
            self.mean += red_value
        total_pixels = image.width() * image.height()
        self.histogram =  list(map(lambda x: x / total_pixels, histogram))
        self.mean /= total_pixels 

