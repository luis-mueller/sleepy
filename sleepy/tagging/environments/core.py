
from PyQt5.QtWidgets import QMessageBox
from sleepy.tagging.view import NullView, TaggingView
from sleepy.tagging.control import TaggingControl
from sleepy.tagging.exceptions import UserCancel

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

    @property
    def widget(self):
        raise NotImplementedError

class NullEnvironment(Environment):

    def __init__(self, app):

        super().__init__(app)

        self._widget = NullView(app)

    @property
    def widget(self):
        return self._widget

class TaggingEnvironment(Environment):

    def __init__(self, app):

        super().__init__(app)

        self.control = TaggingControl(self)

        self.view = TaggingView(app, self.control)

        self.app = app

    @property
    def widget(self):
        return self.view.widget

    def activate(self, fileLoader):

        self.onBeforeActive()

        self.control.open(fileLoader)

        super().activate()

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
