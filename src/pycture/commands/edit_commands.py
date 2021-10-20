from PIL.ImageQt import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog, QWidget, QMainWindow

from pycture.dialogs.input_dialogs import SegmentsInput

from .command import Command


class EditBrightnessCommand(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Brightness")

    def execute(self, main_window: QMainWindow):
        print("Edits brightness")


class ToGrayScale(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Gray scale (NTSC)")

    def execute(self, main_window: QMainWindow):
        image = self.get_active_image(main_window)
        title = self.get_active_title(main_window)
        if image == None:
            print("Gray scale transformation: No image found")
            return  # TODO: Notify the user properly

        gray_scaled_image = image.get_gray_scaled_image()
        main_window.add_editor(QPixmap.fromImage(
            gray_scaled_image), title + "(GrayScaled)")


class transform_by_linear_segments(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "By linear segments")

    def get_num_of_segments(self, main_window: QMainWindow) -> QWidget:
        dialog = QInputDialog(main_window)
        dialog.setInputMode(QInputDialog.InputMode.IntInput)
        dialog.setIntMinimum(1)
        dialog.setIntMaximum(5)
        dialog.setWindowTitle("Linear segments transformation")
        dialog.setLabelText("Number of segments:")
        dialog.resize(300, 300)
        ok = dialog.exec()
        num_of_segments = dialog.intValue()
        return  [num_of_segments, ok]
        
    
    def execute(self, main_window: QMainWindow):
        active_image = self.get_active_image(main_window)
        if (not active_image):
            print("No image to transform")  # TODO: Notify user
            return

        dialog = SegmentsInput(main_window)
        

