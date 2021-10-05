from PyQt5.QtWidgets import QHBoxLayout, QWidget

from cmd_btn import CmdBtn
from classes.commands import OpenFile


class ControlBar:
    def __init__(self, parent: QWidget) -> None:
        self.parent = parent
        self.setUI()

    def setUI(self):
        layout = QHBoxLayout(self.parent)

        buttons = [CmdBtn(text="Open", cmd=OpenFile())]
        for btn in buttons:
            layout.addWidget(btn.getButton())

