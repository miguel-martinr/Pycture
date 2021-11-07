from PyQt5 import QtGui
from PyQt5.QtCore import Qt, Signal
from PyQt5.QtGui import QColor, QColorConstants, QPainter, QPixmap
from PyQt5.QtWidgets import QColorDialog, QDialog, QGridLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget
from .segments_input import IntValidator

class MapOfChangesDialog(QDialog):
    create_map = Signal(int, QColor)

    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self._setup_()
        self.show()

    def _setup_(self):
        self.setWindowTitle("Map of changes")
        layout = QVBoxLayout()
        self.setLayout(layout)
        self._set_inputs_()
        self._set_btn_()

        maximum_width = 300
        self.setMinimumWidth(maximum_width)
        self.setMaximumWidth(maximum_width)

    
    def _set_inputs_(self):
        layout = QGridLayout()
        self.layout().addLayout(layout)

        treshold_label = QLabel("Treshold", self)
        layout.addWidget(treshold_label, 0, 0, Qt.AlignmentFlag.AlignLeft)

        self.treshold = QLineEdit('0', self)
        self.treshold.setValidator(IntValidator(0, 255))

        layout.addWidget(self.treshold, 0, 1, Qt.AlignmentFlag.AlignRight)

        marker_color_label = QLabel("Marker color", self)
        layout.addWidget(marker_color_label, 1, 0, Qt.AlignmentFlag.AlignLeft)
        
        self.marker_color = ColorPicker(self, QColor(0x00ff0000))
        layout.addWidget(self.marker_color, 1, 1)
        self.marker_color.setMaximumWidth(self.treshold.width())

    def _set_btn_(self):
        accept_btn = QPushButton("Create map", self)
        self.layout().addWidget(accept_btn)

        accept_btn.pressed.connect(self._create_map_)

    def _create_map_(self):
        self.create_map.emit(int(self.treshold.text()), self.marker_color.get_color())

class ColorPicker(QLabel):
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

    def get_color(self):
        return self.color
    
    def _get_html_color_(self, color: QColor = None):
        if (color == None): color = self.color
        html_color = '#' + hex(color.rgb())[2:]
        return html_color

    def _set_dialog_(self, initial_color: QColor):
        self.color_dialog = QColorDialog(QColor(initial_color), self) 
        self.color_dialog.setStyleSheet("background-color: black")
        self.color_dialog.setWindowFlags(Qt.WindowType.Window)

        self.color_dialog.colorSelected.connect(lambda color: self._set_color_(color))