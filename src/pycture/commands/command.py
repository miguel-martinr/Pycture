from PyQt5.QtWidgets import QAction, QWidget, QMainWindow
from PyQt5.QtCore import QCoreApplication
from pycture.dialogs.notification import Notification

from pycture.editor.image import Image

from pycture.events import ExecuteCommandEvent


class Command(QAction):
    def __init__(self, parent: QWidget, text: str):
        super().__init__(parent)
        self.setText(text)
        self.triggered.connect(self.clicked)

    def clicked(self):
        QCoreApplication.sendEvent(self.parent(), ExecuteCommandEvent(self))

    def execute(self, main_window: QMainWindow):
        print("Executing base command")

    def get_active_image_and_title(self, main_window: QMainWindow) -> (Image, str):
        active_editor = main_window.get_active_editor()
        if active_editor is None:
            notification = Notification(
                main_window, "There isn't an active editor!").exec()
            return (None, None)
        image = active_editor.get_image()
        if not image.load_finished:
            notification = Notification(main_window,
                                        "The image is still loading. Please wait a bit").exec()
            return (None, None)
        return (image, active_editor.windowTitle())