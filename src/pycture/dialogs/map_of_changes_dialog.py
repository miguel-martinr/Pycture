import typing
from PyQt5 import QtGui
from PyQt5.QtCore import QObject, Qt, Signal
from PyQt5.QtGui import QColor, QValidator
from PyQt5.QtWidgets import QColorDialog, QDialog, QGridLayout, QLabel, QLineEdit, QMainWindow, QSlider, QVBoxLayout, QWidget

from pycture.dialogs.widgets import DropdownList
from .widgets import CustomIntValidator


class MapOfChangesDialog(QDialog):
    #  Treshold    RGB Plane  Marker Color
    map_changed = Signal(int, int, QColor)
    rgb_plane_changed = Signal(int)

    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self._setup_()

    def _setup_(self):
        self.setWindowTitle("Map of changes")
        layout = QVBoxLayout()
        self.setLayout(layout)
        self._set_inputs_()

        maximum_width = 300
        self.setMinimumWidth(maximum_width)
        self.setMaximumWidth(maximum_width)

    def _set_inputs_(self):
        layout = QGridLayout()
        self.layout().addLayout(layout)

        # Treshold
        treshold_label = QLabel("Treshold", self)
        layout.addWidget(treshold_label, 0, 0, Qt.AlignmentFlag.AlignLeft)

        
        self.treshold_input = TextInputWithSlider(self, CustomIntValidator(0, 255))
        

        layout.addWidget(self.treshold_input.text_input, 0, 1, Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.treshold_input.slider, 1, 1, Qt.AlignmentFlag.AlignRight)

        # Marker color
        marker_color_label = QLabel("Marker color", self)
        layout.addWidget(marker_color_label, 2, 0, Qt.AlignmentFlag.AlignLeft)

        self.marker_color = ColorPicker(self, QColor(0x00ff0000))
        layout.addWidget(self.marker_color, 2, 1)
        self.marker_color.setMaximumWidth(self.treshold_input.text_input.width())

        # RGB Plane
        rgb_dropdown_label = QLabel("RGB plane", self)
        layout.addWidget(rgb_dropdown_label, 3, 0, Qt.AlignmentFlag.AlignLeft)

        self.rgb_dropdown = DropdownList(
            self, ["Red", "Green", "Blue", "Gray scale"])

        layout.addWidget(self.rgb_dropdown, 3, 1, Qt.AlignmentFlag.AlignRight)


        # Signals handling
        self.treshold_input.value_changed.connect(lambda: self._map_changed_())
        self.treshold_input.slider.setValue(127)
        
        self.marker_color.color_changed.connect(lambda: self._map_changed_())
        
        
        self.rgb_dropdown.activated.connect(
            lambda index: self.rgb_plane_changed.emit(index))
        self.rgb_dropdown.setCurrentIndex(3)

        self.rgb_dropdown.activated.connect(
            lambda: self._map_changed_())
        self.rgb_dropdown.setCurrentIndex(3)
        
    def _map_changed_(self):
        treshold = self.treshold_input.get_value()
        rgb_plane = self.rgb_dropdown.currentIndex()
        marker_color = self.marker_color.get_color()

        self.map_changed.emit(treshold, rgb_plane, marker_color)


class ColorPicker(QLabel):
    color_changed = Signal(QColor)
    def __init__(self, parent: QWidget, initial_color: QColor) -> None:
        super().__init__(parent)
        self._set_color_(initial_color)
        self._set_dialog_(initial_color)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.color_dialog.show()

    def _set_color_(self, color: QColor):
        self.color = color
        html_color = self._get_html_color_(color)
        self.setStyleSheet(f"background-color: {html_color}")
        self.color_changed.emit(self.color)

    def get_color(self):
        return self.color

    def _get_html_color_(self, color: QColor = None):
        if (color is None):
            color = self.color
        html_color = '#' + hex(color.rgb())[2:]
        return html_color

    def _set_dialog_(self, initial_color: QColor):
        self.color_dialog = QColorDialog(QColor(initial_color), self)
        self.color_dialog.setStyleSheet("background-color: black")
        self.color_dialog.setWindowFlags(Qt.WindowType.Window)

        self.color_dialog.colorSelected.connect(
            lambda color: self._set_color_(color))


class TextInputWithSlider(QObject):
    # The value of the slider is taken as the whole input value
    value_changed = Signal(int)
    
    #
    # @param to_slider tranforms the text input before setting it as the slider's value.
    # (A function that receives any string allowed by the specified validator and returns an integer)
    #
    # @param to_input tranforms the int slider's value before setting it as the text input's value.
    # (A function that receives any int allowed by the specified validator and returns a string)
    #
    def __init__(self, parent: QWidget = None,
                 validator: QValidator = None,
                 bottom: int = 0,
                 top: int = 255,
                 to_slider: typing.Callable = int,
                 to_input: typing.Callable = str) -> (QLineEdit, QSlider):
        super().__init__(parent=None)

        if validator is None:
            validator = CustomIntValidator(bottom, top)
            
        self.to_slider = to_slider
        self.to_input = to_input
        
        self.text_input = text_input = QLineEdit(parent)
        text_input.setValidator(validator)
        
        self.slider = slider = QSlider(orientation=Qt.Orientation.Horizontal)
        self.slider.setMinimum(bottom)
        self.slider.setMaximum(top)

        text_input.textChanged.connect(
            lambda text: slider.setValue(to_slider(text)))
        slider.valueChanged.connect(
            lambda value: text_input.setText(to_input(value))
        )

        text_input.textChanged.connect(
            lambda: self.value_changed.emit(self.slider.value())
        )
        slider.valueChanged.connect(
            lambda value: self.value_changed.emit(value)
        )
        
        
    # Returns slider's current value (int)
    def get_value(self):
        return self.to_slider()
