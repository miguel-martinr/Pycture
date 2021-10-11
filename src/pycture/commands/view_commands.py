from io import BytesIO
from typing import List

from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from PIL.ImageQt import ImageQt
from PIL import Image

from .command import Command


class ViewHistogramCommand(Command):
    def __init__(self, parent: QWidget, color: str):
        super().__init__(color, parent)

    def execute(self, main_window: QMainWindow, color: str):
      image, title = self.get_active_image_with_title(main_window)
      if image == None:
          print("Can't create histogram if there is not an active editor")
          return # TODO: Notify the user (can't create histogram if there isn't an active editor)

      if color == "red":
        histogram, mean = image.redHistWMean()
        getBarColor = lambda i: (i/255, 0, 0)
      elif color == "green":
        histogram, mean = image.greenHistWMean()
        getBarColor = lambda i: (0, i/255, 0)
      else:
        histogram, mean = image.blueHistWMean()
        getBarColor = lambda i: (0, 0, i/255)
        
      figure = plt.figure()
      bars = plt.bar(list(range(256)), histogram)
      for index, bar in enumerate(bars):
          bar.set_color(getBarColor(index))

      self.write_mean(mean)
      pixmap = self.save_figure_to_pixmap(figure)
      main_window.addEditor(pixmap, title + "." + color + "-hist")
    
    def get_active_image_with_title(self, main_window: QMainWindow):  
      active_editor = main_window.getActiveEditor()
      if active_editor:
          return (active_editor.widget(), active_editor.windowTitle())
      else:
          return (None, None)

    def write_mean(self, mean: float):
        plt.axvline(mean)
        plt.title(f"Mean: {mean:.2f}")

    def save_figure_to_pixmap(self, figure) -> QPixmap:
        buffer = BytesIO()
        figure.savefig(buffer)
        return QPixmap.fromImage(ImageQt(Image.open(buffer)))

class ViewRedHistogram(ViewHistogramCommand):
  def __init__(self, parent: QWidget):
      super().__init__(parent, "Red")
  
  def execute(self, main_window: QMainWindow):
      return super().execute(main_window, "red")

class ViewGreenHistogram(ViewHistogramCommand):
  def __init__(self, parent: QWidget):
      super().__init__(parent, "Green")
  
  def execute(self, main_window: QMainWindow):
      return super().execute(main_window, "green")

class ViewBlueHistogram(ViewHistogramCommand):
  def __init__(self, parent: QWidget):
      super().__init__(parent, "Blue")
  
  def execute(self, main_window: QMainWindow):
      return super().execute(main_window, "blue")

