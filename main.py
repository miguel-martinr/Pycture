from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget
from classes.controls_bar import ControlsBar

app = QApplication([])
window = QWidget()

layout = QGridLayout()
window.setLayout(layout)
controlBar = ControlsBar(window, layout)
window.setWindowTitle("Pycture")

window.show()
app.exec()
