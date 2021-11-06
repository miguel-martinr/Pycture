from typing import List
from PyQt5.QtWidgets import QMenu, QWidget
from PyQt5.QtCore import QCoreApplication

from pycture.commands.edit_commands import ConvertToGrayScale, TransformByLinearSegments
from pycture.commands import (Command, file_command_list, edit_command_list,
                              histogram_command_list, cumulative_histogram_command_list,
                              info_command_list, help_command_list, equalize_command_list)


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
        self.set_menu_commands(file_command_list)


class EditMenu(CommandMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setTitle("Edit")
        self.set_menu_commands(edit_command_list)
        self.set_menu_submenus([EqualizeMenu])


class ViewMenu(CommandMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setTitle("View")
        self.set_menu_submenus(
            [HistogramMenu, CumulativeHistogramMenu, ImageInfoMenu])


class HelpMenu(CommandMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setTitle("Help")
        self.set_menu_commands(help_command_list)

# EditMenu submenus


class EqualizeMenu(CommandMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setTitle("Equalize")
        self.set_menu_commands(equalize_command_list)

# ViewMenu submenus


class HistogramMenu(CommandMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setTitle("Histogram")
        self.set_menu_commands(histogram_command_list)


class CumulativeHistogramMenu(CommandMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setTitle("Cumulative histogram")
        self.set_menu_commands(cumulative_histogram_command_list)


class ImageInfoMenu(CommandMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setTitle("Info")
        self.set_menu_commands(info_command_list)


menus = [FileMenu, EditMenu, ViewMenu, HelpMenu]
