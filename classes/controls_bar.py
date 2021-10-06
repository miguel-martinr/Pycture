from PyQt5.QtWidgets import QGridLayout, QMenuBar, QWidget
from classes.cmd_menus import FileMenu
from classes.commands import OpenFile


class ControlsBar(QMenuBar):
    def __init__(self, parent: QWidget, layout: QGridLayout) -> None:
        super().__init__(parent)  
        self.parent = parent
        self.setUI(layout)
        

    def setUI(self, layout):
        
        layout.addWidget(self, 0, 0)
        fileMenu = FileMenu(self)
        self.addMenu(fileMenu)

