
class Dataset:

    def __init__(self, raw):
        """Abstract Dataset class, serving as an interface for all implementations.
        """

        self.raw = raw

        self.samplingRate = 500

        self.changesMade = False

        self.dataSources = {}

    @property
    def epochs(self):
        raise NotImplementedError

    @epochs.setter
    def epochs(self, epochs):
        raise NotImplementedError

    @property
    def data(self):
        raise NotImplementedError

    @data.setter
    def data(self, data):
        raise NotImplementedError

    @property
    def labels(self):
        raise NotImplementedError

    @labels.setter
    def labels(self, labels):
        raise NotImplementedError

    @property
    def userLabels(self):
        raise NotImplementedError

    @userLabels.setter
    def userLabels(self, userLabels):
        raise NotImplementedError

    @property
    def filteredData(self):
        raise NotImplementedError

    @filteredData.setter
    def filteredData(self, filteredData):
        raise NotImplementedError

    @property
    def tags(self):
        raise NotImplementedError

    @tags.setter
    def tags(self, tags):
        raise NotImplementedError

    @property
    def checkpoint(self):
        raise NotImplementedError

    @checkpoint.setter
    def checkpoint(self, checkpoint):
        raise NotImplementedError
