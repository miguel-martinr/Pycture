from typing import List, Tuple
from PyQt5.QtGui import QValidator
from PyQt5.QtWidgets import QCheckBox, QDialog, QFormLayout, QGridLayout, QHBoxLayout, QInputDialog, QLabel, QLayout, QLayoutItem, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSignal

from pycture.editor.image.color import Color


class SegmentsInput(QDialog):
    previewed = pyqtSignal(list)
    applied = pyqtSignal(list)

    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self.setup()
        self.show()

    def setup(self):
        self.setWindowTitle("Linear transformation by segments")
        self.point_inputs = []

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Colors checkboxes
        self.set_color_opts()

        # Input and accept btn
        self.num_of_segments_form = QFormLayout()
        layout.addLayout(self.num_of_segments_form)
        accept_btn, segments_num_input = self.set_segments_num_input(
            self.num_of_segments_form)

        # Point inputs
        self.points_grid = QGridLayout()
        self.points_grid.addWidget(
            QLabel("X"), 0, 1, Qt.AlignmentFlag.AlignCenter)
        self.points_grid.addWidget(
            QLabel("Y"), 0, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(self.points_grid)

        accept_btn.clicked.connect(lambda: self.update_point_inputs(
            int(segments_num_input.text()) + 1, self.points_grid))

        # To place preview and apply buttons
        footer = QGridLayout()
        layout.addLayout(footer)

        # Preview btn
        preview_btn = QPushButton("Preview")
        preview_btn.setDisabled(True)
        preview_btn.clicked.connect(
            lambda: self.previewed.emit(
                self.get_segments()))
        accept_btn.clicked.connect(lambda: preview_btn.setDisabled(False))
        footer.addWidget(preview_btn, 0, 0)

        # Apply btn
        apply_btn = QPushButton("Apply")
        apply_btn.setDisabled(True)
        apply_btn.clicked.connect(
            lambda: self.applied.emit(
                self.get_segments()))
        accept_btn.clicked.connect(lambda: apply_btn.setDisabled(False))
        footer.addWidget(apply_btn, 0, 1)

    def set_color_opts(self):
        # Colors checkboxes
        self.checkboxes = []
        my_layout = QHBoxLayout()
        color_opts = ["Red", "Green", "Blue", "All"]
        for i, color in enumerate(color_opts):
            checkbox = QCheckBox(color, self)
            self.checkboxes.append(checkbox)
            my_layout.addWidget(checkbox)
        self.checkboxes[-1].stateChanged.connect(self.set_all_checkboxes)
        self.layout().addLayout(my_layout)

    def add_point_input(self):
        input = self.get_int_input(0, 255)
        self.point_inputs.append(input)
        return input

    def remove_last_point_inputs(self):
        last_point_inputs = self.point_inputs.pop()
        for input in last_point_inputs:
            input.deleteLater()
        self.points_grid.itemAtPosition(
            len(self.point_inputs) + 1, 0).widget().deleteLater()

    def update_point_inputs(self, num_of_points: int, grid: QGridLayout):
        points_len = len(self.point_inputs)

        if (points_len > num_of_points):
            while (points_len > num_of_points):
                self.remove_last_point_inputs()
                points_len -= 1
            return

        while (points_len < num_of_points):
            grid.addWidget(QLabel(f"Point {points_len}: "), points_len + 1, 0)
            inputX = self.get_int_input(0, 255)
            inputY = self.get_int_input(0, 255)
            grid.addWidget(inputX, points_len + 1, 1)
            grid.addWidget(inputY, points_len + 1, 2)

            self.point_inputs.append((inputX, inputY))
            points_len += 1

    def set_segments_num_input(self, form: QFormLayout):
        num_of_segments_input = self.get_int_input(1, 10, 1)
        form.addRow("Num of segments:", num_of_segments_input)
        accept_btn = QPushButton("Accept", self)
        form.addRow(accept_btn)
        return accept_btn, num_of_segments_input

    def get_int_input(self, bottom: int, top: int, default: int = 0):
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

    def set_all_checkboxes(self, state: Qt.CheckState):
        if (state != Qt.CheckState.Checked):
            return
        for checkbox in self.checkboxes:
            checkbox.setCheckState(state)

    def get_color_opts(self) -> List[Color]:
        opts = []
        for i, checkbox in enumerate(self.checkboxes):
            if (checkbox.isChecked() and i < 3):
                opts.append(Color._value2member_map_[i])
        return opts


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
