
from sleepy.processing import FileProcessor
from sleepy.gui.exceptions import UserCancel
from sleepy.io.gui import FileLoaderControl, FileLoaderView
import pdb

class FileLoader:
    def __init__(self, app, path):

        self.app = app
        self.path = path

    @property
    def dataSet(self):
        raise NotImplementedError

    @property
    def fileProcessor(self):

        try:
            return self._fileProcessor

        except AttributeError:
            self._fileProcessor = FileProcessor(
                self.app.applicationSettings
            )
            return self._fileProcessor

    def load(self):

        if self.fileProcessor.options:

            self.showOptionsAndUpdate()

        self.navigator = self.fileProcessor.computeNavigator(self.dataSet)

        return self.navigator

    def save(self):
        raise NotImplementedError

    def saveAs(self):
        raise NotImplementedError

    def showOptionsAndUpdate(self):

        options = FileLoaderControl(self)

        options.view = FileLoaderView(self.app, options)

        options.view.exec_()

        if not options.accepted:
            raise UserCancel
