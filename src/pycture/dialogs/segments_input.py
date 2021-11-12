from typing import List
from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QMainWindow,
                             QPushButton, QVBoxLayout, QHBoxLayout,
                             QLayout)
from PyQt5.QtCore import Qt, Signal

from pycture.editor.image.color import Color
from .notification import Notification
from .widgets import RGBCheckboxes, PointsInput, CustomIntValidator


class SegmentsInput(QDialog):
    previewed = Signal(list) # list of points
    applied = Signal(list, tuple) # list of points and color options
    # It is guaranteed that there will be at least two points

    def __init__(self, parent: QMainWindow):
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Linear transformation by segments")
        self.points = []
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.checkboxes = RGBCheckboxes(self)
        self.layout.addWidget(self.checkboxes)
        self.setup_point_input()
        self.setup_footer()

        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        self.show()
    
    def setup_point_input(self):
        self.layout.addWidget(QLabel("Number of segments:", self))
        self.number_of_points_input = QLineEdit("1", self)
        self.number_of_points_input.setValidator(CustomIntValidator(1, 25))
        self.layout.addWidget(self.number_of_points_input)
        accept_button = QPushButton("Accept", self)
        self.layout.addWidget(accept_button)

        self.points_input = PointsInput(self, CustomIntValidator(0, 255))
        self.points_input.set_number_of_points(2)
        self.layout.addWidget(self.points_input)
        accept_button.clicked.connect(self.update_number_of_points)
        
    def setup_footer(self):
        footer = QHBoxLayout()
        self.layout.addLayout(footer)

        preview_button = QPushButton("Preview")
        preview_button.clicked.connect(self.emit_previewed)
        footer.addWidget(preview_button)

        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.emit_applied)
        footer.addWidget(apply_button)
        
    def update_number_of_points(self):
        number_of_points = int(self.number_of_points_input.text()) + 1
        self.points_input.set_number_of_points(number_of_points)

    def emit_previewed(self):
        points = self.get_points()
        if points is not None:
            self.previewed.emit(points)

    def emit_applied(self):
        points = self.get_points()
        if points is not None:
            color_options = self.checkboxes.get_checked()
            self.applied.emit(points, color_options)

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
