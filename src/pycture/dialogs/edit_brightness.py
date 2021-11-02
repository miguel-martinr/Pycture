
from typing import Tuple
from PyQt5.QtCore import QLine, Qt
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QMainWindow, QSlider

from pycture.dialogs.segments_input import IntValidator


class EditBrightnessDialog(QDialog):
    def __init__(self, parent: QMainWindow, current_brightness: Tuple[int], current_contrast: Tuple[int]) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self._setup_(current_brightness, current_contrast)
        self.show()

    def _setup_(self, current_brightness, current_contrast):
        self.setWindowTitle("Edit brightness and contrast")
        layout = QGridLayout()
        self.setLayout(layout)
        self._set_brightness_inputs_(current_brightness)
        
    def _set_brightness_inputs_(self, current_brightness):
        self._brightness_inputs_ = []
        self._set_inputs_for_("Brightness", 0, 0, current_brightness, self._brightness_inputs_, 255)
        
        
    def _set_inputs_for_(self, title, row, col, values, inputs, top_limit):
        layout = QGridLayout()
        layout.addWidget(QLabel(title, self), 0,
                         0, Qt.AlignmentFlag.AlignCenter)
        
        self.layout().addLayout(layout, row, col)

        orientation = Qt.Orientation.Horizontal
        inputs = [QLineEdit(str(round(values[i]))) for i in range(3)]
        to_int = lambda str_value: 0 if (str_value == "") else int(str_value)
        

        colors = ["#ff0000", "#00ff00", "#0000ff"]
        for i, input in enumerate(inputs):
            slider = QSlider(orientation, self)
            input.setValidator(IntValidator(0, top_limit))
            slider.setMaximum(top_limit)    
            slider.setStyleSheet("QSlider::handle:horizontal {background-color: " + colors[i] + ";}");
            slider.setValue(to_int(values[i]))
            
            slider.valueChanged.connect(lambda value, i = input: i.setText(str(value)))
            input.textChanged.connect(lambda value, s = slider: s.setValue(to_int(value))) # ASTONISHING!
            j = 2 * i
            layout.addWidget(input, j + 1, 0, Qt.AlignmentFlag.AlignLeft)    
            layout.addWidget(slider, j + 2, 0)   
        
        



