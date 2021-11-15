from typing import List

from PyQt5.QtCore import Qt, Signal
from PyQt5.QtWidgets import (
    QDialog, QHBoxLayout, QVBoxLayout, QLineEdit, QMainWindow, QPushButton,
    QSlider, QLayout, QLabel, QWidget, QSizePolicy
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt

from .widgets import CustomDoubleValidator, RGBCheckboxes, DropdownList
from .notification import Notification

def gamma(x, gamma_value):
    y = x ** gamma_value
    return y

class GammaCorrectionDialog(QDialog):
    applied = Signal(str, float, tuple) # Editor, gamma value and color options

    # Slider limit should never be less than or equal to 0
    def __init__(self, parent: QMainWindow, editors: List[str], slider_limit: int = 30) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Gamma correction")
        self.layout = QHBoxLayout()
        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(self.layout)
        self.slider_limit = slider_limit
        self.graph_figure = None
        
        self.setup_options_layout(editors)
        graph = self.plot_gamma()
        graph.setFixedSize(graph.size())
        self.layout.addWidget(graph)
        
        self.show()
        
    def setup_options_layout(self, editors: List[str]):
        options_layout = QVBoxLayout()
        self.layout.addLayout(options_layout)

        self.dropdown = DropdownList(self, editors)
        options_layout.addWidget(self.dropdown)

        self.checkboxes = RGBCheckboxes(self)
        options_layout.addWidget(self.checkboxes)

        label = QLabel("Gamma value:", self)
        options_layout.addWidget(label)

        self.setup_slider(options_layout)

        separator = QWidget()
        separator.setMinimumSize(0, 0)
        separator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        options_layout.addWidget(separator)

        accept_button = QPushButton("Apply", self)
        accept_button.clicked.connect(self.emit_applied)
        options_layout.addWidget(accept_button)

    def setup_slider(self, layout: QVBoxLayout):
        slider_layout = QHBoxLayout()
        layout.addLayout(slider_layout)

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setMinimum(2 - self.slider_limit)
        self.slider.setMaximum(self.slider_limit)
        self.slider.setValue(1)
        self.slider.setFixedWidth(200)
        slider_layout.addWidget(self.slider)

        self.numeric_input = QLineEdit("1", self)
        self.numeric_input.setValidator(CustomDoubleValidator(0, self.slider_limit, 4))
        slider_layout.addWidget(self.numeric_input)

        self.slider.valueChanged.connect(self.update_text_value)
        self.numeric_input.textEdited.connect(self.update_slider_value)
            
    # These changes are needed to smooth the values in the slider
    def update_text_value(self, slider_value: int):
        new_text_value = slider_value
        if slider_value < 1:
            new_text_value = 1 / (2 - slider_value)
        self.numeric_input.setText(str(round(new_text_value, 4)))
        self.update_graph()
        
    # These changes are needed to smooth the values in the slider
    def update_slider_value(self, text_value: str):
        value = self.text_to_double(text_value)
        if value < 1 / self.slider_limit:
            value = 2 - self.slider_limit
        elif value < 1:
            value = 2 - 1 / value
        self.slider.setValue(round(value))
        self.update_graph()

    def emit_applied(self):
        editor = self.dropdown.currentText()
        if self.parent().get_editor(editor) is None:
            Notification(self, "An active image must be chosen")
            return
        self.applied.emit(editor, self.get_gamma(), self.checkboxes.get_checked())

    def get_gamma(self):
        return max(self.text_to_double(self.numeric_input.text()), 1 / self.slider_limit)

    def text_to_double(self, text):
        return 0.0 if text == "" else float(text)

    def set_dropdown_image(self, editor: str):
        self.dropdown.set_selected(editor)

    def update_graph(self):
        new_graph = self.plot_gamma()
        new_graph.setFixedSize(new_graph.size())
        old_graph = self.layout.itemAt(1).widget()
        self.layout.removeWidget(old_graph)
        old_graph.deleteLater()
        self.layout.addWidget(new_graph)

    def plot_gamma(self) -> FigureCanvasQTAgg:
        gamma_value = self.get_gamma()
        # put 256 values in the x axis between 0 and 1
        x_values = [x / 255 for x in range(256)]
        # get the equivalent y with the respective gamma function
        y_values = [gamma(x, gamma_value) for x in x_values]

        plt.style.use('dark_background')
        title = f"Gamma correction - {gamma_value}"
        if self.graph_figure is not None:
            plt.close(self.graph_figure)
        self.graph_figure = plt.figure()
        plt.plot([0, 255], [0, 255])
        plt.xlabel("Vin")
        plt.ylabel("Vout")
        return FigureCanvasQTAgg(self.graph_figure)
