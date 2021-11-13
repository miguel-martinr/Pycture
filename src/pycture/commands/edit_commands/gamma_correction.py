from PyQt5.QtWidgets import QMainWindow, QWidget

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt

from pycture.dialogs import GammaCorrectionDialog
from pycture.dialogs.plot_window import PlotWindow
from ..command import Command


class GammaCorrection(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Gamma correction")

    def execute(self, main_window: QMainWindow):
        dialog = GammaCorrectionDialog(main_window)
        dialog.plot.connect(
            lambda gamma_value: self.plot(gamma_value, main_window)
        )
        dialog.applied.connect(
            lambda gamma_value: self.apply(gamma_value, main_window)
        )

    def plot(self, gamma_value: int, main_window: QMainWindow):
        # put 256 values in the x axis between 0 and 1
        x_values = [x / 255 for x in range(256)]
        # get the equivalent y with the respective gamma function
        y_values = [self.gamma(x, gamma_value) for x in x_values]

        plt.style.use('dark_background')
        title = f"Gamma correction - {gamma_value}"
        figure = plt.figure()
        plt.plot(x_values, y_values)
        plt.xlabel("Vin")
        plt.ylabel("Vout")
        PlotWindow(main_window, FigureCanvasQTAgg(figure), title)

    def apply(self, gamma_value: int, main_window: QMainWindow):
        active_image, title = self.get_active_image_and_title(main_window)
        if active_image is None:
            return

        lut = self.get_LUT(gamma_value)
        new_image = active_image.apply_LUTs((lut, lut, lut))
        main_window.add_editor(
            new_image, title + f" (Gamma corrected - {gamma_value})"
        )

    def get_LUT(self, gamma_value: int):
        # put 256 values in the x axis between 0 and 1
        x_values = [x / 255 for x in range(256)]
        # get the equivalent y with the respective gamma function
        y_values = [self.gamma(x, gamma_value) for x in x_values]

        # map the y values to the interval [0. 255]
        lut = [round(y * 255) for y in y_values]
        return lut

    def gamma(self, x, gamma_value):
        y = x ** gamma_value
        return y