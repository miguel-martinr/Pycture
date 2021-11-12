from PyQt5.QtWidgets import QWidget, QMainWindow

from typing import List, Tuple
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from pycture.dialogs import SegmentsInput, PlotWindow
from ..command import Command


class TransformByLinearSegments(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "By linear segments")

    def execute(self, main_window: QMainWindow):
        image, _ = self.get_active_image_and_title(main_window)
        if image is None:
            return

        dialog = SegmentsInput(main_window)
        dialog.previewed.connect(lambda points:
            self.preview_transformation(main_window, points)
        )
        dialog.applied.connect(lambda points, options:
            self.apply_transformation(main_window, points, options)
        )

    def preview_transformation(self, main_window: QMainWindow, points: List):
        plt.style.use('dark_background')
        title = "Linear transformation"
        figure = plt.figure()
        self.plot_changes(points)
        self.plot_unchanged_areas(points)

        plt.xlabel("Vin")
        plt.ylabel("Vout")
        plt.title(title)
        plt.xlim(0, 255)
        plt.ylim(0, 255)
        PlotWindow(main_window, FigureCanvasQTAgg(figure), title)
    
    def plot_changes(self, points: List):
        x = list(map(lambda point: point[0], points))
        y = list(map(lambda point: point[1], points))
        plt.plot(x, y)
    
    def plot_unchanged_areas(self, points: List):
        if points[0][0] > 1:
            x = [0, points[0][0] - 1]
            y = x
            plt.plot(x, y)
        if points[-1][0] < 254:
            x = [points[-1][0] + 1, 255]
            y = x
            plt.plot(x, y)

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

    def get_LUT(self, points: List):
        lut = list(range(256))
        point_index = 1
        line_equation = self.get_equation(points[0], points[1])
        for x in range(points[0][0], points[-1][0] + 1):
            if x > points[point_index][0]:
                line_equation = self.get_equation(points[point_index], points[point_index + 1])
                point_index += 1
            lut[x] = round(line_equation(x))
        return lut

    def get_equation(self, point1: (int, int), point2: (int, int)) -> Tuple:
        slope = (point2[1] - point1[1]) / (point2[0] - point1[0])
        intercept = point1[1] - slope * point1[0]
        return (lambda x: slope * x + intercept)



