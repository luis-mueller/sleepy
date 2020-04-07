
from sleepy.processing import FileProcessor
from sleepy.gui.exceptions import UserCancel
from sleepy.io.gui import FileLoaderControl, FileLoaderView
from sleepy.processing._engine import Engine
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

    @fileProcessor.setter
    def fileProcessor(self, value):
        self._fileProcessor = value

    def load(self):

        if self.fileProcessor.options:

            self.showOptionsAndUpdate()

        self.navigator = Engine.run()

        return self.navigator, self.dataSet

    def computeLabels(self):
        self.fileProcessor.computeLabels(self.dataSet)

    def showNumberOfLabels(self):

        self.computeLabels()

        self.fileProcessor.showNumberOfLabels()

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
