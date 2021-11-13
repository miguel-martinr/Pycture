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
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        
        gray_checkbox = QCheckBox("Gray scale")
        gray_checkbox.stateChanged.connect(self.toggle_gray)
        self.layout.addWidget(gray_checkbox, 0, 0)

        self.setup_sliders()
        self.setup_buttons()
        
        self.show()
        
    def setup_sliders(self):
        self.layout.addWidget(QLabel("Brightness", self), 1, 0)
        self.layout.addWidget(QLabel("Contrast", self), 1, 1)
        self.brightness_sliders = RGBSliders(self, 0, 255)
        self.brightness_sliders.set_values(self.current_brightness[:-1])
        self.layout.addWidget(self.brightness_sliders, 2, 0)
        self.contrast_sliders = RGBSliders(self, 0, 255)
        self.contrast_sliders.set_values(self.current_contrast[:-1])
        self.layout.addWidget(self.contrast_sliders, 2, 1)

    def setup_buttons(self):
        recalculate_button = QPushButton("Recalculate", self)
        apply_button = QPushButton("Apply", self)
        recalculate_button.pressed.connect(lambda:
            self.recalculate.emit(self.get_values())
        )
        apply_button.pressed.connect(lambda:
            self.apply.emit(self.get_values())
        )
        self.layout.addWidget(recalculate_button, 3, 0) 
        self.layout.addWidget(apply_button, 3, 1)

    def toggle_gray(self, gray: bool):
        self.brightness_sliders.toggle_gray(gray)
        self.contrast_sliders.toggle_gray(gray)
        if gray:
            brightness_values = [self.current_brightness[-1]] * 3
            contrast_values = [self.current_contrast[-1]] * 3
        else:
            brightness_values = self.current_brightness
            contrast_values = self.current_contrast
        self.brightness_sliders.set_values(brightness_values)
        self.contrast_sliders.set_values(contrast_values)

    def get_values(self):
        brightness_values = self.brightness_sliders.get_values()
        contrast_values = self.contrast_sliders.get_values()
        return (brightness_values, contrast_values)

    # def update_values(self, brightness, contrast):
    #     def straiten(
    #         value, top): return 0 if value < 0 else top if value > top else value

    #     for i in range(4):
    #         self._brightness_inputs_[i].setText(
    #             str(round(straiten(brightness[i], 255))))
    #         self._contrast_inputs_[i].setText(
    #             str(round(straiten(contrast[i], 127))))
