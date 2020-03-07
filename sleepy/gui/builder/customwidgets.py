
from PyQt5.QtWidgets import QCheckBox, QDoubleSpinBox, QSpinBox

class CustomQCheckBox(QCheckBox):

    def setValue(self, value):
        self.setChecked(bool(value))

    def value(self):

        return int(self.isChecked())

    @property
    def valueChanged(self):
        return self.stateChanged

class CustomQDoubleSpinBox(QDoubleSpinBox):

    def setValue(self, value):

        super().setValue(float(value))

class Custom0To1DoubleSpinBox(CustomQDoubleSpinBox):

    def __init__(self):

        super().__init__()

        self.setMinimum(0.0)
        self.setMaximum(1.0)

class CustomQSpinBox(QSpinBox):

    def setValue(self, value):

        super().setValue(int(value))
