from PyQt5.QtWidgets import QWidget, QMainWindow

from pycture.dialogs import Notification, SelectTwoImagesDialog 
from pycture.editor import Editor
from pycture.editor.image import Image
from ..command import Command


class ViewDifference(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Difference")

    def execute(self, main_window: QMainWindow):
        self.main_window = main_window

        self.dialog = SelectTwoImagesDialog(
            main_window, main_window.get_editor_list(),
            main_window.get_active_editor_name(), "View Difference"
        )
        self.dialog.applied.connect(self._show_difference_)

    def _show_difference_(self, image_a_title: str, image_b_title: str):
        # SelectTwoImagesDialog ensures the titles are valid
        image_a = self.main_window.get_editor(image_a_title).get_image()
        image_b = self.main_window.get_editor(image_b_title).get_image()

        if (image_a.height() != image_b.height() or
            image_a.width() != image_b.width()
        ):
            Notification(self.dialog,
                "Image difference: Images must have the same dimensions"
            )
            return

        difference = image_a.get_difference(image_b)
        title = f" -  diff({image_a_title}, {image_b_title})"
        self.main_window.add_editor(difference, title)
        
