from io import BytesIO
from typing import List

from PyQt5.QtWidgets import QPushButton, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from PIL.ImageQt import ImageQt
from PIL import Image

from .command import Command
from ..editor.image import Color


class ViewHistogramCommand(Command):
    def __init__(self, parent: QWidget, color: str):
        super().__init__(parent, color)

    def execute(self, main_window: QMainWindow):
        image = self.get_active_image(main_window)
        title = self.get_active_title(main_window)
        if image == None:
            print("Can't create histogram if there is not an active editor")
            # TODO: Notify the user (can't create histogram if there isn't an active editor)
            return

        histogram = self.get_histogram(image)
        mean = self.get_mean(image)

        figure = plt.figure()
        bars = plt.bar(list(range(256)), histogram)
        for index, bar in enumerate(bars):
            bar.set_color(self.get_bar_color(index))

        self.write_mean(mean)
        pixmap = self.save_figure_to_pixmap(figure)
        main_window.add_editor(pixmap, title + "." + self.text() + "-hist")

    def write_mean(self, mean: float):
        plt.axvline(mean)
        plt.title(f"Mean: {mean:.2f}")

    def save_figure_to_pixmap(self, figure) -> QPixmap:
        buffer = BytesIO()
        figure.savefig(buffer)
        return QPixmap.fromImage(ImageQt(Image.open(buffer)))

    def get_bar_color(self, val: int) -> List[float]:
        pass

    def get_histogram(self, image: QLabel) -> List[int]:
        return image.get_histogram(self.color)

    def get_mean(self, image: QLabel) -> float:
        return image.get_mean(self.color)


class ViewRedHistogram(ViewHistogramCommand):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Red")
        self.color = Color.Red

    def get_bar_color(self, val: int) -> List[float]:
        return (val / 255, 0, 0)


class ViewGreenHistogram(ViewHistogramCommand):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Green")
        self.color = Color.Green

    def get_bar_color(self, val: int) -> List[float]:
        return (0, val / 255, 0)


class ViewBlueHistogram(ViewHistogramCommand):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Blue")
        self.color = Color.Blue

    def get_bar_color(self, val: int) -> List[float]:
        return (0, 0, val / 255)


class ViewGrayScaleHistogram(ViewHistogramCommand):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Gray Scale (NTSC)")
        self.color = Color.Gray

    def get_bar_color(self, val: int) -> List[float]:
        # This is made so the values don't reach pure white and can be seen
        val = val / 255 * 200 / 255
        return (val, val, val)


class ViewImageInfo(Command):
    def __init__(self, parent: QWidget, info_name: str):
        super().__init__(parent, info_name)
        self.container = QWidget()
        self.container.setWindowTitle(info_name)
        self.text_label = QLabel(self.container)
        self.text_label.setAlignment(Qt.AlignCenter)

    def execute(self, main_window: QMainWindow):
        self.container.setParent(main_window, Qt.WindowType.Window)
        img_name = self.get_active_title(main_window)
        info_name = self.container.windowTitle()
        self.container.setWindowTitle(img_name + " - " + info_name)
        self.text_label.setFixedSize(300, 100)
        self.container.show()


class ViewImageBrightness(ViewImageInfo):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Brightness")

    def execute(self, main_window: QMainWindow):
        active_image = self.get_active_image(main_window)
        if active_image == None:
            # TODO: Notify the user
            print("Can't view brightness if there is not an active editor")
            return

        brightness = active_image.get_brightness()
        self.text_label.setText(
            f"R: {brightness[0]:.2f}\nG: {brightness[1]:.2f}\nB: {brightness[2]:.2f}\n\nGray: {brightness[3]:.2f}")
        return super().execute(main_window)


class ViewImageSize(ViewImageInfo):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Size")

    def execute(self, main_window: QMainWindow):
        active_image = self.get_active_image(main_window)
        if active_image == None:
            # TODO: Notify the user
            print("Can't view size if there is not an active editor")
            return
        columns = active_image.get_width()
        rows = active_image.get_height()
        self.text_label.setText(f"Columns: {columns}\nRows: {rows}")
        return super().execute(main_window)


class ViewImageContrast(ViewImageInfo):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Contrast")

    def execute(self, main_window: QMainWindow):
        active_image = self.get_active_image(main_window)
        if active_image == None:
            # TODO: Notify the user
            print("Can't view contrast if there is not an active editor")
            return        
        contrast = active_image.get_contrast()
        self.text_label.setText(
            f"R: {contrast[0]:.2f}\nG: {contrast[1]:.2f}\nB: {contrast[2]:.2f}\n\nGray: {contrast[3]:.2f}")
        return super().execute(main_window)
        
class ViewImageEntropy(ViewImageInfo):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Entropy")

    def execute(self, main_window: QMainWindow):
        active_image = self.get_active_image(main_window)
        if active_image == None:
            # TODO: Notify the user
            print("Can't view entropy if there is not an active editor")
            return        
        entropies = active_image.get_entropies()
        self.text_label.setText(
            f"R: {entropies[0]:.2f}\nG: {entropies[1]:.2f}\nB: {entropies[2]:.2f}\n\nGray: {entropies[3]:.2f}")
        return super().execute(main_window)

class ViewImageRanges(ViewImageInfo):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Ranges")

    def execute(self, main_window: QMainWindow):
        active_image = self.get_active_image(main_window)
        if active_image == None:
            # TODO: Notify the user
            print("Can't view ranges if there is not an active editor")
            return        
        ranges = active_image.get_ranges()
        self.text_label.setText(
            f"R: {ranges[0]}\nG: {ranges[1]}\nB: {ranges[2]}\n\nGray: {ranges[3]}")
        return super().execute(main_window)
