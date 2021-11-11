
from typing import Tuple
from PyQt5.QtCore import QLine, Qt
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QSlider
from PyQt5.QtCore import Qt, Signal
from pycture.dialogs.segments_input import IntValidator


class EditBrightnessAndContrastDialog(QDialog):
    recalculate = Signal(tuple)
    apply = Signal(tuple)

    def __init__(self, parent: QMainWindow,
                 current_brightness: Tuple[int], current_contrast: Tuple[int]) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self._setup_(current_brightness, current_contrast)
        self.show()

    def _setup_(self, current_brightness, current_contrast):
        self.setWindowTitle("Edit brightness and contrast")
        layout = QGridLayout()
        self.setLayout(layout)
        self._set_brightness_inputs_(current_brightness)
        self._set_contrast_inputs_(current_contrast)
        self._set_buttons_()

    def _set_buttons_(self):
        layout = self.layout()

        recalculate_btn = QPushButton("Recalculate", self)
        apply_btn = QPushButton("Apply", self)

        recalculate_btn.pressed.connect(lambda:
                                        self.recalculate.emit(self.get_values()))
        apply_btn.pressed.connect(lambda:
                                  self.apply.emit(self.get_values()))

        layout.addWidget(recalculate_btn, layout.rowCount(),
                         0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(apply_btn, layout.rowCount() - 1,
                         layout.columnCount() - 1, Qt.AlignmentFlag.AlignCenter)

    def get_values(self):
        def get_value(input): return int(input.text())
        brightness_values = tuple(map(get_value, self._brightness_inputs_))
        contrast_values = tuple(map(get_value, self._contrast_inputs_))
        return (brightness_values, contrast_values)

    def update_values(self, brightness, contrast):
        def straiten(
            value, top): return 0 if value < 0 else top if value > top else value

        for i in range(3):
            self._brightness_inputs_[i].setText(
                str(round(straiten(brightness[i], 255))))
            self._contrast_inputs_[i].setText(
                str(round(straiten(contrast[i], 127))))

    def _set_brightness_inputs_(self, current_brightness):
        self._brightness_inputs_ = self._set_inputs_for_(
            "Brightness", 0, 0, current_brightness, 255)

    def _set_contrast_inputs_(self, current_contrast):
        self._contrast_inputs_ = self._set_inputs_for_(
            "Contrast", 0, 1, current_contrast, 127)

    def _set_inputs_for_(self, title, row, col, values, top_limit):
        layout = QGridLayout()
        layout.addWidget(QLabel(title, self), 0,
                         0, Qt.AlignmentFlag.AlignCenter)

        self.layout().addLayout(layout, row, col)

        orientation = Qt.Orientation.Horizontal
        inputs = [QLineEdit(str(round(values[i]))) for i in range(4)]

        def to_int(str_value): return 0 if (
            str_value == "") else int(str_value)

        colors = ["#ff0000", "#00ff00", "#0000ff", "#6c6c6c"]
        for i, input in enumerate(inputs):
            slider = QSlider(orientation, self)
            input.setValidator(IntValidator(0, top_limit))
            slider.setMaximum(top_limit)
            slider.setStyleSheet(
                "QSlider::handle:horizontal {background-color: " + colors[i] + ";}")
            slider.setValue(to_int(values[i]))

            slider.valueChanged.connect(
                lambda value, i=input: i.setText(str(value)))
            input.textChanged.connect(
                lambda value, s=slider: s.setValue(to_int(value)))  # ASTONISHING!
            j = 2 * i
            layout.addWidget(input, j + 1, 0, Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(slider, j + 2, 0)
        return inputs
