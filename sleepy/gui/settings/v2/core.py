
import json
from functools import partial
from PyQt5.QtCore import QSettings
from sleepy.gui.settings.v2.view import SettingsView
from sleepy.gui.builder import Builder

class Settings:

    def __init__(self, application = None, applicationCallback = lambda : None, **kwargs):
        """QSettings comes with the downside that it is extremely intransparant
        for debugging pruposes, since e.g. it is not straigthforward to delete all
        related keys. Thus, this class provides a wrapper around QSettings that
        handles dictionary itself, converts its content into a string and then
        stores that string in one key of the QSettings.
        Embedds the view in an embedding application if one is supplied and also
        propagates the save event to that application.
        """

        self.application = application
        self.applicationCallback = applicationCallback

        # Make values accessible like attributes (settings.value)
        self.__dict__.update(kwargs)

        self.recover()

        self.view = SettingsView(self, self.application)

    def getCallback(self, key):
        """Returns a partial function is called with the key as the first
        argument.
        """

        return partial(self.onCallback, key)

    @Builder.callback
    def onCallback(self, key, value):
        """Gets called on callback of a widget in the builder. Receives a
        key value pair and updates the internal dict accordingly. This dict
        collects updates until a save event is fired.
        """

        self.temporaryDict[key] = value

    def update(self):
        """Store the values of the temporaryDict in the actual internal dict
        and propagate the event to the application.
        """

        self.__dict__.update(self.temporaryDict.copy())

        self.applicationCallback()

    def recover(self):
        """Recover the actual internal dict state.
        """

        self.temporaryDict = self.__dict__.copy()
