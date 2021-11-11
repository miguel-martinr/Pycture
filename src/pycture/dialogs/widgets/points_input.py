from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QWidget, QLabel
from PyQt5.QtGui import QValidator
from PyQt5.QtCore import Qt

from .point_input import PointInput

class PointsInput(QWidget):
    def __init__(self, parent: QWidget, validator: QValidator):
        super().__init__(parent)
        self.validator = validator
        self.layout = QVBoxLayout()
        title_layout = QGridLayout()
        title_layout.addWidget(QLabel("X", self), 0, 1, Qt.AlignCenter)
        title_layout.addWidget(QLabel("Y", self), 0, 2, Qt.AlignCenter)
        self.layout.addLayout(title_layout)
        self.setLayout(self.layout)
        self.points = []
    
    def set_number_of_points(self, number: int):
        difference = number - len(self.points)
        if difference > 0:
            for _ in range(difference):
                self.add_point()
        elif difference < 0:
            for _ in range(-difference):
                self.remove_point()

    def remove_point(self):
        point =  self.points.pop()
        self.layout.removeWidget(point)
    
    def add_point(self):
        name = f"Point {len(self.points) + 1}: "
        new_point = PointInput(self, name, self.validator)
        self.points.append(new_point)
        self.layout.addWidget(new_point)
        
    def get_points(self):
        return list(map(lambda point: point.get_point(), self.points))
        