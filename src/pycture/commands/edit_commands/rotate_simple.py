from PyQt5.QtWidgets import QWidget, QMainWindow

from pycture.dialogs.rotate_simple_dialog import RotateSimpleDialog
from ..command import Command
from .interpolation import bilinear_interpolation, nearest_neighbor_interpolation
from pycture.dialogs import RotateDialog
from pycture.editor import Editor


class RotateSimple(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Rotate and paint")
        
    def apply_rotation(self, editor_title, angle):
        editor = self.main_window.editors.get(editor_title)
        image = editor.get_image()
        title = editor.windowTitle()
        
        rotated_image = image.rotate_simple(angle)
        
        str_angle = str(angle).replace(".", "'")
        self.main_window.add_editor(editor=Editor(
            self.main_window, rotated_image, title + f' rotated {str_angle}º'))

    def execute(self, main_window: QMainWindow):
        # Open dialog
        # Connect dialog button to rotate function
        self.main_window = main_window
        dialog = RotateSimpleDialog(main_window, main_window.get_editor_list())
        dialog.set_editor(main_window.get_active_editor_name())
        dialog.set_interpolation_technique(
            list(self.interpolation_techniques.keys())[0])

        dialog.applied.connect(self.apply_rotation)
