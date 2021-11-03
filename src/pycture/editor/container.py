from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QAbstractScrollArea
from PyQt5.QtCore import Qt, QEvent, QCoreApplication

from .image_holder import Image, ImageHolder
from .data_bar import DataBar
from ..events import UpdateMousePositionEvent, NewSelectionEvent


class Container(QWidget):
    def __init__(self, parent: QWidget, image: QImage):
        super().__init__(parent)
        layout = QVBoxLayout()
        scroll_area = QScrollArea(self)
        self.image_holder = ImageHolder(scroll_area, image)
        scroll_area.setWidget(self.image_holder)
        scroll_area.setMaximumWidth(image.width() + 15)
        scroll_area.setMaximumHeight(image.height() + 15)
        scroll_area.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        scroll_area.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        layout.addWidget(scroll_area)
        layout.setSpacing(0)
        self.data_bar = DataBar(self)
        layout.addWidget(self.data_bar)
        layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.setLayout(layout)

        self.image_holder.mouse_position_updated.connect(self.update_data_bar)
        self.image_holder.new_selection.connect(self.throw_new_selection_event)

    def get_image(self) -> Image:
        return self.image_holder.image

    def update_data_bar(self, x: int, y: int, r: int, g: int, b: int):
        self.data_bar.update_data((x, y), (r, g, b))

    def throw_new_selection_event(self, image: QImage):
        QCoreApplication.sendEvent(self.parent(), NewSelectionEvent(image))

    def customEvent(self, event: QEvent):
        QCoreApplication.sendEvent(self.parent(), event)
