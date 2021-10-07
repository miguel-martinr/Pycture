from typing import List
from PyQt5.QtWidgets import QMenu, QWidget
from classes.commands import Command, file_cmds, edit_cmds

class CmdMenu(QMenu):
  def __init__(self, parent: QWidget):
    super().__init__(parent)

  def setMenuCmds(self, cmds: List[Command]):
    for cmd in cmds:
      self.addAction(cmd(self))

class FileMenu(CmdMenu):
  def __init__(self, parent: QWidget):
      super().__init__(parent)
      self.setTitle("File")
      self.setMenuCmds(file_cmds)
      
class EditMenu(CmdMenu):
  def __init__(self, parent: QWidget):
      super().__init__(parent)
      self.setTitle("Edit")
      self.setMenuCmds(edit_cmds)
  
menus = [FileMenu, EditMenu]