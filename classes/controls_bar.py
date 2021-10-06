from PyQt5.QtGui import QColorConstants, QPalette
from PyQt5.QtWidgets import QGridLayout, QMenuBar, QWidget
from classes.cmd_menus import menus



class ControlsBar(QMenuBar):
    def __init__(self, parent: QWidget, layout: QGridLayout) -> None:
        super().__init__(parent)  
        self.setUI(layout)
        

    def setUI(self, layout):   
        # self.setMaximumSize(200, 50)
        self.setStyleSheet("background-color: darkgray")
        layout.addWidget(self, 0, 0)
        for menu in menus:
          someMenu = menu(self)
          self.addMenu(someMenu)
        

