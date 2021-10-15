from typing import List
from PyQt5.QtWidgets import QMenu, QWidget
from PyQt5.QtCore import QCoreApplication

from pycture.commands.view_commands import ViewBlueHistogram, ViewGrayScaleHistogram, ViewGreenHistogram, ViewImageBrightness, ViewImageContrast, ViewImageEntropy, ViewImageRanges, ViewImageSize, ViewRedHistogram, ViewImageInfo
from pycture.commands.edit_commands import ToGrayScale
from ..commands import (Command, file_commands_list, edit_commands_list,
    red_view_commands_list, green_view_commands_list, blue_view_commands_list,
    gray_view_commands_list)

class CommandMenu(QMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def set_menu_commands(self, commands: List[Command]):
        for command in commands:
            self.addAction(command(self))
        
    def set_menu_submenus(self, submenus: "List[CommandMenu]"):
        for submenu in submenus:
            self.addMenu(submenu(self))
        
    def customEvent(self, event):
        QCoreApplication.sendEvent(self.parent(), event)

class FileMenu(CommandMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setTitle("File")
        self.set_menu_commands(file_commands_list)
      
class EditMenu(CommandMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setTitle("Edit")
        self.set_menu_commands(edit_commands_list)
        self.set_menu_submenus([TransformMenu])
class ViewMenu(CommandMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setTitle("View")
        self.set_menu_submenus([HistogramMenu, ImageInfoMenu])


# ViewMenu submenus
class HistogramMenu(CommandMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setTitle("Histogram")
        self.set_menu_commands([ViewRedHistogram, ViewGreenHistogram, ViewBlueHistogram, ViewGrayScaleHistogram])

class ImageInfoMenu(CommandMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setTitle("Info")
        self.setMenuCommands([ViewImageBrightness, ViewImageSize, ViewImageContrast, ViewImageEntropy, ViewImageRanges])


# EditMenu submenus
class TransformMenu(CommandMenu):
    def __init__(self, parent: QWidget):
      super().__init__(parent)
      self.setTitle("Transform")
      self.set_menu_commands([ToGrayScale])


menus = [FileMenu, EditMenu, ViewMenu]