
from sleepy.tagging.model import DataSource
from sleepy.io.matfiles.core import MultiChannelMatInterface
import numpy as np
import pdb
from functools import partial

class MultiChannelMatDatset(MultiChannelMatInterface):

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
