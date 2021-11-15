from PyQt5.QtCore import Qt, Signal
from pycture.dialogs import Notification

from pycture.dialogs.map_of_changes_dialog import MapOfChangesDialog
from pycture.dialogs.select_two_images_dialog import SelectTwoImagesDialog
from pycture.editor import Editor, image_holder
from pycture.editor import image
from pycture.editor.image import Image
from pycture.editor.image.color import RGBColor
from ..command import Command
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor, QImage, QPixmap


class ViewMapOfChanges(Command):
    map_changed = Signal(QImage)
    images_selected = Signal(Image, Image)

    def __init__(self, parent: QtWidgets):
        super().__init__(parent, "Map of Changes")
        self.is_setted = False
        self.images_selected.connect(lambda: self._trigger_map_())

    def setup(self, base_image: Image, diff_image: Image, map_title: str):
        self.map_title = map_title
        self.base_image = Image(base_image)
        self.diff_image = diff_image
        self.is_setted = True

        self.map_changed.connect(self._show_map_)

    def _show_map_(self, map_image: QImage):
        try:
            image_holder = self.image_holder
        except AttributeError:
            image_holder = self.image_holder = QtWidgets.QLabel(self.main_window, Qt.WindowType.Window)
            image_holder.setWindowTitle(self.map_title)
            
        image_holder.setPixmap(QPixmap.fromImage(map_image))
        image_holder.show()
            
            
    def _save_current_map_(self):
        try:
            image_holder = self.image_holder
        except KeyError:
            return
        
        self.main_window.add_editor(editor=Editor(self.main_window, image_holder.pixmap().toImage(), self.map_title))

    def _update_map_(self, treshold: int, plane: RGBColor, marker_color: QColor):
        if not self.is_setted:
            print("ViewMapOfChanges: command must be setted up before being executed")
            return

        base_image = self.base_image
        diff_image = self.diff_image

        pixels_to_mark = diff_image.get_pixels_coordinates(treshold, plane)
        self.marked_image = base_image.mark_pixels(
            pixels_to_mark, marker_color)

        self.map_changed.emit(self.marked_image)

    def _images_selected_(self, base_title: str, sample_title: str, select_dialog: SelectTwoImagesDialog):
        base_editor = self.main_window.get_editor(base_title)
        if not base_editor:
            Notification(self.map_dialog, f"Image {base_title} not found")
            return

        sample_editor = self.main_window.get_editor(sample_title)
        if not sample_editor:
            Notification(self.map_dialog, f"Image {sample_title} not found")
            return

        base_image = base_editor.get_image()
        sample_image = sample_editor.get_image()
        diff_image = Image(base_image.get_difference(sample_image))
        
        self.setup(base_image, diff_image,
                   f"MapOfChanges({base_editor.windowTitle()}, {sample_editor.windowTitle()})")
        select_dialog.deleteLater()
        self.images_selected.emit(base_image, sample_image)
                
    def _trigger_map_(self):
        self.map_dialog.show()
        self.map_dialog._map_changed_()
        
    def execute(self, main_window: QtWidgets.QMainWindow):
        self.main_window = main_window
        
        self.map_dialog = self.map_dialog = MapOfChangesDialog(self.main_window)
        self.map_dialog.map_changed.connect(self._update_map_)
        self.map_dialog.save_current.connect(self._save_current_map_)
        

        select_images_dialog = SelectTwoImagesDialog(
            main_window, main_window.get_editor_list(), button_text="Create map")
        select_images_dialog.applied.connect(lambda base_title, sample_title: self._images_selected_(
            base_title, sample_title, select_images_dialog))
