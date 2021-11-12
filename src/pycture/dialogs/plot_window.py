from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT


class PlotWindow(QWidget):
    def __init__(self, parent: QWidget, plot: FigureCanvasQTAgg, title: str):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.layout = QVBoxLayout(self)
        toolbar = NavigationToolbar2QT(plot, self)
        toolbar.setStyleSheet("background-color: white;")
        self.layout.addWidget(toolbar)
        self.layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.layout.addWidget(plot)
        self.setParent(parent, Qt.WindowType.Window)
        self.setMinimumWidth(300)
        self.show()
