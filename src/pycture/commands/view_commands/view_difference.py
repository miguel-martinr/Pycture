from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor, QImage

from pycture.dialogs import Notification, DifferenceDialog, MapOfChangesDialog
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

    def _show_difference_(self, image_a_title, image_b_title):

        self.image_a_editor: Editor = self.main_window.get_editor(
            image_a_title)

        self.image_b_editor: Editor = self.main_window.get_editor(
            image_b_title)

        image_a = self.image_a_editor.get_image()
        image_b = self.image_b_editor.get_image()

        if (image_a.height() != image_b.height()
                or image_a.width() != image_b.width()):
            Notification(
                self.dialog, "Image difference: Images must have the same dimensions")
            return False

        difference = image_a.get_difference(image_b)
        title = f" -  diff({image_a_title}, {image_b_title})"
        self.main_window.add_editor(
            difference, title)
        self.difference_editor = self.main_window.get_editor(title)
        return True

    def _update_histogram_view_(self, color_index: int):
        if (color_index < 0):
            return
        if (self.active_histogram):
            self.active_histogram.deleteLater()
        self.active_histogram = self.histograms[color_index](self.main_window)

        try:
            self.main_window.set_active_editor(
                self.difference_editor.windowTitle())
            self.active_histogram.execute(self.main_window)
        except KeyError as _:
            # Notification(self.main_window, "No difference image found")
            # return
            self._show_difference_(
                self.image_a_editor.windowTitle(), self.image_b_editor.windowTitle())
            
            self.difference_editor.get_image().loader.finished.connect(lambda: self.active_histogram.execute(self.main_window))
            self.main_window.set_active_editor(
                self.difference_editor.windowTitle())

    def mark_map_of_changes(self, treshold: int,
                            plane: Color, marker_color: QColor):
        marked_pixels_coordinates = self.difference_editor.get_image(
        ).get_pixels_coordinates(treshold, plane)
        map_of_changes = self.image_a_editor.get_image().mark_pixels(
            marked_pixels_coordinates, marker_color)
        self.main_window.add_editor(
            map_of_changes, f"Map of changes ({self.image_a_editor.windowTitle()} - {self.image_b_editor.windowTitle()})")

    def _trigger_map_of_changes_(self, image_a_title, image_b_title):
        self.map_dialog = MapOfChangesDialog(self.main_window)
        if (not self.difference_editor):
            difference_showed = self._show_difference_(
                image_a_title, image_b_title)
            if (not difference_showed):
                return
        self.map_dialog.rgb_plane_changed.connect(
            lambda color_index: self._update_histogram_view_(color_index))

        if (self.difference_editor.get_image().load_finished):
            self.map_dialog.rgb_plane_changed.emit(3)  # Gray scale by default
        else:
            self.difference_editor.get_image().loader.finished.connect(
                lambda: self.map_dialog.rgb_plane_changed.emit(3))  # Gray scale by default

        self.map_dialog.show()

        self.map_dialog.create_map.connect(self.mark_map_of_changes)

    def execute(self, main_window: QtWidgets.QMainWindow):
        self.main_window = main_window
        self.histograms = [ViewRedHistogram, ViewGreenHistogram,
                           ViewBlueHistogram, ViewGrayScaleHistogram]

        self.dialog = DifferenceDialog(
            main_window, main_window.get_editor_list())
        self.dialog.applied.connect(self._show_difference_)
        self.dialog.map_of_changes.connect(self._trigger_map_of_changes_)
