from PyQt5.QtWidgets import QComboBox, QWidget
from PyQt5.QtGui import QMouseEvent


class DropdownList(QComboBox):
    def __init__(self, parent: QWidget, options: [str]):
        super().__init__(parent)
        self.options = options

    
    def set_selected(self, option: str):
        self.clear()
        self.addItem(option)
        
    # Update the options so they are consistent with new values
    # in the options list (remember the list is a reference)
    def mousePressEvent(self, event: QMouseEvent):
        self.clear()
        for option in self.options:
            self.addItem(option)
        super().mousePressEvent(event)
