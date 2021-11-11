from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

class PlotWindow(QWidget):
    def __init__(self, parent: QWidget, plot: FigureCanvasQTAgg, title: str):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.layout.addWidget(plot)
        self.setParent(parent, Qt.WindowType.Window)
        self.setMinimumWidth(300)
        self.show()
