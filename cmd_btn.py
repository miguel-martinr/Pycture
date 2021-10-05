from PyQt5.QtWidgets import QPushButton
from classes.commands import Command


class CmdBtn:
    def __init__(self, text: str, cmd: Command) -> None:
        self.cmd = cmd
        self.text = text
        self.setButton()

    def setButton(self):
        self.btn = QPushButton(text=self.text)
        run = self.cmd.run
        
        self.btn.clicked.connect(lambda: self.cmd.run())

    def getButton(self) -> QPushButton:
        return self.btn

    def btnClicked(self):
        print("Hola")
        self.cmd.run()
