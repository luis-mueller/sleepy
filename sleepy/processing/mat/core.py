
from sleepy.processing.dataset import Dataset
from scipy.io import loadmat, savemat
import numpy as np

class MatDataset(Dataset):
    """Implements the :class:`Dataset` interface of getters and setters. The
    sleepy-properties make use of a decorator that prepares the sleepy structure
    in mat-file before calling the getter or setter.
    This class is inherited by the publicly visible :class:`MultiChannelMatDataset`,
    which implements the logic behind the dataset. This class merely provides
    the bridge between the file-format and a convenient numpy format.
    """

    def importData(filename, structName='data'):

        '''Load Matlab file with EEG data and save all fields in a Python dictionary'''

        try:

            fullDictData = loadmat(filename)

            keys = fullDictData[structName][0, 0].dtype.descr

            vals = fullDictData[structName][0, 0]

        except:
            raise

        dictData = {}

        for i in range(len(keys)):

            key = keys[i][0]

            dictData[key] = np.squeeze(vals[key]) #Converts Matlab arrays into Python numpy arrays

        return dictData

    def load(path):

        raw = MatDataset.importData(path)

        raw.pop("cfg", None)

        return raw

    @property
    def epochs(self):
        return self.raw['sampleinfo'].copy()#[0][0][6].copy()

    @property
    def data(self):
        return self.raw['trial'].copy()#[0][0][1][0].copy()

    @property
    def labels(self):

        if 'sleepy-labels' not in self.raw:

            self.raw['sleepy-labels'] = np.array([])

        labels = self.raw['sleepy-labels'].copy()

        self.convertToPy(labels)

        return labels

    @labels.setter
    def labels(self, labels):
        """Sets labels as a numpy array to the sleepy addition and derives the
        tags from the new labels too.
        """

        self.setChangesMadeFrom(labels)

        self.raw['sleepy-labels'] = np.asarray(labels).copy()

    @property
    def tags(self):

        if not 'sleepy-tags' in self.raw:

            self.raw['sleepy-tags'] = super().tags

        tags = self.raw['sleepy-tags'].copy()

        self.convertToPy(tags)

        return tags

    @tags.setter
    def tags(self, tags):
        self.raw['sleepy-tags'] = tags.copy()

    @property
    def filteredData(self):
        """Copies the content from the dataset's data if no filtered data is
        available.
        """

        if 'sleepy-filteredData' not in self.raw:

            self.raw['sleepy-filteredData'] = self.data.copy()

        return self.raw['sleepy-filteredData']

    @filteredData.setter
    def filteredData(self, filteredData):

        if filteredData is not None:
            if not np.array_equal(filteredData, self.filteredData):

                self.changesMade = True

        self.raw['sleepy-filteredData'] = filteredData

    @property
    def userLabels(self):

        if 'sleepy-userLabels' not in self.raw:

            self.raw['sleepy-userLabels'] = np.array([])

        return self.raw['sleepy-userLabels'].copy()

    @userLabels.setter
    def userLabels(self, userLabels):

        if not np.array_equal(userLabels, self.userLabels):

            self.changesMade = True

        self.raw['sleepy-userLabels'] = userLabels.copy()

    @property
    def checkpoint(self):

        try:

            return tuple(self.raw['sleepy-metadata-checkpoint'].tolist())
        except KeyError:
            pass

    @checkpoint.setter
    def checkpoint(self, checkpoint):

        self.raw['sleepy-metadata-checkpoint'] = np.array(list(checkpoint))

    def removeCheckpoint(self):

        # Removes the metadata if it exists in the dictionary
        self.raw.pop('sleepy-metadata-checkpoint', None)

    def convertToPy(self, array):
        """Convert the given array into pythonic format.
        """

        for index in range(len(array)):

            array[index] = array[index].squeeze()

    def save(self, path, navigators):
        """Collects potentially changed data from a list of navigators and
        stores the data in the raw structure. Then, saves the raw data in the
        .mat file.
        """

        self.userLabels = np.array([
            navigator.getLabelPartition()[1]
                for navigator in navigators
        ])

        self.tags = np.array([
            navigator.getComputedEventTags()
                for navigator in navigators
        ])

        self.saveToDisk(path)

    def saveToDisk(self, path):
        """I/O method writing the contents of this dataset to the disk. Override
        this in a test environment to avoid I/O.

        :param path: Location of the saved file.
        """

        savemat(path, {'data' : self.raw})
