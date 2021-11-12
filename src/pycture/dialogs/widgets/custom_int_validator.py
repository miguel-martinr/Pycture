from PyQt5.QtGui import QValidator


# This custom validator was needed because Qt's default IntValidator
# is more permisive with the input that can be introduced than it was
# wanted here. This way you can't write 256 or -1.
# For more information: https://doc.qt.io/qt-5/qvalidator.html#validate
class CustomIntValidator(QValidator):
    def __init__(self, lower_limit: int, upper_limit: int):
        super().__init__()
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit

    def validate(self, input: str, pos: int):
        State = QValidator.State

        if (input == ""):
            return State.Intermediate, input, pos
        if (not str.isdigit(input)):
            return State.Invalid, input, pos
        if (not (self.lower_limit <= int(input) <= self.upper_limit)):
            return State.Invalid, input, pos
        return State.Acceptable, input, pos
