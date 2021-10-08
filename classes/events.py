from PyQt5.QtCore import QEvent

OpenFileEventType = QEvent.registerEventType()

class OpenFileEvent(QEvent):
    def __init__(self):
        super().__init__(OpenFileEventType)