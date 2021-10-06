from PyQt5.QtWidgets import QMenu, QWidget

from classes.commands import OpenFile

class CmdMenu(QMenu):
  def __init__(self, parent: QWidget):
    super(QMenu, self).__init__(parent)
    


class FileMenu(CmdMenu):
  def __init__(self, parent: QWidget):
      super(CmdMenu, self).__init__(parent)
      self.setTitle("File")
      self.setup()

  def setup(self):
      self.addAction(OpenFile(self))
      self.addSeparator()
  

  