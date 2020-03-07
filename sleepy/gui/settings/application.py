
from sleepy.gui.settings.builder import ApplicationSettingsBuilder
from sleepy.gui.settings.view import ApplicationSettingsView
from sleepy.gui.settings.api import ApplicationSettingsAPI
from PyQt5.QtWidgets import QCheckBox, QDoubleSpinBox
import pdb

class ApplicationSettings:

    def __init__(self, app):

        self.api = ApplicationSettingsAPI(app)

        self.view = ApplicationSettingsView(app, self.api)

        self.builder = ApplicationSettingsBuilder(self.api, self.view)

        self.builder.build()

    @property
    def useCheckpoints(self):
        return self.api.useCheckpoints

    @property
    def intervalMin(self):
        return self.api.intervalMin

    @property
    def intervalMax(self):
        return self.api.intervalMax

    @property
    def showIndex(self):
        return self.api.showIndex

    @property
    def plotGrid(self):
        return self.api.plotGrid

    @property
    def plotGridSize(self):
        return self.api.plotGridSize
