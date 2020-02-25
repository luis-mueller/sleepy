
class FileLoaderControl:

    def __init__(self, fileLoader):

        self.fileLoader = fileLoader

        self.accepted = False

    @property
    def options(self):
        return self.fileLoader.fileProcessor.options

    @property
    def path(self):
        return self.fileLoader.path

    @property
    def view(self):
        try:
            return self._view
        except AttributeError:
            self._view = None

    @view.setter
    def view(self, view):
        self._view = view

    def computeAndAccept(self):

        self.accepted = True

        self.view.accept()

    def selectPath(self):
        newPath, _ = QFileDialog.getOpenFileName(self, 'Open File')
        if newPath != '':

            self.fileLoader.path = newPath

            self.refresh()

    def refresh(self):

        self.view.pathEdit.setText(self.fileLoader.path)
