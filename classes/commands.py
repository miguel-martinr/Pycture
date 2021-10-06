from PyQt5.QtWidgets import QAction, QWidget

class Command(QAction):
    def __init__(self, parent : QWidget) -> None:
        super(QAction, self).__init__(parent)

    
    def run(self): # Metaclass issue when making it abstract
        pass

class OpenFile(Command):
    def __init__(self, parent: QWidget) -> None:
        super(Command, self).__init__(parent)
        self.setText("Abrir")
        self.triggered.connect(self.run)

    def run(self):
        print("Opens File and loads it in editor")

        
