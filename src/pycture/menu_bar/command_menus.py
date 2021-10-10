from PyQt5.QtWidgets import QMenu, QWidget
from PyQt5.QtCore import QCoreApplication
from ..commands import Command, file_commands_list, edit_commands_list, view_commands_list

class CommandMenu(QMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def setMenuCommands(self, commands: [Command]):
        for command in commands:
            self.addAction(command(self))
        
    def customEvent(self, event):
        QCoreApplication.sendEvent(self.parent(), event)

class FileMenu(CommandMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setTitle("File")
        self.setMenuCommands(file_commands_list)
      
class EditMenu(CommandMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setTitle("Edit")
        self.setMenuCommands(edit_commands_list)

class ViewMenu(CommandMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setTitle("View")
        self.setMenuCommands(view_commands_list)
  
menus = [FileMenu, EditMenu, ViewMenu]