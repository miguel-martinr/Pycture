from PyQt5.QtWidgets import (
    QCheckBox, QDialog, QGridLayout, QVBoxLayout, QLabel, QMainWindow, QPushButton
)
from PyQt5.QtCore import Qt, Signal
from .widgets import RGBSliders

class EditBrightnessAndContrastDialog(QDialog):
    apply = Signal(tuple)

    def __init__(self, parent: QMainWindow,
        current_brightness: (int, int, int),
        current_contrast: (int, int, int)
    ):
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Edit brightness and contrast")
        self.current_brightness = current_brightness
        self.current_contrast = current_contrast
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        gray_checkbox = QCheckBox("Gray scale")
        gray_checkbox.stateChanged.connect(self.toggle_gray)
        self.layout.addWidget(gray_checkbox)

        self.setup_sliders()
        apply_button = QPushButton("Apply", self)
        apply_button.pressed.connect(lambda:
            self.apply.emit(self.get_values())
        )
        self.layout.addWidget(apply_button)
        
        self.show()
        
    def setup_sliders(self):
        layout = QGridLayout()
        layout.addWidget(QLabel("Brightness", self), 0, 0)
        layout.addWidget(QLabel("Contrast", self), 0, 1)
        self.brightness_sliders = RGBSliders(self, 0, 255)
        self.brightness_sliders.set_values(self.current_brightness[:-1])
        layout.addWidget(self.brightness_sliders, 1, 0)
        self.contrast_sliders = RGBSliders(self, 0, 127)
        self.contrast_sliders.set_values(self.current_contrast[:-1])
        layout.addWidget(self.contrast_sliders, 1, 1)
        self.layout.addLayout(layout)

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
