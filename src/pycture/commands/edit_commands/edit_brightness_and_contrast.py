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
        dialog.applied.connect(lambda brightness, contrast: 
            self.apply(main_window, brightness, contrast)
        )

    def apply(self, main_window: QMainWindow, brightness, contrast):
        brightness = list(brightness)
        contrast = list(contrast)
        image, title = self.get_active_image_and_title(main_window)
        if image is None:
            return

        self.recalculate(brightness, contrast, dialog, image)
        luts = [list(range(256)), list(range(256)), list(range(256))]
        for i in range(3):
            if (brightness[i][0] == brightness[i][1]
                    and contrast[i][0] == contrast[i][1]):
                continue
            lut = self.get_LUT(brightness[i], contrast[i])
            luts[i] = lut

        image = image.apply_LUTs(tuple(luts))

        main_window.add_editor(image, title + "-BrCt Edited")

    def get_LUT(self, brightness: Tuple[int], contrast: Tuple[int]):
        equation = self.get_equation(brightness, contrast)

        def get_vout(vin):
            vout = equation(vin)
            if (vout < 0):
                return 0
            if (vout > 255):
                return 255
            return vout

        lut = list(map(get_vout, range(256)))
        return lut

    def recalculate(self, brightness, contrast,
                    dialog: EditBrightnessAndContrastDialog, active_image: Image):
        brightness = list(brightness)
        contrast = list(contrast)
        # for i in range(4):
        #     if (brightness[i][0] == brightness[i][1]
        #             and contrast[i][0] == contrast[i][1]):
        #         brightness[i] = brightness[i][0]
        #         contrast[i] = contrast[i][0]
        #         continue
        #     lut = self.get_LUT(brightness[i], contrast[i])
        #     histogram = active_image.get_histogram(Color._value2member_map_[i])
        #     updated_histogram = [0] * 256

        #     for j, v in enumerate(histogram):
        #         updated_histogram[lut[j]] += v

        #     brightness[i] = round(self._get_mean_(updated_histogram))
        #     contrast[i] = round(self._get_sd_(updated_histogram))

        # dialog.update_values(brightness, contrast)

    def _get_mean_(self, histogram):
        mean = sum([histogram[i] * i for i in range(len(histogram))])
        return mean

    def _get_sd_(self, histogram):
        mean = self._get_mean_(histogram)
        variance = 0
        for i in range(256):
            variance += histogram[i] * (i - mean) ** 2
        return sqrt(variance)

    def get_equation(self, brightness, contrast):
        """
        @param brightness: (old_brightness, new_brightness)
        @param contrast: (old_contrast, new_contrast)
        """
        old_brightness, new_brightness = brightness
        old_contrast, new_contrast = contrast

        A = new_contrast / old_contrast
        B = new_brightness - A * old_brightness

        return lambda vin: round(A * vin + B)
