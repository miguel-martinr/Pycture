from PyQt5.QtWidgets import QMenuBar, QWidget 
from PyQt5.QtCore import QCoreApplication, QEvent
from .command_menus import menus

class MenuBar(QMenuBar):
    def __init__(self, parent: QWidget):
        super().__init__(parent)  
        self.setStyleSheet("background-color: darkgray")
        self.setup_menus()
        
    def setup_menus(self):
        for menu in menus:
          someMenu = menu(self)
          self.addMenu(someMenu)

    def customEvent(self, event: QEvent):
        QCoreApplication.sendEvent(self.parent(), event)

        

