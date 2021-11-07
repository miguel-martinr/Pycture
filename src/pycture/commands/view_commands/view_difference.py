from PyQt5 import QtWidgets

from pycture.dialogs.difference_dialog import DifferenceDialog
from pycture.dialogs.notification import Notification
from ..command import Command
from ...editor import Editor

class ViewDifference(Command):
    def __init__(self, parent: QtWidgets):
        super().__init__(parent, "Difference")


    def _show_difference_(self, image_a_title, image_b_title):
        editor_a = self.main_window.get_editor(image_a_title)
        editor_b = self.main_window.get_editor(image_b_title)

        image_a = editor_a.get_image()
        image_b = editor_b.get_image()

        if (image_a.height() != image_b.height() or image_a.width() != image_b.width()):
            Notification(self.dialog, "Image difference: Images must have the same dimensions")
            return
        
        difference = image_a.get_difference(image_b)
        _, title = self.get_active_image_and_title(self.main_window)
        self.main_window.add_editor(difference, title + f" -  diff({image_a_title}, {image_b_title})")
        

    def execute(self, main_window: QtWidgets.QMainWindow):
        self.main_window = main_window

        self.dialog = DifferenceDialog(main_window, main_window.get_editor_list())
        self.dialog.applied.connect(self._show_difference_)
        
