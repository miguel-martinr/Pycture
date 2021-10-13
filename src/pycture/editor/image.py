from typing import List
from enum import Enum

from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPixmap

class Color(Enum):
    Red = 0
    Green = 1
    Blue = 2
 
    
GrayScale = {
    "NTSC" : [0.299, 0.587, 0.114],
    "Pal" : [0.222, 0.707, 0.071]
}
class Image(QLabel):
    def __init__(self, parent: QWidget, image: QPixmap):
        super().__init__(parent)
        self.setPixmap(image)
        self.setup_histogram_data()
        
    def setup_histogram_data(self) -> List[float]:
        image = self.pixmap().toImage()
        histograms = [[0] * 256, [0] * 256, [0] * 256, [0] * 256]
        means = [0] * 4
        for x in range(image.width()):
          for y in range(image.height()):
            gray_value = 0
            pixel = image.pixel(x, y)
            get_value = [self.get_red_value, self.get_green_value, self.get_blue_value]
            for color in Color:
                value = get_value[color.value](pixel)
                histograms[color.value][value] += 1
                means[color.value] += value
                gray_value += value * GrayScale["NTSC"][color.value] # PAL available
            gray_value = int(gray_value)  # int(gray_value) or a different rounding?
            histograms[3][gray_value] += 1
            means[3] += gray_value   

        total_pixels = image.width() * image.height()
        self.histograms = list(map(lambda histogram:
            list(map(lambda x: x / total_pixels, histogram)),
            histograms
        ))
        self.means = list(map(lambda mean: mean / total_pixels, means))
        
          

    def get_red_value(self, pixel):
        return (pixel & 0x00ff0000) >> 16
    
    def get_green_value(self, pixel):
        return (pixel & 0x0000ff00) >> 8

    def get_blue_value(self, pixel):
        return pixel & 0x000000ff 

    def get_histogram(self, color: Color):
        if (color == 3): # Gray scale temp fix
          return self.histograms[3]
        return self.histograms[color.value]

    def get_gray_scaled_image(self, system = GrayScale["NTSC"]):
        image = self.pixmap().toImage()
        width = image.width()
        heigth = image.height()

        gray_scaled = QPixmap(width, heigth).toImage()

        for x in range(width):
          for y in range(heigth):
              color_value = image.pixel(x, y)
              red_comp = self.get_red_value(color_value) * system[0]
              green_comp = self.get_green_value(color_value) * system[1]
              blue_comp = self.get_blue_value(color_value) * system[2]
              
              gray_value = int(red_comp + green_comp + blue_comp)
              gray_value = 0x000000ff & gray_value
              for i in [0, 1]:
                  gray_value = gray_value | (gray_value << 8)

              
              # Alpha correction
              gray_value = gray_value | (color_value & 0xff000000)
              gray_scaled.setPixel(x, y, gray_value)
        return gray_scaled 
              


    def get_mean(self, color: Color):
      if (color == 3): # Gray scale temp fix
        return self.means[3]
      return self.means[color.value]


