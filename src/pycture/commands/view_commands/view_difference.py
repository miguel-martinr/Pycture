from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor, QImage
from pycture.dialogs.map_of_changes_dialog import MapOfChangesDialog

from pycture.dialogs.difference_dialog import DifferenceDialog
from pycture.dialogs.notification import Notification
from pycture.editor.image import Image
from pycture.editor.image.color import RGBColor
from ..command import Command
from ...editor import Editor
from .view_histogram import ViewHistogram, ViewRedHistogram, ViewGreenHistogram, ViewBlueHistogram, ViewGrayScaleHistogram


class ViewDifference(Command):
    def __init__(self, parent: QtWidgets):
        self.active_histogram = None
        self.map_dialog = None
        super().__init__(parent, "Difference")

    def _show_difference_(self, image_a_title, image_b_title):
        self.image_a_title = image_a_title
        self.image_b_title = image_b_title
        editor_a = self.main_window.get_editor(image_a_title)
        editor_b = self.main_window.get_editor(image_b_title)

        image_a = editor_a.get_image()
        image_b = editor_b.get_image()
        self.image_a = image_a

        if (image_a.height() != image_b.height() or image_a.width() != image_b.width()):
            Notification(
                self.dialog, "Image difference: Images must have the same dimensions")
            return False

        difference = image_a.get_difference(image_b)
        self.main_window.add_editor(
            difference, f" -  diff({image_a_title}, {image_b_title})")
        self.difference = self.main_window.get_active_editor().get_image()
        if (self.map_dialog):
            self.difference.worker.finished.connect(
                lambda: self.map_dialog.rgb_plane_changed.emit(0))

        return (image_a, difference)

    def _update_histogram_view_(self, color_index: int):
        if (color_index < 0):
            return
        if (self.active_histogram):
            self.active_histogram.deleteLater()
        self.active_histogram = self.histograms[color_index](self.main_window)

        self.active_histogram.execute(self.main_window)

    def mark_map_of_changes(self, treshold: int, rgb_plane: RGBColor, marker_color: QColor):
        marked_pixels_coordinates = self.difference.get_pixels_coordinates(treshold, rgb_plane)
        map_of_changes = self.image_a.mark_pixels(
            marked_pixels_coordinates, marker_color)
        self.main_window.add_editor(
            map_of_changes, f"Map of changes ({self.image_a_title} - {self.image_b_title})")

    def _trigger_map_of_changes_(self, image_a_title, image_b_title):
        self.map_dialog = MapOfChangesDialog(self.main_window)
        difference_result = self._show_difference_(
            image_a_title, image_b_title)
        if (not difference_result):
            return
        
        self.map_dialog.show()
        image_a, difference = difference_result

        self.map_dialog.rgb_plane_changed.connect(
            lambda color_index: self._update_histogram_view_(color_index))
        self.map_dialog.create_map.connect(self.mark_map_of_changes)

    def execute(self, main_window: QtWidgets.QMainWindow):
        self.main_window = main_window
        self.histograms = [ViewRedHistogram, ViewGreenHistogram,
                           ViewBlueHistogram, ViewGrayScaleHistogram]

        self.dialog = DifferenceDialog(
            main_window, main_window.get_editor_list())
        self.dialog.applied.connect(self._show_difference_)
        self.dialog.map_of_changes.connect(self._trigger_map_of_changes_)
