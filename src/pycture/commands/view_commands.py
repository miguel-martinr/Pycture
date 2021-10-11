from io import BytesIO

from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from PIL.ImageQt import ImageQt
from PIL import Image

from .command import Command

class ViewHistogramCommand(Command):
    def __init__(self, parent: QWidget):
        super().__init__("Histogram", parent)

    def execute(self, main_window: QMainWindow):
        image, title = get_active_image_with_title(main_window)
        if image == None:
            return # TODO: Notify the user (can't create histogram if there isn't an active editor)

        histogram = image.histogram
        figure = plt.figure()
        bars = plt.bar(list(range(256)), histogram)
        for index, bar in enumerate(bars):
            bar.set_color((index / 255, 0, 0))

        write_mean(image.mean)
        pixmap = save_figure_to_pixmap(figure)
        main_window.addEditor(pixmap, title + ".hist")
    
    def get_active_image(main_window: QMainWindow):  
        active_editor = main_window.getActiveEditor()
        if active_editor:
            return (active_editor.widget(), active_editor.windowTitle())

    def write_mean(mean: float):
        plt.axvline(mean)
        plt.title(f"Mean: {mean:.2f}")

    def save_figure_to_pixmap(figure) -> QPixmap:
        buffer = BytesIO()
        figure.savefig(buffer)
        return QPixmap.fromImage(ImageQt(Image.open(buffer)))
