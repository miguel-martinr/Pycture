from sys import argv
from PyQt5.QtWidgets import QApplication 
from pycture import MainWindow

app = QApplication(argv)
window = MainWindow()
window.show()
app.exec()
