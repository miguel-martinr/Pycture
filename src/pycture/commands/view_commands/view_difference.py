from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor, QImage
from pycture.commands.view_commands.view_map_of_changes import ViewMapOfChanges

from pycture.dialogs import Notification, SelectTwoImagesDialog, MapOfChangesDialog
from pycture.editor.image import Image
from pycture.editor.image.color import Color, RGBColor
from ..command import Command
from pycture.editor import Editor
from .view_histogram import ViewHistogram, ViewRedHistogram, ViewGreenHistogram, ViewBlueHistogram, ViewGrayScaleHistogram


class ViewDifference(Command):
    def __init__(self, parent: QtWidgets):
        self.active_histogram = None
        self.map_dialog = None
        self.difference_editor = None
        super().__init__(parent, "Difference")

    def _show_difference_(self, image_a_title: str, image_b_title: str):

        self.image_a_editor: Editor = self.main_window.get_editor(
            image_a_title)
        
        if not self.image_a_editor:
            Notification(self.dialog, f"Image {image_a_title} not found")
            return
        
        self.image_b_editor: Editor = self.main_window.get_editor(
            image_b_title)
        
        if not self.image_b_editor:
            Notification(self.dialog, f"Image {image_b_title} not found")
            return

        image_a = self.image_a_editor.get_image()
        image_b = self.image_b_editor.get_image()

        if (image_a.height() != image_b.height()
                or image_a.width() != image_b.width()):
            Notification(
                self.dialog, "Image difference: Images must have the same dimensions")
            return

        difference = image_a.get_difference(image_b)
        title = f" -  diff({image_a_title}, {image_b_title})"
        self.main_window.add_editor(
            difference, title)
        self.difference_editor = self.main_window.get_editor(title)
        

    def execute(self, main_window: QtWidgets.QMainWindow):
        self.main_window = main_window

        self.dialog = SelectTwoImagesDialog(
            main_window, main_window.get_editor_list(), "View Difference")
        self.dialog.applied.connect(self._show_difference_)
