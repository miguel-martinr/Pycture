from PyQt5 import QtWidgets
from ..command import Command

class ViewDifference(Command):
    def __init__(self, parent: QtWidgets):
        super().__init__(parent, "Difference")

    def execute(self, main_window: QtWidgets.QMainWindow):
        return super().execute(main_window)