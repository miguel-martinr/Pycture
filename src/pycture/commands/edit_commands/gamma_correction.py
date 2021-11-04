from PyQt5.QtWidgets import QMainWindow, QWidget

from pycture.dialogs.gamma_correction_dialog import GammaCorrectionDialog
from ..command import Command


class GammaCorrection(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Gamma correction")
    
    def gamma(self, a, gamma_value):
        b = a ** gamma_value
        return b

    def apply(self, gamma_value, main_window):
        active_image, title = self.get_active_image_and_title(main_window)
        if (not active_image): return

        # map a (Vin) in [0, 1]
        A = [a / 255 for a in range(256)]

        # apply gamma function
        B = [self.gamma(a, gamma_value) for a in A]

        # map b (Vout) in [0, 255]
        luts = [[round(b * 255) for b in B]] * 3
        new_image = active_image.apply_LUTs(luts)
        main_window.add_editor(new_image, title + f" (Gamma corrected - {gamma_value})")

    def execute(self, main_window: QMainWindow):
        active_image, title = self.get_active_image_and_title(main_window)
        if (not active_image): return

        dialog = GammaCorrectionDialog(main_window)
        dialog.applied.connect(lambda gamma_value: self.apply(gamma_value, main_window))

        
