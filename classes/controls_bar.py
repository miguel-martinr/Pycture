from PyQt5.QtWidgets import QGridLayout, QMenuBar, QWidget
from classes.commands import OpenFile


class ControlsBar(QMenuBar):
    def __init__(self, parent: QWidget, layout: QGridLayout) -> None:
        super().__init__(parent)  
        self.parent = parent
        self.setUI(layout)
        

    def setUI(self, layout):
        
        layout.addWidget(self, 0, 0)
        actionFile = self.addMenu("File")
        actionFile.addAction(OpenFile(self))
        actionFile.addSeparator()



        # self.controls = []
        # buttons = [CmdBtn(text="Open", cmd=OpenFile())]
        # for btn in buttons:
        #     layout.addWidget(btn.getButton())
