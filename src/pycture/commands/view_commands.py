from io import BytesIO
from typing import List

from PyQt5.QtWidgets import QPushButton, QWidget, QMainWindow, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from PIL.ImageQt import ImageQt
from PIL import Image

from .command import Command
from ..dialogs import Notification
from ..editor.image import Color


class ViewHistogramCommand(Command):
    def __init__(self, parent: QWidget, color: str):
        super().__init__(parent, color)

    def execute(self, main_window: QMainWindow):
        image = self.get_active_image(main_window)
        title = self.get_active_title(main_window)
        if image is None:
            notification = Notification(main_window, "There isn't an active editor!").exec()
            return
        if not image.load_finished:
            notification = Notification(main_window,
                "The image is still loading. Please wait a bit").exec()
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
        image = self.get_active_image(main_window)
        if image is None:
            Notification(main_window, "There isn't an active editor!").exec()
            return
        if not image.load_finished:
            notification = Notification(main_window,
                "The image is still loading. Please wait a bit").exec()
            return
        self.container.setParent(main_window, Qt.WindowType.Window)
        img_name = self.get_active_title(main_window)
        info_name = self.container.windowTitle()
        self.container.setWindowTitle(img_name + " - " + info_name)
        self.text_label.setFixedSize(300, 100)
        self.text_label.setText(self.get_information(image))
        self.container.show()

    def get_information(self, active_image) -> str:
        pass


class ViewImageBrightness(ViewImageInfo):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Brightness")

    def get_information(self, active_image) -> str:
        brightness = active_image.get_brightness()
        return (f"R: {brightness[0]:.2f}\nG: {brightness[1]:.2f}\n" +
                f"B: {brightness[2]:.2f}\n\nGray: {brightness[3]:.2f}")


class ViewImageSize(ViewImageInfo):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Size")

    def get_information(self, active_image) -> str:
        columns = active_image.get_width()
        rows = active_image.get_height()
        return f"Columns: {columns}\nRows: {rows}"


class ViewImageContrast(ViewImageInfo):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Contrast")

    def get_information(self, active_image) -> str:
        contrast = active_image.get_contrast()
        return (f"R: {contrast[0]:.2f}\nG: {contrast[1]:.2f}\n" +
                f"B: {contrast[2]:.2f}\n\nGray: {contrast[3]:.2f}")


class ViewImageEntropy(ViewImageInfo):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Entropy")

    def get_information(self, active_image) -> str:
        entropies = active_image.get_entropies()
        return (f"R: {entropies[0]:.2f}\nG: {entropies[1]:.2f}\n" +
                f"B: {entropies[2]:.2f}\n\nGray: {entropies[3]:.2f}")


class ViewImageRanges(ViewImageInfo):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Ranges")

    def get_information(self, active_image) -> str:
        ranges = list(map(lambda color: active_image.get_ranges(color), Color))
        return (f"R: {ranges[0]}\nG: {ranges[1]}\n" +
                f"B: {ranges[2]}\n\nGray: {ranges[3]}")
