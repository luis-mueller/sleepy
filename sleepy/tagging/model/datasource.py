
import numpy as np

class DataSource:
    """A :class:`DataSet` loads the data initially and converts it into a
    useable form. It further creates a dictionary of dataSources, the epochs
    of the data. Each epoch contains information about the sampling-rate,
    the interval of the epoch and maintains an instance of :class:`ApplicationSettings`.
    This instance is UI-decoupled, hence does not prepare a GUI-Widget but simply
    builds the updateObjects which have access to memory. Additionally the
    :class:`DataSource` offers methods for general conversion.
    """
    def __init__(self, epoch, epochInterval, samplingRate = 500):
        self.epoch = epoch
        self.epochInterval = epochInterval
        self.samplingRate = samplingRate
        self.labels = []
        self.events = []

    @property
    def size(self):
        return self.epoch.size

    def get(self, start, stop):
        return self.epoch[start:stop]

    def addLabel(self, label):
        self.labels.append(label)

    def addEvent(self, event):
        self.events.append(event)

    @property
    def labelsInSeconds(self):
        """Works for point and interval labels"""

        labels = np.array(self.labels)

        labels = labels / self.samplingRate

        return labels.tolist()
