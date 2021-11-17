from PyQt5.QtCore import Qt, Signal
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QColor, QImage, QPixmap

from pycture.commands.view_commands.view_histogram import ViewBlueHistogram, ViewGrayScaleHistogram, ViewGreenHistogram, ViewHistogram, ViewRedHistogram
from pycture.dialogs import Notification, MapOfChangesDialog, PlotWindow, SelectTwoImagesDialog
from pycture.editor import Editor
from pycture.editor.image import Image, Color, RGBColor
from ..command import Command


class ViewMapOfChanges(Command):
    map_changed = Signal(QImage)
    images_selected = Signal(Image, Image)

    def __init__(self, parent: QWidget):
        super().__init__(parent, "Map of Changes")
        self.is_setted = False
        self.images_selected.connect(lambda: self._trigger_map_())

    def execute(self, main_window: QMainWindow):
        self.main_window = main_window

        self.map_dialog = MapOfChangesDialog(self.main_window)
        self.map_dialog.map_changed.connect(self._update_map_)
        self.map_dialog.save_current.connect(self._save_current_map_)
        self.map_dialog.rgb_plane_changed.connect(self._rgb_plane_changed_)

        select_images_dialog = SelectTwoImagesDialog(
            main_window, main_window.get_editor_list(),
            main_window.get_active_editor_name(), button_text="Create map"
        )
        select_images_dialog.applied.connect(
            lambda base_title, sample_title: self._images_selected_(
                base_title, sample_title, select_images_dialog
            )
        )

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
            image_holder = self.image_holder = QLabel(
                self.main_window, Qt.WindowType.Window
            )
            image_holder.setWindowTitle(self.map_title)

        image_holder.setPixmap(QPixmap.fromImage(map_image))
        image_holder.show()

    def _save_current_map_(self):
        try:
            image_holder = self.image_holder
        except KeyError:
            return

        self.main_window.add_editor(editor=Editor(
            self.main_window, image_holder.pixmap().toImage(), self.map_title
        ))

    def _update_map_(self, treshold: int, plane: RGBColor, marker_color: QColor):
        if not self.is_setted:
            print("ViewMapOfChanges: command must be setted up before being executed")
            return

        pixels_to_mark = self.diff_image.get_pixels_coordinates(treshold, plane)
        self.marked_image = self.base_image.mark_pixels(pixels_to_mark, marker_color)

        self.map_changed.emit(self.marked_image)

    def _images_selected_(self, base_title: str, sample_title: str, select_dialog: SelectTwoImagesDialog):
        select_dialog.deleteLater()
        # SelectTwoImagesDialog ensures the titles are valid
        base_editor = self.main_window.get_editor(base_title)
        base_image = base_editor.get_image()
        sample_editor = self.main_window.get_editor(sample_title)
        sample_image = sample_editor.get_image()

        diff_image = Image(base_image.get_difference(sample_image))
        
        # Shows difference image gray scale histogram by default 
        diff_image.loader.finished.connect(lambda: self.map_dialog.set_rgb_plane(Color.Gray))
        diff_image.start_load()

        self.setup(
            base_image, diff_image,
            f"MapOfChanges({base_editor.windowTitle()}, {sample_editor.windowTitle()})"
        )
        self.images_selected.emit(base_image, sample_image)

    def _trigger_map_(self):
        self.map_dialog.show()
        self.map_dialog._map_changed_()
        
    def _rgb_plane_changed_(self, color_index: int):
        if not self.diff_image.load_finished:
            Notification(self.main_window, "Image's still loading. Please wait a bit.")
            return
        
        histogram_commands = [
            ViewRedHistogram, ViewGreenHistogram,
            ViewBlueHistogram, ViewGrayScaleHistogram
        ]
        histogram_command = histogram_commands[color_index](None)
        
        color = Color._value2member_map_[color_index]
        histogram = self.diff_image.get_histogram(color)
        mean = self.diff_image.get_mean(color)
        title = histogram_command.get_title(self.map_title)
        figure = histogram_command.get_histogram_figure(histogram, mean, title)
        self.map_dialog.update_plot(
            PlotWindow(self.map_dialog, figure, title, Qt.WindowType.SubWindow)
        )
        