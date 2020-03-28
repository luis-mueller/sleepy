
import json
from functools import partial
from PyQt5.QtCore import QSettings
from sleepy.gui.settings.v2.view import SettingsView
from sleepy.gui.builder import Builder
import pdb

class Settings:

    def __init__(self, application = None, applicationCallback = lambda : None):
        """QSettings comes with the downside that it is extremely intransparant
        for debugging pruposes, since e.g. it is not straigthforward to delete all
        related keys. Thus, this class provides a wrapper around QSettings that
        handles dictionary itself, converts its content into a string and then
        stores that string in one key of the QSettings.
        An instance of this class, much like QSettings itself, can be created
        at any point in the application and still the latest values are drawn
        from the disk.
        """

        self.application = application
        self.applicationCallback = applicationCallback

        self.reset()

        self.load()

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

        # Make values accessible like attributes (settings.value)
        self.__dict__.update(self.temporaryDict.copy())

        self.dump(self.temporaryDict.copy())

        self.reset()

        self.applicationCallback()

    def reset(self):
        """Recover the actual internal dict state into a temporary dict. This
        dict is filled via the onCallback method. Once update is executed, this
        dict must be initialized.
        """

        self.temporaryDict = {
            'useCheckpoints' : False,
            'showIndex' : True,
            'intervalMin' : 3.0,
            'intervalMax' : 3.0
        }

    def asDialog(self):
        """Open a QDialog, displaying the current state. Embedds the view in an
        embedding application if one is supplied and also propagates the save
        event to that application.
        """

        view = SettingsView(self, self.application)

        view.exec_()

    def load(self):
        """Settings values are recovered from QSettings and written to the
        __dict__ dict.
        """

        try:

            values = self.loadValuesFromDisk()

            self.__dict__.update(values)

            self.extendDict(self.temporaryDict)

        except TypeError:
            pass

    def loadValuesFromDisk(self):
        """Disk access. Redefine this in a testing environment and return a
        dict with values. This method is encapsulated to make the class
        mockable under test with little to no effort.
        """

        jsonString = QSettings().value("json_settings")

        return json.loads(jsonString)

    def dump(self, settings):
        """Settings values are stored in the values dict and are now converted
        to json and dumped via QSettings.
        """

        jsonString = json.dumps(settings)

        QSettings().setValue("json_settings", jsonString)

    def extendDict(self, defaults):
        """Extend a dict with defaults, if and only if the defaulting key is
        not in the dict.
        """

        for key in defaults.keys():

            if not key in self__dict__.keys():

                self.__dict__[key] = defaults[key]
