from typing import List

from PyQt5.QtWidgets import (
    QCheckBox, QDialog, QGridLayout, QVBoxLayout, QLabel, QMainWindow, QPushButton
)
from PyQt5.QtCore import Qt, Signal
from .widgets import RGBSliders, DropdownList
from .notification import Notification

class EditBrightnessAndContrastDialog(QDialog):
    # The name of the editor and the values of the brightness and contrast
    # to apply. The brightness varies between 0 and 255 and the contrast
    # between 1 and 128. 128 shouldn't be used, it is allowed to
    # represent 127.5 in the slider which is a valid contrast value
    applied = Signal(str, tuple, tuple)

    def __init__(self, parent: QMainWindow, editors: List[str]):
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Edit brightness and contrast")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.layout.addWidget(QLabel("Image:", self))
        self.dropdown = DropdownList(self, editors)
        self.layout.addWidget(self.dropdown)
        self.dropdown.textActivated.connect(self.update_selected_editor)
        self.current_brightness = [0] * 4
        self.current_contrast = [0] * 4
        
        gray_checkbox = QCheckBox("Gray scale")
        gray_checkbox.stateChanged.connect(self.toggle_gray)
        self.layout.addWidget(gray_checkbox)
        self.gray = False

        self.setup_sliders()
        apply_button = QPushButton("Apply", self)
        apply_button.pressed.connect(self.emit_aplied)
        self.layout.addWidget(apply_button)
        
        self.show()
        
    def setup_sliders(self):
        layout = QGridLayout()
        layout.addWidget(QLabel("Brightness", self), 0, 0)
        layout.addWidget(QLabel("Contrast", self), 0, 1)
        self.brightness_sliders = RGBSliders(self, 0, 255)
        self.brightness_sliders.set_disabled(True)
        self.brightness_sliders.set_values(self.current_brightness[:-1])
        layout.addWidget(self.brightness_sliders, 1, 0)
        self.contrast_sliders = RGBSliders(self, 0, 128)
        self.contrast_sliders.set_disabled(True)
        self.contrast_sliders.set_values(self.current_contrast[:-1])
        layout.addWidget(self.contrast_sliders, 1, 1)
        self.layout.addLayout(layout)

    def toggle_gray(self, gray: bool):
        self.gray = gray
        self.brightness_sliders.toggle_gray(gray)
        self.contrast_sliders.toggle_gray(gray)
        self.update_sliders()
        
    def update_sliders(self):
        if self.gray:
            brightness_values = [self.current_brightness[-1]] * 3
            contrast_values = [self.current_contrast[-1]] * 3
        else:
            brightness_values = self.current_brightness[:-1]
            contrast_values = self.current_contrast[:-1]
        self.brightness_sliders.set_values(brightness_values)
        self.contrast_sliders.set_values(contrast_values)
        
    def update_selected_editor(self, editor: str):
        self.brightness_sliders.set_disabled(False)
        self.contrast_sliders.set_disabled(False)
        image = self.parent().get_editor(editor).get_image()
        self.current_brightness = list(map(lambda x: int(x), image.get_brightness()))
        self.current_contrast = list(map(lambda x: int(x), image.get_contrast()))
        self.update_sliders()
        
    def emit_aplied(self):
        brightness, contrast = self.get_values()
        editor = self.dropdown.currentText()
        if self.parent().get_editor(editor) is None:
            Notification(self, "An active image must be chosen")
            return
        self.applied.emit(editor, brightness, contrast)

    def get_values(self):
        brightness_values = tuple(map(
            lambda x: float(x), self.brightness_sliders.get_values()
        ))
        # Contrast values allow 128 as a value for the slider but 128 isn't
        # a valid value for a contrast. It is only allowed to let the user
        # specify 127.5
        contrast_values = tuple(map(
            lambda x: min(float(x), 127.5), self.contrast_sliders.get_values()
        ))
        return brightness_values, contrast_values
