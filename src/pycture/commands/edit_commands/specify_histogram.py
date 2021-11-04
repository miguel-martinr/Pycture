from PyQt5.QtWidgets import QWidget, QMainWindow

from ..command import Command
from pycture.dialogs import HistogramSpecificationDialog


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
        new_image = self.main_window.get_editor(base).get_image()
        self.main_window.add_editor(new_image, base + "(ModHist)")
