
from sleepy.tagging.model import DataSource
from sleepy.io.dataset import mapping, Dataset
import numpy as np
import pdb

def formatCheck(function):

    def setterFunction(self, *args):

        try:

            function(self, *args)

        except KeyError:
            raise TypeError('Format not supported.')

        except IndexError:
            raise TypeError('Format not supported.')

    return setterFunction

class MultiChannelMatDatSet(Dataset):

    def __init__(self, raw):

        self.raw = raw

        self.samplingRate = 500

        self.changesMade = False

        self.dataSources = {}

        self.epochs()

        self.data()

        self.sleepyContent(
            ['labels', 'tags', 'userLabels', 'filteredData', 'checkpoint']
        )

        pdb.set_trace()


    @mapping
    def epochs(self, data):

        return data['data'][0][0][6]

    @mapping
    def data(self, data):

        self.filteredData = data['data'][0][0][1][0].copy()

        return data['data'][0][0][1][0]

    def setLabels(self, labels):

        self.labels = labels

        numberOfChannels = self.labels.shape[0]

        self.tags = [ np.zeros(self.labels[channel].shape[0]) for channel in range(numberOfChannels) ]

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

        dataSource = self.getDataSourceForLabel(channel, label[0])

        dataSource.addLabel(label)

        return dataSource

    def getDataSourceForLabel(self, channel, label):

        # We only use label[0] as we rely on events not overlapping samples.
        # Therefore interval and point labels are both covered
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

    def setFilteredData(self, index, channel, filteredData):

        if not np.array_equal(filteredData, self.filteredData[index][channel]):

            self.changesMade = True

        self.filteredData[index][channel] = filteredData

    def removeCheckpoint(self):
        pass