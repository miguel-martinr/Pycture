from PIL.ImageQt import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QMainWindow



from .command import Command, InsiderCommand

class EditBrightnessCommand(InsiderCommand):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Brightness")

    def execute(self, main_window: QMainWindow):
        print("Edits brightness")

class ToGrayScale(InsiderCommand):
    def __init__(self, parent: QWidget):
       super().__init__(parent, "Gray scale (NTSC)")

    def execute(self, main_window: QMainWindow):
        image, title = self.get_active_image_with_title(main_window)
        if image == None:
            print("Gray scale transformation: No image found")
            return

        gray_scaled_image = image.get_gray_scaled_image()
        main_window.addEditor(QPixmap.fromImage(gray_scaled_image), title + "(GrayScaled)")


    
