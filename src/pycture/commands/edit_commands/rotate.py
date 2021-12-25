from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage
from pycture.commands.command import Command
from pycture.commands.edit_commands.interpolation import nearest_neighbor_interpolation
from pycture.dialogs.rotate_dialog import RotateDialog
from pycture.editor import Editor
from pycture.editor.image import Image
from math import ceil, cos, floor, sin, pi, sqrt
import numpy as np


class Rotate(Command):
    def __init__(self, parent: QtWidgets):
        super().__init__(parent, "Rotate")
        self.interpolation_techniques = {
            "Nearest Neighbour": nearest_neighbor_interpolation,
        }

    def apply_rotation(self, editor_title, interpolation_technique, angle):
        image, title = self.get_active_image_and_title(self.main_window)
        rotated_image = image.rotate(
            angle, self.interpolation_techniques[interpolation_technique])
        self.main_window.add_editor(editor=Editor(
            self.main_window, rotated_image, title + f' rotated {angle}º'))

    def execute(self, main_window: QtWidgets.QMainWindow):
        # Open dialog
        # Connect dialog button to rotate function
        self.main_window = main_window
        dialog = RotateDialog(main_window, main_window.get_editor_list())
        dialog.set_editor(main_window.get_active_editor_name())
        dialog.set_interpolation_technique(
            list(self.interpolation_techniques.keys())[0])

        dialog.applied.connect(self.apply_rotation)
