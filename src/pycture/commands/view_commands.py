from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QValueAxis
from PyQt5.QtCore import Qt

from .command import Command

class ViewHistogramCommand(Command):
    def __init__(self, parent: QWidget):
        super().__init__("Histogram", parent)

    def execute(self, main_window: QMainWindow):
        activeEditor = main_window.getActiveEditor()
        if activeEditor == None:
            return # TODO: Notify the user (can't create histogram if there isn't an active editor)
        histogram = activeEditor.widget().histogram

        chart = QChart()
        chart.legend().hide()
        chart.setTitle("Histogram")

        bars = QBarSet("")
        for val in histogram[:50]:
            bars.append(val)
        series = QBarSeries()
        series.append(bars)
        chart.addSeries(series)

        x_axis = QValueAxis()
        x_axis.setRange(0, 255)
        x_axis.setTickCount(2)
        x_axis.setLabelFormat("%d")
        chart.addAxis(x_axis, Qt.AlignmentFlag.AlignBottom)

        y_axis = QValueAxis()
        # y_axis.setRange(0, 1)
        chart.addAxis(y_axis, Qt.AlignmentFlag.AlignLeft)

        chart_view = QChartView(chart)
        main_window.addEditor(chart_view.grab(), main_window.activeEditor + ".hist")
