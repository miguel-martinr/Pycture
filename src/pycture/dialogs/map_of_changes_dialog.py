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

        
        self.treshold_input = QLineEdit("Treshold", self)
        
        self.treshold_input.setValidator(CustomIntValidator(0, 255))
        

        layout.addWidget(self.treshold_input, 0, 1, Qt.AlignmentFlag.AlignRight)
        

        # Marker color
        marker_color_label = QLabel("Marker color", self)
        layout.addWidget(marker_color_label, 2, 0, Qt.AlignmentFlag.AlignLeft)

        self.marker_color = ColorPicker(self, QColor(0x00ff0000))
        layout.addWidget(self.marker_color, 2, 1)
        self.marker_color.setMaximumWidth(self.treshold_input.width())

        # RGB Plane
        rgb_dropdown_label = QLabel("RGB plane", self)
        layout.addWidget(rgb_dropdown_label, 3, 0, Qt.AlignmentFlag.AlignLeft)

        self.rgb_dropdown = DropdownList(
            self, ["Red", "Green", "Blue", "Gray scale"])

        layout.addWidget(self.rgb_dropdown, 3, 1, Qt.AlignmentFlag.AlignRight)


        # Signals handling
        self.treshold_input.textChanged.connect(lambda: self._map_changed_())
        
        
        self.marker_color.color_changed.connect(lambda: self._map_changed_())
        
        
        self.rgb_dropdown.activated.connect(
            lambda index: self.rgb_plane_changed.emit(index))
        self.rgb_dropdown.setCurrentIndex(3)

        self.rgb_dropdown.activated.connect(
            lambda: self._map_changed_())
        self.rgb_dropdown.setCurrentIndex(3)
        
    def _map_changed_(self):
        treshold_text = self.treshold_input.text()
        treshold = int(treshold_text) if treshold_text != "" else 0
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


