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
        dialog = GammaCorrectionDialog(main_window, main_window.get_editor_list())
        dialog.plot.connect(
            lambda gamma_value: self.plot(main_window, gamma_value)
        )
        dialog.applied.connect(lambda editor, gamma_value, color_options:
            self.apply(main_window, editor, gamma_value, color_options)
        )
        editor = main_window.get_active_editor_name()
        if editor is not None:
            dialog.set_dropdown_image(editor)

    def plot(self, main_window: QMainWindow, gamma_value: int):
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

    def apply(self, main_window: QMainWindow, editor: str,
            gamma_value: int, color_options: (int, int, int)
        ):
        image = main_window.get_editor(editor).get_image()
        if image is None:
            return

        lut = self.get_LUT(gamma_value)
        lut_or_none = lambda condition: lut if condition else None
        new_image = image.apply_LUTs((
            lut_or_none(color_options[0]),
            lut_or_none(color_options[1]),
            lut_or_none(color_options[2])
        ))
        main_window.add_editor(
            new_image, editor + f" (Gamma corrected - {gamma_value})"
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