
import numpy as np
from sleepy.gui.tagging.model import DataSource

class Dataset:

    def load(path):
        """Static API-method that returns a raw data object for a given path.
        Must be implemented by direct subclasses.

        :param path: An absolute path to a file whose contents should be loaded
        as a raw data object.
        """

        pass

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

        try:
            return self._userLabels
        except AttributeError:
            return []

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

            return self._filteredData

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
        pass

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
        """Supplies a converter function for each pair of channel and label that
        is stored in this dataset. The converter function is supplied with the
        following arguments:

        * Label
        * Tag of the corresponding event
        * Data source containing the data of the epoch that contains the label

        The goal of this method is to abstract extracting the necessary data
        from the dataset to create a new event. The converter function can
        create an event based on this input and return it.

        :param converter: A function that respects the said format.

        :returns: A list of lists of the return values of each converter function
        call.
        """

        numberOfChannels = self.labels.shape[0]

        return [ self.__forEachLabel(channel, converter) for channel in range(numberOfChannels) ]

    def getDataSource(self, channel, label):
        """Returns a data source for a given channel and a given label.
        Extracts the first element from the label. The goal is to create one
        data source for each epoch such that events in the same epoch can share
        the data source (and data must not be copied that often). This instance
        buffers the data sources it has already created. If the epoch to which
        the given label belongs did not occur already, a new data source is
        allocated.

        :param channel: The index of the channel for which the data source shall
        be retrieved.

        :param label: The label containing a point or an interval in samples
        indicating where the event occurs.

        :returns: An instance of :class:`sleepy.gui.tagging.model.datasource.DataSource`
        containing the epoch data of the label.
        """

        if isinstance(label, np.ndarray):
            label = label[0]

        epochIndex = self.__findIndexInInterval(label)

        dataSource = self.__getBufferedDataSource(epochIndex, channel)

        dataSource.addLabel(label)

        return dataSource

    def __forEachLabel(self, channel, converter):
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

    def __findIndexInInterval(self, point):
        """Finds the epoch interval by index to which a given point belongs.
        """

        startPoints = self.epochs[:,0]
        endPoints = self.epochs[:,1]

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

    def __getBufferedDataSource(self, epochIndex, channel):
        """Checks the buffer if the data source for the epoch specified by
        epochIndex and channel. If the data source does not exist, creates
        a new data source for this epoch. Returns the data source in both cases.
        """

        self.__ensureChannelInDataSources(channel)

        if not epochIndex in self.dataSources[channel]:

            self.__allocateDataSource(epochIndex, channel)

        return self.dataSources[channel][epochIndex]

    def __allocateDataSource(self, epochIndex, channel):
        """Creates a new data source for an epoch specified by epochIndex and
        channel.
        """

        epochInterval = self.epochs[epochIndex]

        epochData = self.__getEpochData(epochIndex, channel)

        self.dataSources[channel][epochIndex] = DataSource(
            *epochData, epochInterval, self.samplingRate
        )

    def __getEpochData(self, epochIndex, channel):
        """Retrieves the raw and the filtered data of the epoch, specified by
        epochIndex and channel, from the dataset.
        """

        epoch = self.data[epochIndex][channel]

        epochFiltered = self.filteredData[epochIndex][channel]

        return epoch, epochFiltered

    def __ensureChannelInDataSources(self, channel):
        """Ensures that the buffer contains an entry for a given channel.
        """

        if not channel in self.dataSources:

            self.dataSources[channel] = {}
