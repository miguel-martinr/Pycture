from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtChart import QChart, QChartView

from .command import Command

class ViewHistogramCommand(Command):
    def __init__(self, parent: QWidget):
        super().__init__("Histogram", parent)

    def execute(self, main_window: QMainWindow):
        activeEditor = main_window.getActiveEditor()
        if activeEditor == None:
            return # TODO: Notify the user (can't create histogram if there isn't an active editor)
        chart = QChart()
        chart_view = QChartView(chart)
        main_window.addEditor(chart_view.grab(), main_window.activeEditor)
