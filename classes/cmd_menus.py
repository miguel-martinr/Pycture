from typing import List
from PyQt5.QtWidgets import QMenu, QWidget
from classes.commands import Command, file_cmds, edit_cmds

class CmdMenu(QMenu):
  def __init__(self, parent: QWidget):
    super(QMenu, self).__init__(parent)
    self.setStyleSheet("background-color: gray;")
    



def setMenuCmds(self: CmdMenu, cmds: List[Command]):
  for cmd in cmds:
    self.addAction(cmd(self))

class FileMenu(CmdMenu):
  def __init__(self, parent: QWidget):
      super(CmdMenu, self).__init__(parent)
      self.setTitle("File")
      setMenuCmds(self, file_cmds) # Issues when adding it as CmdMenu method
      
class EditMenu(CmdMenu):
  def __init__(self, parent: QWidget):
      super(CmdMenu, self).__init__(parent)
      self.setTitle("Edit")
      setMenuCmds(self, edit_cmds) # Issues when adding it as CmdMenu method
  
menus = [FileMenu, EditMenu]