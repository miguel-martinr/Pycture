from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage
from pycture.commands.command import Command
from pycture.commands.edit_commands.interpolation import nearest_neighbor_interpolation
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


    def rotation_matrix(self, angle_rad: float):
        return np.array(
            ((cos(angle_rad), -sin(angle_rad)),
             (sin(angle_rad), cos(angle_rad)))
        )

    def rotate(self, image: Image, angle_deg: float, interpolation_technique):
        angle_rad = angle_deg * (pi / 180)
        old_top_left = (0, 0)
        old_top_right = (image.width() - 1, 0)
        old_bottom_left = (0, image.height() - 1)
        old_bottom_right = (image.width() - 1, image.height() - 1)

        dt_rotation_matrix = self.rotation_matrix(angle_rad)
        it_rotation_matrix = self.rotation_matrix(-angle_rad)

        new_top_left = np.array(
            [floor(value) for value in np.dot(dt_rotation_matrix, old_top_left)])
        new_top_right = np.dot(dt_rotation_matrix, old_top_right)
        new_bottom_left = np.dot(dt_rotation_matrix, old_bottom_left)
        new_bottom_right = np.dot(dt_rotation_matrix, old_bottom_right)

        xs = [new_top_left[0], new_top_right[0],
              new_bottom_left[0], new_bottom_right[0]]
        ys = [new_top_left[1], new_top_right[1],
              new_bottom_left[1], new_bottom_right[1]]

        max_x = max(xs)
        max_y = max(ys)
        min_x = min(xs)
        min_y = min(ys)

        new_width = ceil(abs(max_x - min_x))
        new_height = ceil(abs(max_y - min_y))

        new_image = QImage(new_width, new_height, image.format())
        for indexXp in range(new_width):
            for indexYp in range(new_height):
                xp, yp = (indexXp + min_x, indexYp + min_y)
                x, y = np.dot(it_rotation_matrix, (xp, yp))

                if (0 <= x < image.width() and 0 <= y < image.height()):
                    new_image.setPixel(indexXp, indexYp, interpolation_technique(image, (x, y)))
                else:
                    new_image.setPixel(indexXp, indexYp, 0xffffff)
        return new_image

    def execute(self, main_window: QtWidgets.QMainWindow):
        # Open dialog
        # Connect dialog button to rotate function

        image, title = self.get_active_image_and_title(main_window)
        
        rotated_image = self.rotate(image, 211, self.interpolation_techniques['Nearest Neighbour'])
        main_window.add_editor(editor=Editor(
            main_window, rotated_image, title + ' rotated 45º'))
