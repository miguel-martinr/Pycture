from typing import Tuple
from PyQt5.QtWidgets import QWidget, QMainWindow
from pycture.dialogs import Notification
from pycture.editor.image.color import Color
from ..command import Command


class EditBrightness(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Brightness")


    def get_equation(self, brightness, contrast):
        """
        @param brightness: (old_brightness, new_brightness)
        @param contrast: (old_contrast, new_contrast)
        """
        old_brightness, new_brightness = brightness
        old_contrast, new_contrast = contrast

        A = old_contrast / new_contrast
        B = new_brightness - A * old_brightness
        
        return lambda vin: round(A * vin + B)
        
    def get_LUT(self, brightness: Tuple[int], contrast: Tuple[int]):
        equation = self.get_equation(brightness, contrast)    
        def get_vout(vin):
            vout = equation(vin)
            if (vout < 0): return 0
            if (vout > 255): return 255
            return vout

        lut = list(map(get_vout, range(256)))
        return lut
        
    def execute(self, main_window: QMainWindow):
        active_image = self.get_active_image(main_window)
        title = self.get_active_title(main_window)
        if active_image is None:
            notification = Notification(
                main_window, "There isn't an active editor!").exec()
            return
        if not active_image.load_finished:
            notification = Notification(main_window,
                                        "The image is still loading. Please wait a bit").exec()
            return

        old_brightness = active_image.get_brightness()[2]
        old_contrast = active_image.get_contrast()[2]
        new_brightness = 170
        new_contrast = 7
        
        lut = self.get_LUT((old_brightness, new_brightness), (old_contrast, new_contrast))
        new_image = active_image.apply_LUT(lut, (Color.Blue,))
        
        main_window.add_editor(new_image, title + "-BrCo")
        
        print("lut:" ,lut)
        print(f"Brightness: {active_image.get_brightness()[2]}")
        print(f"Contrast: {active_image.get_contrast()[2]}")




