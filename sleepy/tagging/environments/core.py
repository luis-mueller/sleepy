
from PyQt5.QtWidgets import QMessageBox
from sleepy.tagging.view import NullView, TaggingView
from sleepy.tagging.control import TaggingControl
from sleepy.gui.exceptions import UserCancel
from sleepy.gui.settings.v2.core import Settings

class Environment:

    def __init__(self, app):

        self.app = app

        self.active = False

    def activate(self):

        self.active = True

    def deactivate(self):

        self.active = False

    def refresh(self):
        pass

    def onResize(self):
        pass

class NullEnvironment(Environment):

    def __init__(self, app):

        super().__init__(app)

        self.view = NullView(app)

class TaggingEnvironment(Environment):

    def __init__(self, app):

        super().__init__(app)

        self.control = TaggingControl(self, app.applicationSettings)

        self.view = TaggingView(app, self.control)

        self.app = app

    def activate(self, fileLoader):
        """Attempt to activate the control. If the control can be opened, then
        activate self and process the control on after activation.
        """

        self.onBeforeActive()

        self.control.open(fileLoader)

        super().activate()

        self.control.onAfterActivate()

    def deactivate(self):

        self.onBeforeDeactive()

        self.control.onDeactivate()

        super().deactivate()

    def refresh(self):

        self.control.refresh()

    def onBeforeDeactive(self):

        if self.active:

            self.control.notifyUserOfSwitch()

    def onBeforeActive(self):

        if self.active:

            self.control.notifyUserOfSwitch()
