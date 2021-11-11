from PyQt5.QtWidgets import QHBoxLayout, QWidget, QLabel, QLineEdit
from PyQt5.QtGui import QValidator

class PointInput(QWidget):
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
        return line_edit
        
    def get_point(self) -> (int, int):
        return (int(self.x.text()), int(self.y.text()))
 
