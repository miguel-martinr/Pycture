from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QCloseEvent, QMouseEvent
from PyQt5.QtWidgets import QDockWidget, QWidget, QMessageBox, QLabel

class Editor(QDockWidget):
    def __init__(self, parent: QWidget, image: QPixmap, image_path: str):
        super().__init__(parent)
        self.setWindowTitle(image_path)
        self.setup_image(image)
        self.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        parent.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self)
    
    def setup_image(self, image: QPixmap):
        label = QLabel(self)
        label.setPixmap(image)
        self.setWidget(label)
        
    def closeEvent(self, event: QCloseEvent):
        close_dialog = QMessageBox()
        close_dialog.setText("Are you sure?")
        close_dialog.setStandardButtons(QMessageBox.StandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
        ))
        answer = close_dialog.exec()

        if (answer == Yes):
            Context.deleteEditor(self.index)
            event.accept()
        else:
            event.ignore()
  
    def mousePressEvent(self, event: QMouseEvent):
        print("mouse pressed")
        #ChangeFocusEvent
