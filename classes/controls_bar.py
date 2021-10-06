from PyQt5.QtWidgets import QGridLayout, QMenuBar, QWidget
from classes.cmd_menus import menus



class ControlsBar(QMenuBar):
    def __init__(self, parent: QWidget, layout: QGridLayout) -> None:
        super().__init__(parent)  
        
        self.setUI(layout)
        

    def setUI(self, layout):
        
        layout.addWidget(self, 0, 0)
        for menu in menus:
          someMenu = menu(self)
          self.addMenu(someMenu)
        

