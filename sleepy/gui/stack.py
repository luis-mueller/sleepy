
from PyQt5.QtWidgets import QStackedWidget
from sleepy.tagging.environments import TaggingEnvironment, NullEnvironment
from sleepy.gui.exceptions import NoNavigatorError, UserCancel

class EnvironmentStack(QStackedWidget):
    def __init__(self, app):
        super().__init__()

        self.tagging = TaggingEnvironment(app)
        self.null = NullEnvironment(app)

        self.addWidget(self.tagging.view)
        self.addWidget(self.null.view)

        self.setNullWidget()

    def switchToTagging(self, fileLoader):

        try:

            self.tagging.activate(fileLoader)
        except UserCancel:

            return False

        if self.currentEnvironment == self.null:

            self.setCurrentWidget(self.tagging.view)

            self.currentEnvironment = self.tagging

            return True

        return False

    def switchToNull(self):

        if self.currentEnvironment == self.tagging:

            try:

                self.tagging.deactivate()
            except UserCancel:

                return False

            self.setNullWidget()

        return True

    def setNullWidget(self):

        self.null.view.open()

        self.setCurrentWidget(self.null.view)
        self.currentEnvironment = self.null

    def refresh(self):

        self.currentEnvironment.refresh()
