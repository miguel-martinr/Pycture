from PyQt5.QtWidgets import QMenuBar, QWidget 
from PyQt5.QtCore import QCoreApplication
from classes.command_menus import menus

class ControlsBar(QMenuBar):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)  
        self.setStyleSheet("background-color: darkgray")
        self.setup_menus()
        
    def customEvent(self, event):
        QCoreApplication.sendEvent(self.parent(), event)

    def setup_menus(self):
        for menu in menus:
          someMenu = menu(self)
          self.addMenu(someMenu)
        

