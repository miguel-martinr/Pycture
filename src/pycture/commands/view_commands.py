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
        active_editor = main_window.getActiveEditor()
        if active_editor == None:
            return # TODO: Notify the user (can't create histogram if there isn't an active editor)
        histogram = active_editor.widget().histogram

        figure = plt.figure()
        bars = plt.bar(list(range(256)), histogram)
        for index, bar in enumerate(bars):
            bar.set_color((index / 255, 0, 0))

        mean = active_editor.widget().mean
        plt.axvline(mean)
        plt.title(f"Mean: {mean:.2f}")

        buffer = BytesIO()
        figure.savefig(buffer)
        plt.close()

        main_window.addEditor(
            QPixmap.fromImage(ImageQt(Image.open(buffer))),
            active_editor.windowTitle() + ".hist"
        )
