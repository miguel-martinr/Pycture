from math import sqrt
from typing import Tuple

from PyQt5.QtWidgets import QWidget, QMainWindow

from pycture.dialogs import EditBrightnessAndContrastDialog
from pycture.editor.image import Image
from pycture.editor.image.color import Color

from ..command import Command


class EditBrightnessAndContrast(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Brightness and Contrast")

    def execute(self, main_window: QMainWindow):
        dialog = EditBrightnessAndContrastDialog(
            main_window, main_window.get_editor_list()
        )
        dialog.applied.connect(lambda editor, brightness, contrast: 
            self.apply(main_window, editor, brightness, contrast)
        )
        editor = main_window.get_active_editor_name()
        if editor is not None:
            dialog.set_dropdown_image(editor)

    def apply(self, main_window: QMainWindow, editor: str,
        brightness: (float, float, float), contrast: (float, float, float)
    ):
        # get_editor won't return None, because the dialog will never
        # return an editor name that isn't valid
        image = main_window.get_editor(editor).get_image()
        old_brightness = image.get_brightness()
        old_contrast = image.get_contrast()
        luts = [list(range(256)) for _ in range(3)]
        for i in range(3):
            if (brightness[i] == old_brightness[i]
                and contrast[i] == old_contrast[i]
            ):
                continue
            luts[i] = self.get_LUT(
                (old_brightness[i], brightness[i]),
                (old_contrast[i], contrast[i])
            )

        image = image.apply_LUTs(tuple(luts))
        main_window.add_editor(image, editor + "-BrCt Edited")

    def get_LUT(self, brightness: Tuple[float], contrast: Tuple[float]):
        equation = self.get_equation(brightness, contrast)
        clamp = lambda x: min(max(x, 0), 255)
        lut = list(map(lambda x: clamp(equation(x)), range(256)))
        return lut

    def get_equation(self, brightness, contrast):
        """
        @param brightness: (old_brightness, new_brightness)
        @param contrast: (old_contrast, new_contrast)
        """
        old_brightness, new_brightness = brightness
        old_contrast, new_contrast = contrast

        # Even if the contrast can theoretically be zero 
        # we can't allow a division by zero 
        A = new_contrast / max(old_contrast, 0.0001)
        B = new_brightness - A * old_brightness

        return lambda vin: round(A * vin + B)
