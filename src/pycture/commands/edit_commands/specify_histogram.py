from typing import List

from PyQt5.QtWidgets import QWidget, QMainWindow

from ..command import Command
from pycture.dialogs import HistogramSpecificationDialog
from pycture.editor.image import RGBColor


class SpecifyHistogram(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Specify histogram")
        self.main_window = None

    def execute(self, main_window: QMainWindow):
        self.main_window = main_window
        dialog = HistogramSpecificationDialog(
            main_window, main_window.get_editor_list())
        dialog.editors_selected.connect(self.specify_histogram)
        dialog.show()

    def specify_histogram(self, base: str, sample: str,
                          rgb: (bool, bool, bool)):
        base_image = self.main_window.get_editor(base).get_image()
        sample_image = self.main_window.get_editor(sample).get_image()

        luts = [list(range(256)) for x in range(3)]
        for color in RGBColor:
            if not rgb[color.value]:
                continue
            lut = luts[color.value]
            base_histogram = base_image.get_cumulative_histogram(color)
            sample_histogram = sample_image.get_cumulative_histogram(color)
            self.setup_lut(lut, base_histogram, sample_histogram)
        new_image = base_image.apply_LUTs(luts)

        self.main_window.add_editor(new_image, base + "(ModHist)")

    def setup_lut(self, lut: List[int], base: List[float], sample: List[float]):
        sample_index = 0
        for index, val in enumerate(base):
            while (sample_index < 255 and base[index] > sample[sample_index]):
                sample_index += 1
            if (sample_index < 255 and sample[sample_index] - base[index] >
                base[index] - sample[sample_index]):
                sample_index += 1
            lut[index] = sample_index