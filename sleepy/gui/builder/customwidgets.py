
from PyQt5.QtWidgets import QCheckBox, QDoubleSpinBox, QSpinBox, QLineEdit, QPushButton, QHBoxLayout, QWidget, QColorDialog
from PyQt5.QtCore import Qt

class CustomQColorPicker(QWidget):

    def __init__(self):

        super().__init__()

        self.colorCode = QLineEdit()
        self.button = QPushButton('')
        self.button.clicked.connect(self.onClick)
        self.button.setMaximumHeight(20)
        self.button.setMaximumWidth(20)

        layout = QHBoxLayout()

        layout.addWidget(self.colorCode, alignment = Qt.AlignRight)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def onClick(self, event):
        self.setValue(QColorDialog.getColor().name())

    def setValue(self, value):
        self.colorCode.setText(value.upper())

        stylesheet = "QPushButton { background: %s; }" % value.upper()

        self.button.setStyleSheet(
            stylesheet
        )

    def value(self):
        return self.colorCode.text()

    @property
    def valueChanged(self):
        return self.colorCode.textChanged

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
