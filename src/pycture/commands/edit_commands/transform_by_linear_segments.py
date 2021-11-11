from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QMainWindow

from typing import List, Tuple
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from pycture.editor.image import Color
from pycture.dialogs import SegmentsInput, PlotWindow
from ..command import Command


class TransformByLinearSegments(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "By linear segments")

    def get_equation(self, segment: List[int]) -> Tuple:
        s = segment
        m = (s[1][1] - s[0][1]) / (s[1][0] - s[0][0])
        n = s[0][1] - m * s[0][0]
        return (lambda x: m * x + n)

    def get_LUT(self, segments: List):
        lut = list(range(256))
        num_of_segments = len(segments)
        equations = list(map(self.get_equation, segments))
        for i in range(256):
            j = 0
            s = segments[j]
            while (j < num_of_segments):
                s = segments[j]
                if (s[0][0] <= i <= s[1][0]):
                    break
                j += 1  # :(

            if (j < num_of_segments):
                equation = equations[j]
                lut[i] = round(equation(i))
        return lut

    def preview_transformation(self, main_window: QMainWindow, points: List):
        x = []
        y = []
        for p in points:
            x.append(p[0])
            y.append(p[1])

        plt.style.use('dark_background')
        title = "Linear transformation"
        figure = plt.figure(title)
        plt.plot(x, y)
        plt.xlabel("Vin")
        plt.ylabel("Vout")
        plt.title(title)
        PlotWindow(main_window, FigureCanvasQTAgg(figure), title)

    def apply_transformation(
            self, main_window: QMainWindow, segments: List, options: tuple):
        image, title = self.get_active_image_and_title(main_window)
        if image is None:
            return

        lut = self.get_LUT(segments)

        def lut_or_none(condition): return lut if condition else None
        luts = (
            lut_or_none(options[0]),
            lut_or_none(options[1]),
            lut_or_none(options[2])
        )
        transformed_image = image.apply_LUTs(luts)
        main_window.add_editor(transformed_image, title + "-LT")

    def execute(self, main_window: QMainWindow):
        image, _ = self.get_active_image_and_title(main_window)
        if image is None:
            return

        dialog = SegmentsInput(main_window)
        dialog.previewed.connect(lambda points:
                                 self.preview_transformation(
                                     main_window, points)
                                 )
        dialog.applied.connect(lambda segments, options:
                               self.apply_transformation(
                                   main_window, segments, options)
                               )
