
from sleepy.tagging.model import DataSource
import numpy as np
import pdb

class MatDataSet:
    def __init__(self, matData):

        self.matData = matData
        self.dataSources = {}
        self.samplingRate = 500

    @property
    def epochs(self):

        return self.matData['sampleInfo']

    @property
    def labels(self):

        labels = self.matData['label']

        if len(labels) != 1  or len(labels.shape) > 1:

            return labels.squeeze()
        else:

            return labels

    @labels.setter
    def labels(self, entries):

        labels = self.labels

        self.matData['label'] = entries

        self.migrateTags(labels)

    @property
    def channelData(self):

        try:

            return self.channelInternalFormat
        except:

            channelData = self.matData['channelData'].squeeze(axis = 0)

            self.channelInternalFormat = list(
                map(
                    lambda e: e[0],
                    channelData
                )
            )

            return self.channelInternalFormat

    @property
    def numberOfLabels(self):

        return self.labels.shape[0]

    @property
    def tags(self):

        if not 'tags' in self.matData:

            self.matData['tags'] = np.zeros(self.numberOfLabels)

            return self.matData['tags']

        else:

            tags = self.matData['tags']

            if len(tags) != 1 or len(tags.shape) > 1:

                return  tags.squeeze()
            else:

                return tags

    @tags.setter
    def tags(self, tags):

        self.matData['tags'] = tags

    @property
    def pointsInSeconds(self):

        channelData = np.array(self.channelData.copy()).flatten()

        return channelData / self.samplingRate

    def getDataSourceFor(self, labelIndex):

        label = self.labels[labelIndex]

        if isinstance(label, list):
            label = label [0]

        # We only use label[0] as we rely on events not overlapping samples.
        # Therefore interval and point labels are both covered
        epochIndex = self.findIndexInInterval(self.epochs, label)

        dataSource = self.getBufferedDataSource(epochIndex)

        dataSource.addLabel(label)

        return dataSource

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

    def getBufferedDataSource(self, epochIndex):

        if not epochIndex in self.dataSources:

            epochInterval = self.epochs[epochIndex]

            epoch = self.channelData[epochIndex]

            self.dataSources[epochIndex] = DataSource(
                epoch, epochInterval, self.samplingRate
            )

        return self.dataSources[epochIndex]

    def migrateTags(self, oldLabels):
        """Maps old tags to old labels (if they are still in the data-set)"""

        oldTags = self.exchangeTagList()

        if self.compliantEventType(oldLabels, self.labels):

            indexRange = range(oldLabels.shape[0])

            for index in indexRange:

                try:

                    newIndex = self.findIndexForOldLabel(oldLabels[index])

                    self.tags[newIndex] = oldTags[index]
                except ValueError:
                    pass

    def findIndexForOldLabel(self, oldLabel):

        labelList = self.labels.tolist()

        return labelList.index(oldLabel)

    def exchangeTagList(self):

        oldTags = self.tags

        self.tags = np.zeros(self.numberOfLabels)

        return oldTags

    def compliantEventType(self, old, new):

        if len(old.shape) == len(new.shape):

            if len(old.shape) > 1:

                if old.shape[1] == new.shape[1]:

                    return True
            else:

                return True

        return False

    def setCheckpoint(self, checkpoint):

        self.matData['sleepy-metadata-checkpoint'] = str(checkpoint)

    def getCheckpoint(self):

        try:

            return int(self.matData['sleepy-metadata-checkpoint'])
        except KeyError:
            pass

    def removeCheckpoint(self):

        # Removes the metadata if it exists in the dictionary
        self.matData.pop('sleepy-metadata-checkpoint', None)
