from PIL.ImageQt import QImage

from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPixmap, QMouseEvent, QGuiApplication
from PyQt5.QtCore import Signal, Qt 

from .image import Image


class ImageHolder(QLabel):
    mouse_position_updated = Signal(int, int, int, int, int)
    new_selection = Signal(QPixmap)

    def __init__(self, parent: QWidget, image: QImage):
        super().__init__(parent)
        self.setPixmap(QPixmap.fromImage(image))
        self.image = Image(image)

        self.setMouseTracking(True)
        self.setFixedHeight(image.height())
        self.setFixedWidth(image.width())
        self.press_pos = None

    def mouseMoveEvent(self, event: QMouseEvent):
        pos = (event.x(), event.y())
        rgb = self.image.get_pixel_rgb(pos[0], pos[1])
        if rgb is not None:
            self.mouse_position_updated.emit(*pos, *rgb)

    def mousePressEvent(self, event: QMouseEvent):
        if (event.button() == Qt.LeftButton and
                QGuiApplication.keyboardModifiers() == Qt.ControlModifier):
            self.press_pos = (event.x(), event.y())
        else:
            self.press_pos = None
        event.ignore()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if (event.button() != Qt.LeftButton or not self.press_pos or
                QGuiApplication.keyboardModifiers() != Qt.ControlModifier):
            return
        x_values = sorted([event.x(), self.press_pos[0]])
        y_values = sorted([event.y(), self.press_pos[1]])
        new_image = self.image.copy(
            x_values[0],
            y_values[0],
            x_values[1] - x_values[0],
            y_values[1] - y_values[0]
        )
        self.new_selection.emit(new_image)
        event.ignore()
