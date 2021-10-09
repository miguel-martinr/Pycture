from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QPixmap, QCloseEvent, QMouseEvent
from PyQt5.QtWidgets import QDockWidget, QWidget, QMessageBox, QLabel

from classes.events import DeleteEditorEvent, ChangeActiveEditorEvent

class Editor(QDockWidget):
    def __init__(self, parent: QWidget, image: QPixmap, image_name: str):
        super().__init__(parent)
        self.setWindowTitle(image_name)
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
        Yes = QMessageBox.StandardButton.Yes 
        Cancel = QMessageBox.StandardButton.Cancel
        close_dialog.setStandardButtons(
            QMessageBox.StandardButtons(Yes | Cancel)
        )
        answer = close_dialog.exec()

        if (answer == Yes):
            QCoreApplication.sendEvent(
                self.parent(),
                DeleteEditorEvent(self.windowTitle())
            )
            event.accept()
        else:
            event.ignore()
  
    def mousePressEvent(self, event: QMouseEvent):
        QCoreApplication.sendEvent(
            self.parent(),
            ChangeActiveEditorEvent(self.windowTitle())
        )
        