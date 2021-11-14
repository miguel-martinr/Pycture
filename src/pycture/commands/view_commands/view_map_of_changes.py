
from pycture import MainWindow
from pycture.dialogs.map_of_changes_dialog import MapOfChangesDialog
from pycture.editor import Editor
from pycture.editor.image import Image
from ..command import Command
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor, QImage

class ViewMapOfChanges(Command):
    def __init__(self, parent: QtWidgets):
        self.is_setted = False
        super().__init__(parent, "Difference")
        
        
    def _setup_(self, base_image: Image, diff_image: Image):
        self.base_image = base_image
        self.diff_image = diff_image
        self.is_setted = True
    
    def execute(self, main_window: QtWidgets.QMainWindow):
        
        if not self.is_setted:
            print("ViewMapOfChanges: command must be setted up before being executed")
            return
        
        dialog = self.dialog = MapOfChangesDialog(main_window)
        
        
        
        return super().execute(main_window)