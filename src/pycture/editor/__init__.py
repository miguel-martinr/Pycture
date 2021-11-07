from PyQt5.QtCore import Qt, QCoreApplication, QEvent
from PyQt5.QtGui import QImage, QCloseEvent, QMouseEvent
from PyQt5.QtWidgets import QDockWidget, QGraphicsDropShadowEffect, QWidget
from pycture.editor.image import Image

from pycture.events import DeleteEditorEvent, ChangeActiveEditorEvent
from pycture.css import LIGHT_GRAY
from pycture.dialogs import YesCancelNotification
from .container import Container

SELECTED_DOCK_CSS = f"""
QDockWidget::title {{
    background: {LIGHT_GRAY};
}}
"""


class Editor(QDockWidget):
    def __init__(self, parent: QWidget, image: QImage, image_name: str):
        super().__init__(parent)
        self.setWindowTitle(image_name)
        self.setWidget(Container(self, image))

        self.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        parent.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self)
        self.active = False

    def get_active_effect(self):
        active_effect = QGraphicsDropShadowEffect()
        active_effect.setBlurRadius(10)
        return active_effect

    def get_image(self) -> Image:
        return self.widget().get_image()

    def closeEvent(self, event: QCloseEvent):
        close_dialog = YesCancelNotification(self, "Are you sure?")
        if (close_dialog.exec()):
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

    def customEvent(self, event: QEvent):
        QCoreApplication.sendEvent(self.parent(), event)

    def set_active(self, active: bool):
        if (active and not self.active):
            self.setStyleSheet(SELECTED_DOCK_CSS)
            self.active = True
        else:
            self.setStyleSheet(None)
            self.active = False

    def is_fully_loaded(self):
        return self.get_image().load_finished