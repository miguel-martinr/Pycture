from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QPixmap

NewEditorEventType = QEvent.registerEventType()

class NewEditorEvent(QEvent):
    def __init__(self, image: QPixmap, image_name: str):
        super().__init__(NewEditorEventType)
        self.image = image
        self.image_name = image_name