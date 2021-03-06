from PIL.ImageQt import QImage

from PyQt5.QtWidgets import QLabel, QWidget, QRubberBand
from PyQt5.QtGui import QPixmap, QMouseEvent, QGuiApplication
from PyQt5.QtCore import Signal, Qt, QRect

from .image import Image


class ImageHolder(QLabel):
    # Takes the position as (x, y) and the color as (r, g, b)
    mouse_position_updated = Signal(tuple, tuple)
    new_selection = Signal(QImage)

    def __init__(self, parent: QWidget, image: QImage):
        super().__init__(parent)
        self.setPixmap(QPixmap.fromImage(image))
        self.image = Image(image)

        self.setMouseTracking(True)
        self.setFixedHeight(image.height())
        self.setFixedWidth(image.width())
        self.press_pos = None
        self.rubberband = QRubberBand(QRubberBand.Rectangle, self)
        self.rubberband.hide()

    def mouseMoveEvent(self, event: QMouseEvent):
        pos = (event.x(), event.y())
        rgb = self.image.get_pixel_rgb(pos[0], pos[1])
        if rgb is not None:
            self.mouse_position_updated.emit(pos, rgb)
        if self.press_pos is not None:
            rect = self.Qrect_from_two_points(
                self.press_pos, (event.x(), event.y()))
            self.rubberband.setGeometry(rect)

    def mousePressEvent(self, event: QMouseEvent):
        if (event.button() == Qt.LeftButton and
                QGuiApplication.keyboardModifiers() == Qt.ControlModifier):
            self.press_pos = (event.x(), event.y())
            self.rubberband.setGeometry(*self.press_pos, 1, 1)
            self.rubberband.show()
        else:
            self.press_pos = None
        event.ignore()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if (event.button() != Qt.LeftButton or not self.press_pos or
                QGuiApplication.keyboardModifiers() != Qt.ControlModifier):
            return
        self.rubberband.hide()
        def clamp(x, lower, upper): return max(min(x, upper), lower)
        rect = self.Qrect_from_two_points(self.press_pos, (
            clamp(event.x(), 0, self.image.width()),
            clamp(event.y(), 0, self.image.height())
        ))
        new_image = self.image.copy(rect)
        self.new_selection.emit(new_image)
        event.ignore()

    def Qrect_from_two_points(self, point1: (
            int, int), point2: (int, int)) -> QRect:
        return QRect(
            min(point1[0], point2[0]),
            min(point1[1], point2[1]),
            abs(point1[0] - point2[0]),
            abs(point1[1] - point2[1])
        )
