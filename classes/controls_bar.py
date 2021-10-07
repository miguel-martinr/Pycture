from PyQt5.QtWidgets import QMenuBar, QWidget 
from classes.cmd_menus import menus

class ControlsBar(QMenuBar):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)  
        self.setStyleSheet("background-color: darkgray")
        self.setup_menus()
        

    def setup_menus(self):
        for menu in menus:
          someMenu = menu(self)
          self.addMenu(someMenu)
        

