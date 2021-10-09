from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QAction

NewEditorEventType = QEvent.registerEventType()
DeleteEditorEventType = QEvent.registerEventType()
ChangeActiveEditorEventType = QEvent.registerEventType()

class NewEditorEvent(QEvent):
    def __init__(self, command: QAction):
        super().__init__(NewEditorEventType)
        self.command = command

class DeleteEditorEvent(QEvent):
    def __init__(self, editor_name: str):
        super().__init__(DeleteEditorEventType)
        self.editor_name = editor_name

class ChangeActiveEditorEvent(QEvent):
    def __init__(self, editor_name: str):
        super().__init__(ChangeActiveEditorEventType)
        self.editor_name = editor_name