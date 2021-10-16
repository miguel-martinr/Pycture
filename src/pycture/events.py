from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QAction

ExecuteCommandEventType = QEvent.registerEventType()
DeleteEditorEventType = QEvent.registerEventType()
ChangeActiveEditorEventType = QEvent.registerEventType()
NewEditorEventType = QEvent.registerEventType()

class ExecuteCommandEvent(QEvent):
    def __init__(self, command: QAction):
        super().__init__(ExecuteCommandEventType)
        self.command = command

class DeleteEditorEvent(QEvent):
    def __init__(self, editor_name: str):
        super().__init__(DeleteEditorEventType)
        self.editor_name = editor_name

class ChangeActiveEditorEvent(QEvent):
    def __init__(self, editor_name: str):
        super().__init__(ChangeActiveEditorEventType)
        self.editor_name = editor_name

class NewEditorEvent(QEvent):
    def __init__(self, image: QPixmap, editor_name: str):
        super().__init__(NewEditorEventType)
        self.image = image
        self.editor_name = editor_name