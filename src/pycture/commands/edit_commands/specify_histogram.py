from PyQt5.QtWidgets import QWidget, QMainWindow

from ..command import Command
from pycture.dialogs import HistogramSpecificationDialog

class SpecifyHistogram(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Specify histogram")

    def execute(self, main_window: QMainWindow):
        image, title = self.get_active_image_and_title(main_window)

        HistogramSpecificationDialog(main_window)
