from PyQt5.QtWidgets import QMainWindow, QWidget
import matplotlib.pyplot as plt
from pycture.dialogs.gamma_correction_dialog import GammaCorrectionDialog
from ..command import Command


class GammaCorrection(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Gamma correction")

    def gamma(self, a, gamma_value):
        b = a ** gamma_value
        return b

    def get_LUTs(self, gamma_value):
          # map a (Vin) in [0, 1]
        A = [a / 255 for a in range(256)]

        # apply gamma function
        B = [self.gamma(a, gamma_value) for a in A]

        # map b (Vout) in [0, 255]
        luts = [[round(b * 255) for b in B]] * 3
        return luts

    def apply(self, gamma_value, main_window):
        active_image, title = self.get_active_image_and_title(main_window)
        if (not active_image):
            return

        luts = self.get_LUTs(gamma_value)
        new_image = active_image.apply_LUTs(luts)
        main_window.add_editor(
            new_image, title + f" (Gamma corrected - {gamma_value})")

    def plot(self, gamma_value):
        # map a (Vin) in [0, 1]
        A = [a / 255 for a in range(256)]

        # apply gamma function
        B = [self.gamma(a, gamma_value) for a in A]
        
        plt.style.use('dark_background')
        plt.clf()
        plt.interactive(True)
        plt.plot(A, B)
        plt.xlabel("a")
        plt.ylabel("b")
        plt.title(f"Gamma correction - {gamma_value}")
        plt.show()
        

    def execute(self, main_window: QMainWindow):
        active_image, title = self.get_active_image_and_title(main_window)
        if (not active_image):
            return

        dialog = GammaCorrectionDialog(main_window)
        dialog.applied.connect(
            lambda gamma_value: self.apply(gamma_value, main_window))
        dialog.plot.connect(
            lambda gamma_value: self.plot(gamma_value))
