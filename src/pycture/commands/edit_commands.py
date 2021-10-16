from PIL.ImageQt import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QMainWindow

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
            return #TODO: Notify the user properly

        gray_scaled_image = image.get_gray_scaled_image()
        main_window.add_editor(QPixmap.fromImage(gray_scaled_image), title + "(GrayScaled)")


    
