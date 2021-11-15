from PyQt5.QtWidgets import QHBoxLayout, QWidget, QLabel, QLineEdit
from PyQt5.QtGui import QValidator
from PyQt5.QtCore import Signal

class PointInput(QWidget):
    point_changed = Signal() 

    def __init__(self, parent: QWidget, name: str, validator: QValidator):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.addWidget(QLabel(name, self))
        self.x = self.get_int_input(validator)
        self.layout.addWidget(self.x)
        self.y = self.get_int_input(validator)
        self.layout.addWidget(self.y)
        self.setLayout(self.layout)
    
    def get_int_input(self, validator: QValidator) -> QLineEdit:
        line_edit = QLineEdit("0")
        line_edit.setValidator(validator)
        line_edit.textChanged.connect(lambda: self.point_changed.emit())
        return line_edit
        
    def get_point(self) -> (int, int):
        text_to_int = lambda text: int(text) if len(text) > 0 else 0
        return (text_to_int(self.x.text()), text_to_int(self.y.text()))
 
