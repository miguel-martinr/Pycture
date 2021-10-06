from PyQt5.QtWidgets import QAction, QWidget


class Command(QAction):
    def __init__(self, text: str, parent: QWidget) -> None:
        super(QAction, self).__init__(parent)
        self.setText(text)

    def run(self):  # Metaclass issue when making it abstract
        pass

class OpenFile(Command):
    def __init__(self, parent: QWidget) -> None:
        super(Command, self).__init__("Open", parent)
        self.triggered.connect(self.run)

    def run(self):
        print("Opens File and loads it in editor")

class SaveFile(Command):
    def __init__(self, parent: QWidget) -> None:
        super(Command, self).__init__("Save", parent)
        self.triggered.connect(self.run)

    def run(self):
        print("Saves File")

file_cmds = [OpenFile, SaveFile]



class EditBright(Command):
    def __init__(self, parent: QWidget) -> None:
        super(Command, self).__init__("Bright", parent)
        self.triggered.connect(self.run)

    def run(self):
        print("Edits bright")





edit_cmds = [EditBright]