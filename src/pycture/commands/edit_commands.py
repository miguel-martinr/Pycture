from typing import List, Tuple
from PIL.ImageQt import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog, QWidget, QMainWindow
from matplotlib import pyplot as plt

from pycture.dialogs.input_dialogs import SegmentsInput
from pycture.editor.image import Image

from .command import Command


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
        if image == None:
            print("Gray scale transformation: No image found")
            return  # TODO: Notify the user properly

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

    def get_ecuation(segment: List[int]) -> Tuple:
        s = segment
        m = (s[1][1] - s[0][1]) / (s[0][1] - s[0][0])
        n = s[0][1] - m * s[0][0]
        return (lambda x: m * x + n)

    def get_LUT(self, segments: List):
        lut = list(range(256))
        num_of_segments = len(segments)
        ecuations = list(map(self.get_ecuation, segments))
        for i in range(256):
            j = 0
            s = segments[j]
            while (j < num_of_segments and not (s[0][0] <= i <= s[1][0])):
                j += 1
                s = segments[j]
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

    def execute(self, main_window: QMainWindow):
        active_image = self.get_active_image(main_window)
        if (not active_image):
            print("No image to transform")  # TODO: Notify user
            return

        dialog = SegmentsInput(main_window)
        dialog.previewed.connect(lambda s: self.preview_transformation(dialog.get_points()))
