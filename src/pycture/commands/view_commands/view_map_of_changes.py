from PyQt5.QtCore import Signal

from pycture.dialogs.map_of_changes_dialog import MapOfChangesDialog
from pycture.editor import Editor
from pycture.editor.image import Image
from pycture.editor.image.color import RGBColor
from ..command import Command
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor, QImage


class ViewMapOfChanges(Command):

    map_changed = Signal(QImage)

    def __init__(self, parent: QtWidgets):
        self.is_setted = False
        super().__init__(parent, "Difference")

    def setup(self, base_image: Image, diff_image: Image, map_title: str):
        self.map_title = map_title
        self.base_image = base_image
        self.diff_image = diff_image
        self.is_setted = True

        self.map_changed.connect(self._show_map_)

    def _show_map_(self, map_image: QImage):

        map_editor = self.main_window.get_editor(self.map_title)
        
        if not map_editor:
            map_editor = Editor(self.main_window, map_image, self.map_title)
            self.main_window.add_editor(editor=map_editor)
        
        map_editor.set_image(map_image)


    def _update_map_(self, treshold: int, plane: RGBColor, marker_color: QColor):
        base_image = self.base_image
        diff_image = self.diff_image

        pixels_to_mark = diff_image.get_pixels_coordinates(treshold, plane)
        self.marked_image = base_image.mark_pixels(
            pixels_to_mark, marker_color)

        self.map_changed.emit(self.marked_image)

    def execute(self, main_window: QtWidgets.QMainWindow):
        if not self.is_setted:
            print("ViewMapOfChanges: command must be setted up before being executed")
            return

        self.main_window = main_window
        dialog = self.dialog = MapOfChangesDialog(main_window)
        dialog.treshold_changed.connect(self._update_map_)
        dialog.show()
