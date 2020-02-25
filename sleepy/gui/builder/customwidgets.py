
from PyQt5.QtWidgets import QCheckBox, QDoubleSpinBox

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
