from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QAction

ExecuteCommandEventType = QEvent.registerEventType()
DeleteEditorEventType = QEvent.registerEventType()
ChangeActiveEditorEventType = QEvent.registerEventType()
NewSelectionEventType = QEvent.registerEventType()
UpdateMousePositionEventType = QEvent.registerEventType()


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


class NewSelectionEvent(QEvent):
    def __init__(self, image: QPixmap):
        super().__init__(NewSelectionEventType)
        self.image = image


class UpdateMousePositionEvent(QEvent):
    def __init__(self, pos: (int, int), rgb: (int, int, int)):
        super().__init__(UpdateMousePositionEventType)
        self.pos = pos
        self.rgb = rgb
