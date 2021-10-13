from typing import List
from PyQt5.QtWidgets import QMenu, QWidget
from PyQt5.QtCore import QCoreApplication

from pycture.commands.view_commands import ViewBlueHistogram, ViewGrayScaleHistogram, ViewGreenHistogram, ViewRedHistogram
from pycture.commands.edit_commands import ToGrayScale
from ..commands import (Command, file_commands_list, edit_commands_list,
    red_view_commands_list, green_view_commands_list, blue_view_commands_list,
    gray_view_commands_list)

class CommandMenu(QMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def setMenuCommands(self, commands: List[Command]):
        for command in commands:
            self.addAction(command(self))
        
    def setMenuSubmenus(self, submenus: "List[CommandMenu]"):
        for submenu in submenus:
            self.addMenu(submenu(self))
        
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
        self.setMenuSubmenus([TransformMenu])
class ViewMenu(CommandMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setTitle("View")
        self.setMenuSubmenus([HistogramMenu])

class HistogramMenu(CommandMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setTitle("Histogram")
        self.setMenuCommands([ViewRedHistogram, ViewGreenHistogram, ViewBlueHistogram, ViewGrayScaleHistogram])

class TransformMenu(CommandMenu):
    def __init__(self, parent: QWidget):
      super().__init__(parent)
      self.setTitle("Transform")
      self.setMenuCommands([ToGrayScale])

menus = [FileMenu, EditMenu, ViewMenu]
