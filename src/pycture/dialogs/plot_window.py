from PyQt5.QtWidgets import QVBoxLayout, QWidget 
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from pycture.css import PLOT_TOOLBAR_CSS

class PlotWindow(QWidget):
    def __init__(self, parent: QWidget, figure: Figure, title: str, window_type: Qt.WindowType = Qt.WindowType.Window):
        super().__init__(parent)
        self.figure = figure
        self.setWindowTitle(title)
        self.layout = QVBoxLayout(self)
        plot = FigureCanvasQTAgg(figure)
        toolbar = NavigationToolbar2QT(plot, self)
        toolbar.setStyleSheet(PLOT_TOOLBAR_CSS)
        self.layout.addWidget(toolbar)
        self.layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.layout.addWidget(plot)
        self.setParent(parent, window_type)
        self.setMinimumWidth(300)
        self.show()

    def destroy(self, a, b):
        plt.close(self.figure)
        super().destroy(a, b)
