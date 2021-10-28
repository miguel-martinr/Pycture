from typing import List, Tuple
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog, QWidget, QMainWindow
from matplotlib import pyplot as plt

from pycture.dialogs.input_dialogs import SegmentsInput
from pycture.editor import Editor
from pycture.editor.image import Color, Image

from .command import Command
from ..dialogs.notification import Notification


class EditBrightnessCommand(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Brightness")

    def execute(self, main_window: QMainWindow):
        print("Edits brightness")


class ToGrayScale(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Gray scale (NTSC)")

    def execute(self, main_window: QMainWindow):
        image = self.get_active_image(main_window)
        title = self.get_active_title(main_window)
        if image is None:
            notification = Notification("There isn't an active editor!").exec()
            return
        if not image.load_finished:
            notification = Notification(
                "The image is still loading. Please wait a bit").exec()
            return

        gray_scaled_image = image.get_gray_scaled_image()
        main_window.add_editor(QPixmap.fromImage(
            gray_scaled_image), title + "(GrayScaled)")


class transform_by_linear_segments(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "By linear segments")

    def get_num_of_segments(self, main_window: QMainWindow) -> QWidget:
        dialog = QInputDialog(main_window)
        dialog.setInputMode(QInputDialog.InputMode.IntInput)
        dialog.setIntMinimum(1)
        dialog.setIntMaximum(5)
        dialog.setWindowTitle("Linear segments transformation")
        dialog.setLabelText("Number of segments:")
        dialog.resize(300, 300)
        ok = dialog.exec()
        num_of_segments = dialog.intValue()
        return [num_of_segments, ok]

    def get_ecuation(self, segment: List[int]) -> Tuple:
        s = segment
        m = (s[1][1] - s[0][1]) / (s[1][0] - s[0][0])
        n = s[0][1] - m * s[0][0]
        return (lambda x: m * x + n)

    def get_LUT(self, segments: List):
        lut = list(range(256))
        num_of_segments = len(segments)
        ecuations = list(map(self.get_ecuation, segments))
        for i in range(256):
            j = 0
            s = segments[j]
            while (j < num_of_segments):
                s = segments[j]
                if (s[0][0] <= i <= s[1][0]):
                    break
                j += 1  # :(

            if (j < num_of_segments):
                ecuation = ecuations[j]
                lut[i] = round(ecuation(i))
        return lut

    def preview_transformation(self, points: List):
        x = []
        y = []
        for p in points:
            x.append(p[0])
            y.append(p[1])
        plt.clf()
        plt.plot(x, y)
        plt.xlabel("Vin")
        plt.ylabel("Vout")
        plt.title("Linear transformation")
        plt.show()

    def apply_transformation(self, main_window: QMainWindow, segments: List, opts: List[Color]):
        lut = self.get_LUT(segments)
        active_img = self.get_active_image(main_window)
        title = self.get_active_title(main_window)
        
        transformed_img = active_img.apply_LUT(lut, opts)  # temp
        main_window.add_editor(QPixmap.fromImage(
            transformed_img), title + "-LT")

    def execute(self, main_window: QMainWindow):
        active_image = self.get_active_image(main_window)
        if active_image is None:
            notification = Notification("There isn't an active editor!").exec()
            return
        if not active_image.load_finished:
            notification = Notification(
                "The image is still loading. Please wait a bit").exec()
            return

        dialog = SegmentsInput(main_window)
        dialog.previewed.connect(
            lambda s: self.preview_transformation(dialog.get_points()))
        dialog.applied.connect(
            lambda s: self.apply_transformation(
                main_window, s, dialog.get_color_opts()))
