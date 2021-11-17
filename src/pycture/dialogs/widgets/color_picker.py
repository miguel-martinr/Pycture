from PyQt5.QtCore import Qt, Signal
from PyQt5.QtGui import QColor, QMouseEvent
from PyQt5.QtWidgets import QColorDialog, QLabel, QWidget

class ColorPicker(QLabel):
    color_changed = Signal(QColor)
    def __init__(self, parent: QWidget, initial_color: QColor):
        super().__init__(parent)
        self._set_color_(initial_color)
        self._set_dialog_(initial_color)

    def mousePressEvent(self, ev: QMouseEvent):
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
            lambda color: self._set_color_(color)
        )


