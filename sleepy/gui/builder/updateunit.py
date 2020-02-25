
from PyQt5.QtWidgets import QWidget
from sleepy.gui.builder.exceptions import LoadNotPossible

class UpdateUnit:

    def __init__(self, default):

        self.value = default

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

class UpdateObject:

    def __init__(self, identifier, WidgetType, unit):

        self.widgetTypeCheck(WidgetType)

        self.identifier = identifier
        self.widget = WidgetType()

        try:
            self.load()
        except LoadNotPossible:

            self.widget.setValue(unit.value)

        self.widget.valueChanged.connect(self.update)

        self.unit = unit

    def widgetTypeCheck(self, type):

        if not issubclass(type, QWidget):
            raise ValueError("Dynamic QSetting: Type is not a QWidget.")

    @property
    def value(self):
        return self.widget.value()

    def update(self):
        self.unit.value = self.value

    def load(self):
        raise LoadNotPossible()
