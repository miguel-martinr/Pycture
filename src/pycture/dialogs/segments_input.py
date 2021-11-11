from typing import List
from PyQt5.QtGui import QValidator
from PyQt5.QtWidgets import (QCheckBox, QDialog, QFormLayout, QGridLayout,
                             QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                             QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt, Signal

from pycture.editor.image.color import Color
from .widgets import RGBCheckboxes


class SegmentsInput(QDialog):
    previewed = Signal(list)
    applied = Signal(list, tuple)

    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self._setup_()
        self.show()

    def _setup_(self):
        self.setWindowTitle("Linear transformation by segments")
        self.point_inputs = []

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.checkboxes = RGBCheckboxes(self)
        layout.addWidget(self.checkboxes)

        # Input and accept button
        self.num_of_segments_form = QFormLayout()
        layout.addLayout(self.num_of_segments_form)
        accept_button, segments_num_input = self._get_segments_num_input_(
            self.num_of_segments_form)

        # Point inputs
        self.points_grid = QGridLayout()
        self.points_grid.addWidget(
            QLabel("X"), 0, 1, Qt.AlignmentFlag.AlignCenter)
        self.points_grid.addWidget(
            QLabel("Y"), 0, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(self.points_grid)

        accept_button.clicked.connect(lambda: self._update_point_inputs_(
            int(segments_num_input.text()) + 1, self.points_grid))

        # To place preview and apply buttons
        footer = QGridLayout()
        layout.addLayout(footer)

        # Preview button
        preview_button = QPushButton("Preview")
        preview_button.setDisabled(True)
        preview_button.clicked.connect(
            lambda: self.previewed.emit(self.get_points())
        )
        accept_button.clicked.connect(lambda: preview_button.setDisabled(False))
        footer.addWidget(preview_button, 0, 0)

        # Apply button
        apply_button = QPushButton("Apply")
        apply_button.setDisabled(True)
        apply_button.clicked.connect(
            lambda: self.applied.emit(self.get_segments(), self.checkboxes.get_checked())
        )
        accept_button.clicked.connect(lambda: apply_button.setDisabled(False))
        footer.addWidget(apply_button, 0, 1)

    def _add_point_input_(self):
        input = self._get_int_input_(0, 255)
        self.point_inputs.append(input)
        return input

    def _remove_last_point_inputs_(self):
        last_point_inputs = self.point_inputs.pop()
        for input in last_point_inputs:
            input.deleteLater()
        self.points_grid.itemAtPosition(
            len(self.point_inputs) + 1, 0).widget().deleteLater()

    def _update_point_inputs_(self, num_of_points: int, grid: QGridLayout):
        points_len = len(self.point_inputs)

        if (points_len > num_of_points):
            while (points_len > num_of_points):
                self._remove_last_point_inputs_()
                points_len -= 1
            return

        while (points_len < num_of_points):
            grid.addWidget(QLabel(f"Point {points_len}: "), points_len + 1, 0)
            inputX = self._get_int_input_(0, 255)
            inputY = self._get_int_input_(0, 255)
            grid.addWidget(inputX, points_len + 1, 1)
            grid.addWidget(inputY, points_len + 1, 2)

            self.point_inputs.append((inputX, inputY))
            points_len += 1

    def _get_segments_num_input_(self, form: QFormLayout):
        num_of_segments_input = self._get_int_input_(1, 10, 1)
        form.addRow("Num of segments:", num_of_segments_input)
        accept_button = QPushButton("Accept", self)
        form.addRow(accept_button)
        return accept_button, num_of_segments_input

    def _get_int_input_(self, bottom: int, top: int, default: int = 0):
        input = QLineEdit(str(default))
        input.setValidator(IntValidator(bottom, top))
        return input

    def get_points(self):
        points = []
        for x_input, y_input in self.point_inputs:
            x = int(x_input.text())
            y = int(y_input.text())
            points.append([x, y])
        self._sanitize_points_(points)
        return points

    def _sanitize_points_(self, points):
        for i in range(1, len(points)):
            if (points[i - 1][0] >= points[i][0]):
                points[i][0] = points[i - 1][0] + 1

    def get_segments(self):
        points = self.get_points()
        segments = []
        for i in range(len(points) - 1):
            segments.append((points[i], points[i + 1]))
        return segments


class IntValidator(QValidator):
    def __init__(self, bottom: int, top: int) -> None:
        super().__init__()
        self.bottom = bottom
        self.top = top

    def validate(self, input: str, pos: int):
        State = QValidator.State

        if (input == ""):
            return State.Intermediate, input, pos
        if (not str.isdigit(input)):
            return State.Invalid, input, pos
        if (not (self.bottom <= int(input) <= self.top)):
            return State.Invalid, input, pos
        return State.Acceptable, input, pos
