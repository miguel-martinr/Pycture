from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout
from cmd_btn import CmdBtn
from command import Command, OpenFile

from control_bar import ControlBar

app = QApplication([])
window = QWidget()


controlBar = ControlBar(parent=window)


# window.setLayout()
window.show()
app.exec()
