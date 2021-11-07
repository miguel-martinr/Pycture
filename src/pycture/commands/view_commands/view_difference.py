from PyQt5 import QtWidgets

from pycture.dialogs.difference_dialog import DifferenceDialog
from ..command import Command


class ViewDifference(Command):
    def __init__(self, parent: QtWidgets):
        super().__init__(parent, "Difference")

    def execute(self, main_window: QtWidgets.QMainWindow):
        active_image, title = self.get_active_image_and_title(main_window)
        if (not active_image):
            return

        # Dialog
        dialog = DifferenceDialog(main_window, ["TestA", "TestB"])
        return super().execute(main_window)
