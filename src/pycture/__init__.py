from os import path

from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QEvent

from .menu_bar import MenuBar
from .editor import Editor
from .events import ExecuteCommandEvent, DeleteEditorEvent, ChangeActiveEditorEvent, NewEditorEvent


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pycture")
        self.setMenuBar(MenuBar(self))
        placeholder_widget = QWidget()
        placeholder_widget.setLayout(QGridLayout())
        self.setCentralWidget(placeholder_widget)
        self.editors = {}
        self.active_editor = None

    def customEvent(self, event: QEvent):
        if isinstance(event, ExecuteCommandEvent):
            event.command.execute(self)
        elif isinstance(event, DeleteEditorEvent):
            if event.editor_name == self.active_editor:
                self.active_editor = None
            self.editors.pop(event.editor_name)
        elif isinstance(event, ChangeActiveEditorEvent):
            self.set_active_editor(event.editor_name)
        elif isinstance(event, NewEditorEvent):
            self.add_editor(event.image, event.editor_name)

        else:
            event.ignore()

    def add_editor(self, image: QPixmap, name: str):
        while self.editors.get(name):
            (name, extension) = path.splitext(name)
            name = name + "+" + extension
        self.editors[name] = Editor(self, image, name)
        self.set_active_editor(name)

    def get_active_editor(self) -> Editor:
        return self.editors.get(self.active_editor)

    def set_active_editor(self, name: str):
        if (self.active_editor):
            self.editors[self.active_editor].set_active(False)
        self.active_editor = name
        self.editors[name].set_active(True)
