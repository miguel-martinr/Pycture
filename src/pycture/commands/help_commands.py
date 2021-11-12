from PyQt5.QtWidgets import QWidget, QMainWindow

from .command import Command
from pycture.dialogs import Notification

HELP_MESSAGE = """
• You can apply different operations to the selected editor with the menus in the top bar.
• You can also open a smaller selection of an image pressing CTRL and dragging over an editor.
"""


class ShowHelp(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Show help")

    def execute(self, main_window: QMainWindow):
        Notification(main_window, HELP_MESSAGE)
