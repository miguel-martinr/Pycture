from PyQt5.QtWidgets import QHBoxLayout, QCheckBox, QWidget

class RGBCheckboxes(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.checkboxes = []
        layout = QHBoxLayout()
        self.setLayout(layout)
        colors = ["Red", "Green", "Blue", "All"]
        for color in colors:
            checkbox = QCheckBox(color, self)
            self.checkboxes.append(checkbox)
            layout.addWidget(checkbox)
        for checkbox in self.checkboxes[0:3]:
            checkbox.stateChanged.connect(self.rgb_checkbox_changed)
        self.checkboxes[3].stateChanged.connect(self.all_checkbox_changed)
        self.changed_in_code = False

    def all_checkbox_changed(self, checked):
        if not self.changed_in_code:
            for checkbox in self.checkboxes[0:3]:
                checkbox.setChecked(checked)
            

    def rgb_checkbox_changed(self, checked):
        if not checked:
            self.changed_in_code = True
            self.checkboxes[3].setChecked(False)
            self.changed_in_code = False
        elif self.get_checked() == (True, True, True):
            self.checkboxes[3].setChecked(True)

    def get_checked(self) -> (bool, bool, bool):
        is_checked = lambda index: self.checkboxes[index].isChecked()
        return (is_checked(0), is_checked(1), is_checked(2))