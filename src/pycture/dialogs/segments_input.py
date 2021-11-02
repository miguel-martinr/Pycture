from typing import List 
from PyQt5.QtGui import QValidator
from PyQt5.QtWidgets import QCheckBox, QDialog, QFormLayout, QGridLayout, QHBoxLayout, QInputDialog, QLabel, QLayout, QLayoutItem, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, Signal

from pycture.editor.image.color import Color


class SegmentsInput(QDialog):
    previewed = Signal(list)
    applied = Signal(list)

    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self._setup_()
        self.show()

    def _setup_(self):
        self.setWindowTitle("Linear transformation by segments")
        self.point_inputs = []

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Colors checkboxes
        self._set_color_opts_()

        # Input and accept btn
        self.num_of_segments_form = QFormLayout()
        layout.addLayout(self.num_of_segments_form)
        accept_btn, segments_num_input = self._get_segments_num_input_(
            self.num_of_segments_form)

        # Point inputs
        self.points_grid = QGridLayout()
        self.points_grid.addWidget(
            QLabel("X"), 0, 1, Qt.AlignmentFlag.AlignCenter)
        self.points_grid.addWidget(
            QLabel("Y"), 0, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(self.points_grid)

        accept_btn.clicked.connect(lambda: self._update_point_inputs_(
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

    def _set_color_opts_(self):
        # Colors checkboxes
        self.checkboxes = []
        my_layout = QHBoxLayout()
        color_opts = ["Red", "Green", "Blue", "All"]
        for i, color in enumerate(color_opts):
            checkbox = QCheckBox(color, self)
            self.checkboxes.append(checkbox)
            my_layout.addWidget(checkbox)
        self.checkboxes[-1].stateChanged.connect(self._set_all_checkboxes_)
        self.layout().addLayout(my_layout)

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
        accept_btn = QPushButton("Accept", self)
        form.addRow(accept_btn)
        return accept_btn, num_of_segments_input

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

    def _set_all_checkboxes_(self, state: Qt.CheckState):
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
