from PyQt5.QtWidgets import QCheckBox, QDialog, QGridLayout, QLabel, QMainWindow, QPushButton
from PyQt5.QtCore import Qt, Signal
from .widgets import RGBSliders

class EditBrightnessAndContrastDialog(QDialog):
    recalculate = Signal(tuple)
    apply = Signal(tuple)

    def __init__(self, parent: QMainWindow,
        current_brightness: (int, int, int),
        current_contrast: (int, int, int)
    ):
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Edit brightness and contrast")
        self.current_brightness = current_brightness
        self.current_contrast = current_contrast
        layout = QGridLayout()
        self.setLayout(layout)
        
        gray_checkbox = QCheckBox("Gray scale")
        # gray_checkbox.stateChanged.connect(self.set_gray)
        layout.addWidget(gray_checkbox, 0, 0)
        
        layout.addWidget(QLabel("Brightness", self), 1, 0)
        layout.addWidget(QLabel("Contrast", self), 1, 1)
        self.brightness_sliders = RGBSliders(self, 0, 255)
        self.brightness_sliders.set_values(self.current_brightness[:-1])
        layout.addWidget(self.brightness_sliders, 2, 0)
        self.contrast_sliders = RGBSliders(self, 0, 255)
        self.contrast_sliders.set_values(self.current_contrast[:-1])
        layout.addWidget(self.contrast_sliders, 2, 1)
        self.show()

    # def set_gray(self, gray_checked: Qt.CheckState):
    #     gray_checked = True if gray_checked == Qt.CheckState.Checked else False
    #     gray_slider: QSlider = self._brightness_sliders_[3]
    #     gray_slider.setEnabled(gray_checked)
    #     for i in range(3):
    #         brightness_slider: QSlider = self._brightness_sliders_[i]
    #         brightness_slider.setDisabled(gray_checked)
    #         brightness_input: QLine = self._brightness_inputs_[i]
    #         brightness_input.setDisabled(gray_checked)            
    #         brightness_input.setText(self._brightness_inputs_[3].text())
    #         self._brightness_inputs_[3].textChanged.connect(lambda text, input=brightness_input: input.setText(text))
            
    #         contrast_slider: QSlider = self._contrast_sliders_[i]
    #         contrast_slider.setDisabled(gray_checked)
    #         contrast_input: QLine = self._contrast_inputs_[i]
    #         contrast_input.setDisabled(gray_checked)
    #         contrast_input.setText(self._contrast_inputs_[3].text())
    #         self._contrast_inputs_[3].textChanged.connect(lambda text, input=contrast_input: input.setText(text))

    # def _set_buttons_(self):
    #     layout = self.layout()

    #     recalculate_btn = QPushButton("Recalculate", self)
    #     apply_button = QPushButton("Apply", self)

    #     recalculate_btn.pressed.connect(lambda:
    #                                     self.recalculate.emit(self.get_values()))
    #     apply_button.pressed.connect(lambda:
    #                               self.apply.emit(self.get_values()))

    #     layout.addWidget(recalculate_btn, layout.rowCount(),
    #                      0, Qt.AlignmentFlag.AlignCenter)
    #     layout.addWidget(apply_button, layout.rowCount() - 1,
    #                      layout.columnCount() - 1, Qt.AlignmentFlag.AlignCenter)

    # def get_values(self):
    #     def get_value(input): return int(input.text())
    #     brightness_values = tuple(map(get_value, self._brightness_inputs_))
    #     contrast_values = tuple(map(get_value, self._contrast_inputs_))
    #     return (brightness_values, contrast_values)

    # def update_values(self, brightness, contrast):
    #     def straiten(
    #         value, top): return 0 if value < 0 else top if value > top else value

    #     for i in range(4):
    #         self._brightness_inputs_[i].setText(
    #             str(round(straiten(brightness[i], 255))))
    #         self._contrast_inputs_[i].setText(
    #             str(round(straiten(contrast[i], 127))))
