from PyQt5.QtCore import  Qt, Signal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QDialog, QGridLayout, QLabel, QLayout, QLineEdit,
    QMainWindow, QPushButton, QVBoxLayout
) 

from pycture.dialogs.plot_window import PlotWindow
from pycture.editor.image.color import Color
from .widgets import CustomIntValidator, ColorPicker, DropdownList


class MapOfChangesDialog(QDialog):
    #  Treshold    RGB Plane  Marker Color
    map_changed = Signal(int, int, QColor)
    rgb_plane_changed = Signal(int)
    save_current = Signal()

    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Map of changes")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        self._setup_inputs_()
        self._set_button_()
        
        self.plot = None

        self.setFixedWidth(300)

    def _setup_inputs_(self):
        layout = QGridLayout()
        self.layout.addLayout(layout)

        # Treshold
        treshold_label = QLabel("Treshold", self)
        layout.addWidget(treshold_label, 0, 0, Qt.AlignmentFlag.AlignLeft)
        self.treshold_input = QLineEdit("127", self)
        self.treshold_input.setValidator(CustomIntValidator(0, 255))
        self.treshold_input.textChanged.connect(lambda: self._map_changed_())
        layout.addWidget(self.treshold_input, 0, 1, Qt.AlignmentFlag.AlignRight)

        # Marker color
        marker_color_label = QLabel("Marker color", self)
        layout.addWidget(marker_color_label, 1, 0, Qt.AlignmentFlag.AlignLeft)
        self.marker_color = ColorPicker(self, QColor(0x00ff0000))
        self.marker_color.setMaximumWidth(self.treshold_input.width())
        self.marker_color.color_changed.connect(lambda: self._map_changed_())
        layout.addWidget(self.marker_color, 1, 1)

        # RGB Plane
        rgb_dropdown_label = QLabel("RGB plane", self)
        layout.addWidget(rgb_dropdown_label, 2, 0, Qt.AlignmentFlag.AlignLeft)
        self.rgb_dropdown = DropdownList(self, ["Red", "Green", "Blue", "Gray scale"])
        self.rgb_dropdown.activated.connect(lambda: self._map_changed_())
        self.rgb_dropdown.setFixedWidth(150)
        self.rgb_dropdown.activated.connect(
            lambda index: self.rgb_plane_changed.emit(index)
        )
        layout.addWidget(self.rgb_dropdown, 2, 1, Qt.AlignmentFlag.AlignRight)
        
    def _map_changed_(self):
        treshold_text = self.treshold_input.text()
        treshold = int(treshold_text) if treshold_text != "" else 0
        rgb_plane = self.rgb_dropdown.currentIndex()
        marker_color = self.marker_color.get_color()

        self.map_changed.emit(treshold, rgb_plane, marker_color)

    def _set_button_(self):
        save_current_button = QPushButton("Save current", self)
        save_current_button.pressed.connect(lambda: self.save_current.emit())
        self.layout.addWidget(save_current_button)

    def update_plot(self, new_plot: PlotWindow):
        if self.plot is None:
            self.layout.addWidget(new_plot)
            self.plot = new_plot
            return 
    
        self.layout.replaceWidget(self.plot, new_plot)
        self.plot.destroy(True, True)
        self.plot.deleteLater()
        self.plot = new_plot
            
    def set_rgb_plane(self, color: Color):
        option = self.rgb_dropdown.options[color.value]
        self.rgb_dropdown.set_selected(option)     
        self.rgb_plane_changed.emit(color.value)
            