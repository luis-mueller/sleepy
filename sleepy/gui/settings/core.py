
import json
from functools import partial
from PyQt5.QtCore import QSettings
from sleepy.gui.settings.view import SettingsView
from sleepy.gui.builder import Builder
from sleepy import SLEEPY_ROOT_DIR
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

        self.values = {}

        Builder.setAttributesFromJSON(SLEEPY_ROOT_DIR + '/gui/settings/view.json', self, level = 3)

        self.load()

    def getCallbackDefault(self, key):
        """Returns a partial function is called with the key as the first
        argument. Called by the builder when default values are set. By default
        this adds an attribute to the control. However, this control requires
        that the values are stored in a dict, so they can be translated to json.
        """

        return partial(self.updateValues, key)

    def getCallback(self, key):
        """Returns a partial function is called with the key as the first
        argument. Called by the builder when layout is built.
        """

        return partial(self.onCallback, key)

    @Builder.callback
    def onCallback(self, key, value):
        """Gets called on callback in the builder. Receives a
        key value pair and updates the internal dict accordingly. This dict
        collects updates until a save event is fired.
        """

        self.updateValues(key, value)

    def updateValues(self, key, value):
        """Updates values with a key value pair
        """

        self.values[key] = value

    def update(self):
        """Store the values of the temporaryDict in the actual internal dict
        and propagate the event to the application.
        """

        # Make values accessible like attributes (settings.value)
        self.__dict__.update(self.values)

        self.dump(self.values)

        self.applicationCallback()

    def reset(self):
        """Resets the values dict to the values before updating.
        """

        Settings.updateExistingValues(self.__dict__, self.values)

    def asDialog(self):
        """Open a QDialog, displaying the current state. Embedds the view in an
        embedding application if one is supplied and also propagates the save
        event to that application.
        """

        view = SettingsView(self, self.application.view.window)

        view.exec_()

    def load(self):
        """Settings values are recovered from QSettings and written to the
        __dict__ dict.
        """

        try:

            values = self.loadValuesFromDisk()

            self.values.update(values)

        except TypeError:
            pass

        self.__dict__.update(self.values)

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

    def updateExistingValues(source, target):
        """Updates the value in target from the values in source if and only if
        the corresponding keys exist in both dicts.
        """

        for key in source.keys():

            if key in target:

                target[key] = source[key]
