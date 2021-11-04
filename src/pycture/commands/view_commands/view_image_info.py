from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel
from PyQt5.QtCore import Qt

from ..command import Command
from pycture.dialogs import InformationWindow
from pycture.editor.image import Color


class ViewImageInfo(Command):
    def __init__(self, parent: QWidget, info_name: str):
        super().__init__(parent, info_name)

    def execute(self, main_window: QMainWindow):
        image, image_name = self.get_active_image_and_title(main_window)
        if image is None:
            return

        
        info_name = self.text()
        title = image_name + " - " + info_name
        InformationWindow(main_window, title, self.get_information(image))

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
        columns = active_image.width()
        rows = active_image.height()
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
