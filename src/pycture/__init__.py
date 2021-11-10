from os import path

from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout
from PyQt5.QtGui import QImage, QGuiApplication
from PyQt5.QtCore import QEvent

from .menu_bar import MenuBar
from .editor import Editor
from .events import ExecuteCommandEvent, DeleteEditorEvent, ChangeActiveEditorEvent, NewSelectionEvent
from .css import PYCTURE_CSS


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pycture")
        self.setStyleSheet(PYCTURE_CSS)
        self.setMenuBar(MenuBar(self))
        placeholder_widget = QWidget()
        self.setCentralWidget(placeholder_widget)
        self.setup_size()
        self.editors = {}
        self.active_editor = None

    def setup_size(self):
        desktop_size = QGuiApplication.screens()[0].size()
        screen_width = desktop_size.width()
        screen_height = desktop_size.height()
        self.setMaximumSize(screen_width, screen_height)
        width = round(0.3 * screen_width)
        height = round(0.3 * screen_height)
        self.resize(width, height)
        self.move((screen_width - width) / 2, height / 2)


    def customEvent(self, event: QEvent):
        if isinstance(event, ExecuteCommandEvent):
            event.command.execute(self)
        elif isinstance(event, DeleteEditorEvent):
            if event.editor_name == self.active_editor:
                self.active_editor = None
            self.editors.pop(event.editor_name)
        elif isinstance(event, ChangeActiveEditorEvent):
            self.set_active_editor(event.editor_name)
        elif isinstance(event, NewSelectionEvent):
            title = self.get_active_editor().windowTitle() + "(Selection)"
            self.add_editor(event.image, title)

        else:
            event.ignore()

    def add_editor(self, image: QImage, name: str):
        while self.editors.get(name):
            (name, extension) = path.splitext(name)
            name = name + "+" + extension
        self.editors[name] = Editor(self, image, name)
        self.set_active_editor(name)

    def get_active_editor(self) -> Editor:
        return self.editors.get(self.active_editor)

    def get_editor(self, editor: str) -> Editor:
        return self.editors.get(editor)

    def set_active_editor(self, name: str):
        if (self.active_editor):
            self.editors[self.active_editor].set_active(False)
        self.active_editor = name
        self.editors[name].set_active(True)

    def get_editor_list(self) -> [Editor]:
        return self.editors
