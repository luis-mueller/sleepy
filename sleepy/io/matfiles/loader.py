
from sleepy.io.matfiles import MatDataSet
from sleepy.io.core import FileLoader
from sleepy.gui.exceptions import UserCancel
from scipy.io import loadmat, savemat
import pdb

class MatFileLoader(FileLoader):

    @property
    def dataSet(self):

        try:
            return self._dataSet

        except AttributeError:

            rawData = loadmat(self.path)

            self._dataSet =  MatDataSet(rawData)

            return self._dataSet

    def save(self):

        computed, user = self.navigator.getLabelPartition()

        self.dataSet.labels = computed

        self.dataSet.setUserLabels(user)

        self.dataSet.tags = self.navigator.getCurrentTags()

        savemat(self.path, self.dataSet.matData)

    def saveAs(self):

        path = self.app.fileManager.getPathForSaving()
        if path == '':
            raise UserCancel

        self.path = path

        self.save()
