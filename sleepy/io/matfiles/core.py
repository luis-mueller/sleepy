
from sleepy.io.dataset import Dataset
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

class MultiChannelMatInterface(Dataset):
    """Implements the :class:`Dataset` interface of getters and setters. The
    sleepy-properties make use of a decorator that prepares the sleepy structure
    in mat-file before calling the getter or setter.
    This class is inherited by the publicly visible :class:`MultiChannelMatDataset`,
    which implements the logic behind the dataset. This class merely provides
    the bridge between the file-format and a convenient numpy format.
    """

    @property
    def epochs(self):
        return self.raw['data'][0][0][6].copy()

    @property
    def data(self):
        return self.raw['data'][0][0][1][0].copy()

    @property
    @sleepyProperty
    def labels(self):

        if self.raw['sleepy'][0] is None:

            self.raw['sleepy'][0] = np.array([])

        return self.raw['sleepy'][0]

    @labels.setter
    @sleepyProperty
    def labels(self, labels):

        self.raw['sleepy'][0] = labels.copy()

        numberOfChannels = self.labels.shape[0]

        self.tags = [ np.zeros(self.labels[channel].shape[0]) for channel in range(numberOfChannels) ]

    @property
    @sleepyProperty
    def tags(self):
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

        return self.data.copy()
        return self.raw['sleepy'][2]

    @filteredData.setter
    @sleepyProperty
    def filteredData(self, filteredData):
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
