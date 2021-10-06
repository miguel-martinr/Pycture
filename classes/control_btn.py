from PyQt5.QtWidgets import QPushButton, QWidget
from abc import ABC, abstractmethod


class ControlBtn(ABC):
    def __init__(self, text: str, parent: QWidget) -> None:
        self.text = text
        self.parent = parent
        self.button = QPushButton(text=self.text, parent=self.parent)

    @abstractmethod
    def setMenu(self):
        pass

    def getButton(self):
        return self.button


class FileControlBtn(ControlBtn):
    def __init__(self, text: str, parent: QWidget) -> None:
        super().__init__(text, parent)

    def setMenu(self):
        return super().setMenu()
