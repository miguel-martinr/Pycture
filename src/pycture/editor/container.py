from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QAbstractScrollArea, QProgressBar
from PyQt5.QtCore import Qt, QEvent, QCoreApplication

from .image_holder import Image, ImageHolder
from .data_bar import DataBar
from ..events import UpdateMousePositionEvent, NewSelectionEvent


class Container(QWidget):
    def __init__(self, parent: QWidget, image: QImage):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.setup_scroll_area(image)
        self.get_image().loader.progress.connect(self.update_progress_bar)
        self.get_image().start_load()
        self.data_bar = DataBar(self)
        self.layout.addWidget(self.data_bar)
        self.progress_bar = None

        self.image_holder.mouse_position_updated.connect(
            self.data_bar.update_data
        )
        self.image_holder.new_selection.connect(
            self.throw_new_selection_event
        )

    def setup_scroll_area(self, image: QImage):
        scroll_area = QScrollArea(self)
        self.image_holder = ImageHolder(scroll_area, image)
        scroll_area.setWidget(self.image_holder)
        scroll_area.setMaximumWidth(image.width() + 15)
        scroll_area.setMaximumHeight(image.height() + 15)
        scroll_area.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        scroll_area.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.layout.addWidget(scroll_area)

    def update_progress_bar(self, value: int):
        if self.progress_bar is None:
            self.setup_progress_bar()
        self.progress_bar.setValue(value)
        if value == 100:
            self.layout.removeWidget(self.progress_bar)
            self.progress_bar = None

    def setup_progress_bar(self):
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setFixedWidth(self.data_bar.width())
        self.layout.addWidget(self.progress_bar)
        
    def get_image(self) -> Image:
        return self.image_holder.image

    def throw_new_selection_event(self, image: QImage):
        QCoreApplication.sendEvent(self.parent(), NewSelectionEvent(image))

    def customEvent(self, event: QEvent):
        QCoreApplication.sendEvent(self.parent(), event)
