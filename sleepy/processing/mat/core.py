
from sleepy.processing.dataset import Dataset
from scipy.io import loadmat, savemat
import numpy as np

def sleepyProperty(function):

    def installer(self, *args):

        if not 'sleepy' in self.raw:

            self.raw['sleepy'] = np.array([None]*4)

        value = function(self, *args)

        if isinstance(value, np.ndarray):

            return value.copy()

        return value

    return installer

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
    @sleepyProperty
    def labels(self):

        if self.raw['sleepy'][0] is None:

            self.raw['sleepy'][0] = np.array([])

        return self.raw['sleepy'][0]

    @labels.setter
    @sleepyProperty
    def labels(self, labels):
        """Sets labels as a numpy array to the sleepy addition and derives the
        tags from the new labels too.
        """

        self.setChangesMadeFrom(labels)

        self.raw['sleepy'][0] = np.asarray(labels).copy()

    @property
    @sleepyProperty
    def tags(self):

        self.raw['sleepy'][1] = super().tags

        return self.raw['sleepy'][1]

    @tags.setter
    @sleepyProperty
    def tags(self, tags):
        self.raw['sleepy'][1] = tags.copy()

    @property
    @sleepyProperty
    def filteredData(self):
        """Copies the content from the dataset's data if no filtered data is
        available.
        """

        if self.raw['sleepy'][2] is None:

            self.raw['sleepy'][2] = self.data.copy()

        return self.raw['sleepy'][2]

    @filteredData.setter
    @sleepyProperty
    def filteredData(self, filteredData):

        if not np.array_equal(filteredData, self.filteredData):

            self.changesMade = True

        self.raw['sleepy'][2] = filteredData.copy()

    @property
    @sleepyProperty
    def userLabels(self):

        if self.raw['sleepy'][3] is None:

            self.raw['sleepy'][3] = np.array([])

        return self.raw['sleepy'][3]

    @userLabels.setter
    @sleepyProperty
    def userLabels(self, userLabels):

        if not np.array_equal(userLabels, self.userLabels):

            self.changesMade = True

        self.raw['sleepy'][3] = userLabels.copy()

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
            navigator.getCurrentTags()
                for navigator in navigators
        ])

        savemat(path, {'data' : self.raw})
