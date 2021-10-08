from sys import argv
from PyQt5.QtWidgets import QApplication 
from classes.main_window import MainWindow

app = QApplication(argv)
window = MainWindow()
window.show()
app.exec()
