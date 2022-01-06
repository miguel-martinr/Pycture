from PyQt5.QtWidgets import QWidget, QMainWindow
from ..command import Command
from .interpolation import bilinear_interpolation, nearest_neighbor_interpolation
from pycture.dialogs import ScaleDialog
from pycture.editor import Editor


class Scale(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Scale")
        self.interpolation_techniques = {
            "Nearest neighbour": nearest_neighbor_interpolation,
            "Bilinear": bilinear_interpolation,
        }

    def execute(self, main_window: QMainWindow):
        # Open dialog
        # Connect dialog button to rotate function
        self.main_window = main_window
        dialog = ScaleDialog(main_window, main_window.get_editor_list(), list(self.interpolation_techniques.keys()))
        dialog.set_editor(main_window.get_active_editor_name())
        dialog.set_interpolation_technique(
            list(self.interpolation_techniques.keys())[0])

        dialog.applied.connect(self.apply_scale)

    def apply_scale(self, 
        editor_title: str, interpolation_name: str, new_size: (int, int)
    ):
        editor = self.main_window.get_editor(editor_title)
        image = editor.get_image()
        title = editor.windowTitle()
        
        
        interpolation_technique = self.interpolation_techniques[interpolation_name]
        scaled_image = image.scale(new_size, interpolation_technique)
        self.main_window.add_editor(editor=Editor(
            self.main_window, scaled_image, title + ' scaled'))
