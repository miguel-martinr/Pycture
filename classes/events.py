from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QPixmap

NewEditorEventType = QEvent.registerEventType()
DeleteEditorEventType = QEvent.registerEventType()
ChangeFocusedEditorEventType = QEvent.registerEventType()

class NewEditorEvent(QEvent):
    def __init__(self, image: QPixmap, image_name: str):
        super().__init__(NewEditorEventType)
        self.image = image
        self.image_name = image_name

class DeleteEditorEvent(QEvent):
    def __init__(self, editor_name: str):
        super().__init__(DeleteEditorEventType)
        self.editor_name = editor_name

class ChangedFocusedEditorEvent(QEvent):
    def __init__(self, editor_name: str):
        super().__init__(ChangeFocusedEditorEventType)
        self.editor_name = editor_name