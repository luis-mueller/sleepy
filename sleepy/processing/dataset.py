
import numpy as np
from sleepy.gui.tagging.model import DataSource

class Dataset:

    def load(path):
        """Static API-method that returns a raw data object for a given path.
        Must be implemented by direct subclasses.

        :param path: An absolute path to a file whose contents should be loaded
        as a raw data object.
        """

        raise NotImplementedError

    def __init__(self, raw = None, path = ""):
        """Abstract Dataset class, serving as an interface for all implementations.
        """

        self.raw = raw

        self.path = path

        self.samplingRate = 500

        self.changesMade = False

        self.dataSources = {}

    @property
    def filename(self):
        return self.path.split('/')[-1]

    @property
    def epochs(self):
        return self._epochs

    @epochs.setter
    def epochs(self, epochs):
        self._epochs = epochs

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def labels(self):
        try:
            return self._labels
        except AttributeError:

            self._labels = np.array([])

            return self._labels

    @labels.setter
    def labels(self, labels):
        self._labels = labels

    @property
    def userLabels(self):
        return self._userLabels

    @userLabels.setter
    def userLabels(self, userLabels):
        self._userLabels = userLabels

    @property
    def filteredData(self):
        """By default, if no filteredData is set, the filteredData is simply
        equal the unfiltered data, i.e. self.data.
        """

        try:

            return self._filteredData
        except AttributeError:

            self.filteredData = self.data.copy()

    @filteredData.setter
    def filteredData(self, filteredData):
        self._filteredData = filteredData

    @property
    def tags(self):
        """If tags are not set by the caller, then the tags are set to 0 using
        the labels array.
        """

        try:
            return self._tags
        except AttributeError:

            numberOfChannels = self.labels.shape[0]

            self._tags = [
                np.zeros(self.labels[channel].shape[0])
                    for channel in range(numberOfChannels)
            ]

            return self._tags

    @tags.setter
    def tags(self, tags):
        self._tags = tags

    @property
    def checkpoint(self):
        return self._checkpoint

    @checkpoint.setter
    def checkpoint(self, checkpoint):
        self._checkpoint = checkpoint

    def save(self):
        """Call to the dataset to save its contents on disk.
        """

    def setChangesMadeFrom(self, result):
        """Sets changesMade to true if the result array is equal to the labels
        in the dataset.
        """

        try:
            labels = self.dataSet.labels
        except AttributeError:
            return True

        self.changesMade = not np.array_equal(result, labels)

    def forEachChannel(self, converter):

        numberOfChannels = self.labels.shape[0]

        return [ self.forEachLabel(channel, converter) for channel in range(numberOfChannels) ]

    def forEachLabel(self, channel, converter):
        """Supplies a set of parameters to a converter and returns
        the result to the caller. Parameters a numpy array type of a label
        """

        numberOfLabels = self.labels[channel].shape[0]

        def getObject(labelIndex):

            label = np.array([self.labels[channel][labelIndex]]).ravel()

            dataSource = self.getDataSource(channel, label)

            tag = self.tags[channel][labelIndex]

            return converter(label, tag, dataSource)

        return [ getObject(idx) for idx in range(numberOfLabels) ]

    def getDataSource(self, channel, label):
        """Returns a data source for a given channel and a given label.
        Extracts the first element from the label.
        """

        # We only use label[0] as we rely on events not overlapping samples.
        # Therefore interval and point labels are both covered.
        dataSource = self.getDataSourceForLabel(channel, label[0])

        dataSource.addLabel(label)

        return dataSource

    def getDataSourceForLabel(self, channel, label):

        epochIndex = self.findIndexInInterval(self.epochs, label)

        return self.getBufferedDataSource(epochIndex, channel)

    def findIndexInInterval(self, data, point):

        startPoints = data[:,0]
        endPoints = data[:,1]

        startIndices = np.where(
            startPoints <= point
        )

        endIndices = np.where(
            endPoints >= point
        )

        intersection = np.intersect1d(startIndices, endIndices)

        # We assume the intervals to be non-overlapping and thus
        # it can only be one index match in both queries
        return intersection[0]

    def getBufferedDataSource(self, epochIndex, channel):

        if not channel in self.dataSources:

            self.dataSources[channel] = {}

        if not epochIndex in self.dataSources[channel]:

            epochInterval = self.epochs[epochIndex]

            epoch = self.data[epochIndex][channel]

            epochFiltered = self.filteredData[epochIndex][channel]

            self.dataSources[channel][epochIndex] = DataSource(
                epoch, epochFiltered, epochInterval, self.samplingRate
            )

        return self.dataSources[channel][epochIndex]

    def removeCheckpoint(self):
        pass
