from PyQt5.QtWidgets import QWidget, QMainWindow

from typing import List, Tuple

from pycture.dialogs import SegmentsInput
from ..command import Command


class TransformByLinearSegments(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "By linear segments")

    def execute(self, main_window: QMainWindow):
        dialog = SegmentsInput(main_window, main_window.get_editor_list())
        dialog.applied.connect(lambda editor, points, options:
            self.apply_transformation(main_window, editor, points, options)
        )
        editor = main_window.get_active_editor_name()
        if editor is not None:
            dialog.set_dropdown_image(editor)

    def apply_transformation(self, main_window: QMainWindow,
        editor: str, segments: List, options: tuple
    ):
        image = main_window.get_editor(editor).get_image()
        if image is None:
            return

        lut = self.get_LUT(segments)

        lut_or_none = lambda condition: lut if condition else None
        transformed_image = image.apply_LUTs((
            lut_or_none(options[0]),
            lut_or_none(options[1]),
            lut_or_none(options[2])
        ))
        main_window.add_editor(transformed_image, editor + "-LT")

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



