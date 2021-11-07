from PyQt5 import QtWidgets
from pycture.dialogs.map_of_changes_dialog import MapOfChangesDialog

from pycture.dialogs.difference_dialog import DifferenceDialog
from pycture.dialogs.notification import Notification
from ..command import Command
from ...editor import Editor
from .view_histogram import ViewHistogram, ViewRedHistogram, ViewGreenHistogram, ViewBlueHistogram, ViewGrayScaleHistogram

class ViewDifference(Command):
    def __init__(self, parent: QtWidgets):
        self.active_histogram = None
        super().__init__(parent, "Difference")


    def _show_difference_(self, image_a_title, image_b_title):
        editor_a = self.main_window.get_editor(image_a_title)
        editor_b = self.main_window.get_editor(image_b_title)

        image_a = editor_a.get_image()
        image_b = editor_b.get_image()

        if (image_a.height() != image_b.height() or image_a.width() != image_b.width()):
            Notification(self.dialog, "Image difference: Images must have the same dimensions")
            return False
        
        difference = image_a.get_difference(image_b)
        self.main_window.add_editor(difference, f" -  diff({image_a_title}, {image_b_title})")
        return True

    def _update_histogram_view_(self, color_index: int):
        if (color_index < 0): return
        if (self.active_histogram): self.active_histogram.deleteLater()
        self.active_histogram = self.histograms[color_index]

        self.active_histogram.execute(self.main_window)

    def _trigger_map_of_changes_(self, image_a_title, image_b_title):
        difference_showed = self._show_difference_(image_a_title, image_b_title)
        if (not difference_showed): return
        map_dialog = MapOfChangesDialog(self.main_window)
        map_dialog.rgb_plane_changed.connect(lambda color_index: self._update_histogram_view_(color_index))
        map_dialog.rgb_plane_changed.emit(0)
        


    def execute(self, main_window: QtWidgets.QMainWindow):
        self.main_window = main_window
        histograms_parent = self.main_window
        self.histograms = [ViewRedHistogram, ViewGreenHistogram, ViewBlueHistogram, ViewGrayScaleHistogram]
        self.histograms = list(map(lambda vh: vh(histograms_parent), self.histograms))
  
        self.dialog = DifferenceDialog(main_window, main_window.get_editor_list())
        self.dialog.applied.connect(self._show_difference_)
        self.dialog.map_of_changes.connect(self._trigger_map_of_changes_)

        
