
from sleepy.io.matfiles import MatFileLoader
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QSettings

class FileManager:
    def __init__(self, app, supportedLoaders = {'mat' : MatFileLoader}):

        self.supportedLoaders = supportedLoaders
        self.app = app
        self.qSettings = QSettings()
        self.recentPath = self.qSettings.value("recentPath")

    def openNew(self):

        path, _ = QFileDialog.getOpenFileName(
            self.app, 'Open File', self.recentPath
        )

        if path != '':

            self.recentPath = path
            self.qSettings.setValue("recentPath", path)

            fileExtension = self.getFileExtension(path)

            try:

                return self.supportedLoaders[fileExtension](self.app, path)
            except AttributeError:

                error = QMessageBox(self.app)
                error.setWindowTitle('Error')
                error.setIcon(QMessageBox.Critical)
                error.setText(
                    'Files of type {} are not supported.'.format(fileExtension)
                )
                error.exec_()

    def getPathForSaving(self):

        path, _ = QFileDialog.getSaveFileName(
            self.app, 'Save File', self.recentPath
        )
        return path

    def getFileExtension(self, path):

        return path.rsplit('.', 1)[-1]
