
from sleepy.io.matfiles import MatDataSet
from sleepy.io.matfiles.multi import MultiChannelMatDatset
from sleepy.io.core import FileLoader
from sleepy.gui.exceptions import UserCancel
from scipy.io import loadmat, savemat
import pdb
import numpy as np

class MatFileLoader(FileLoader):

    @property
    def dataSet(self):

        try:
            return self._dataSet

        except AttributeError:

            rawData = loadmat(self.path)

            self._dataSet =  MultiChannelMatDatset(rawData)

            return self._dataSet

    def save(self):

        computedList, userList, tagList = [], [], []

        for navigator in self.navigator:

            computed, user = navigator.getLabelPartition()

            tags = navigator.getCurrentTags()

            computedList.append(computed)
            userList.append(user)
            tagList.append(tags)

        self.dataSet.userLabels = np.array(userList)

        self.dataSet.tags = np.array(tagList)

        #self.dataSet.raw.pop('data')

        savemat(self.path, self.dataSet.raw)

    def saveAs(self):

        path = self.app.fileManager.getPathForSaving()
        if path == '':
            raise UserCancel

        self.path = path

        self.save()
