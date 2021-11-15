from typing import List

from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QMainWindow,
                             QPushButton, QVBoxLayout, QHBoxLayout,
                             QLayout, QSizePolicy, QWidget)
from PyQt5.QtCore import Qt, Signal
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from pycture.editor.image.color import Color
from .notification import Notification
from .widgets import RGBCheckboxes, PointsInput, CustomIntValidator, DropdownList

PLOT_LINE_COLOR = "#0000ff"
PLOT__LINE_WIDTH = 3


class SegmentsInput(QDialog):
    applied = Signal(str, list, tuple) # Editor, list of points and color options
    # It is guaranteed that there will be at least two points

    def __init__(self, parent: QMainWindow, editors: List[str]):
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Linear transformation by segments")
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.graph_figure = None
        
        self.setup_options_layout(editors)
        graph = self.preview_transformation()
        graph.setFixedSize(graph.size())
        self.layout.addWidget(graph)

        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        self.show()
    
    def setup_options_layout(self, editors: List[str]):
        options_layout = QVBoxLayout()
        self.layout.addLayout(options_layout)
        self.dropdown = DropdownList(self, editors)
        options_layout.addWidget(self.dropdown)

        self.checkboxes = RGBCheckboxes(self)
        options_layout.addWidget(self.checkboxes)
        self.setup_points_input(options_layout)
        
        separator = QWidget()
        separator.setMinimumSize(0, 0)
        separator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        options_layout.addWidget(separator)

        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.emit_applied)
        options_layout.addWidget(apply_button)
    
    def setup_points_input(self, layout: QVBoxLayout):
        layout.addWidget(QLabel("Number of segments:", self))
        self.number_of_points_input = QLineEdit("1", self)
        self.number_of_points_input.setValidator(CustomIntValidator(1, 25))
        layout.addWidget(self.number_of_points_input)
        accept_button = QPushButton("Accept", self)
        layout.addWidget(accept_button)

        self.points_input = PointsInput(self, CustomIntValidator(0, 255))
        self.points_input.points_changed.connect(self.update_graph)
        self.points_input.set_number_of_points(2)
        layout.addWidget(self.points_input)
        accept_button.clicked.connect(self.update_number_of_points)
        
    def update_number_of_points(self):
        number_of_points = int(self.number_of_points_input.text()) + 1
        self.points_input.set_number_of_points(number_of_points)

    def emit_applied(self):
        points = self.get_points()
        if points is None:
            return
        editor = self.dropdown.currentText()
        if self.parent().get_editor(editor) is None:
            Notification(self, "An active image must be chosen")
            return
        color_options = self.checkboxes.get_checked()
        self.applied.emit(editor, points, color_options)

    def get_points(self):
        points = self.points_input.get_points() 
        if self.check_points_integrity(points):
            return points
        Notification(self, "The x coordinates of the points must be monotonically increasing")

    def check_points_integrity(self, points):
        points_x = list(map(lambda point: point[0], self.points_input.get_points()))        
        for i in range(len(points_x) - 1):
            if points_x[i] >= points_x[i + 1]:
                return False
        return True

    def set_dropdown_image(self, editor: str):
        self.dropdown.set_selected(editor)
        
    def update_graph(self):
        new_graph = self.preview_transformation()
        new_graph.setFixedSize(new_graph.size())
        old_graph = self.layout.itemAt(1).widget()
        self.layout.removeWidget(old_graph)
        old_graph.deleteLater()
        self.layout.addWidget(new_graph)

    def preview_transformation(self) -> FigureCanvasQTAgg:
        plt.style.use('dark_background')
        title = "Linear transformation"
        if self.graph_figure is not None:
            plt.close(self.graph_figure)
        self.graph_figure = plt.figure()
        points = self.points_input.get_points()
        self.plot_changes(points)
        self.plot_unchanged_areas(points)

        plt.xlabel("Vin")
        plt.ylabel("Vout")
        plt.title(title)
        plt.xlim(0, 255)
        plt.ylim(0, 255)
        return FigureCanvasQTAgg(self.graph_figure)
    
    def plot_changes(self, points: List):
        x = list(map(lambda point: point[0], points))
        y = list(map(lambda point: point[1], points))
        plt.plot(x, y, color=PLOT_LINE_COLOR, linewidth=3)
    
    def plot_unchanged_areas(self, points: List):
        if len(points) == 0:
            return
        if points[0][0] > 1:
            x = [0, points[0][0]]
            y = x
            plt.plot(x, y, color=PLOT_LINE_COLOR, linewidth=3)
        if points[-1][0] < 254:
            x = [points[-1][0], 255]
            y = x
            plt.plot(x, y, color=PLOT_LINE_COLOR, linewidth=3)
