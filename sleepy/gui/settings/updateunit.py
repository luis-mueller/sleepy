
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSettings
from sleepy.gui.settings.constants import SLASH, PATH
from sleepy.gui.builder.updateunit import UpdateUnit

class ApplicationSettingsUnit(UpdateUnit):

    def __init__(self, name, default):

        self.qSettings = QSettings()

        self.name = name

        value = self.getSettingFor()

        if value:
            super().__init__(value)
        else:
            super().__init__(default)

        self.value = value

    @property
    def value(self):
        return self.getSettingFor()

    @value.setter
    def value(self, value):
        self.setSettingFor(value)

    def getSettingFor(self):

        return self.qSettings.value(SLASH.join([PATH, self.name]))

    def setSettingFor(self, value):

        self.qSettings.setValue(SLASH.join([PATH, self.name]), value)
