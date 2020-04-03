
import numpy as np

def mapping(function):

    def mapper(self):

        object = function(self, self.raw)

        setattr(self, function.__name__, object)

    return mapper

def sleepyContent(function):

    def content(self):

        if not 'sleepy' in self.raw:

            self.raw['sleepy'] = {}

        if not function.__name__ in self.raw['sleepy']:

            self.raw['sleepy'][function.__name__] = np.array([])

        mapping(function)(self)

    return content

class Dataset:

    def __init__(self, raw):

        self.raw = raw

        self.samplingRate = 500

        self.changesMade = False

        self.dataSources = {}

    def sleepyContent(self, attributes):

        if not 'sleepy' in self.raw:

            self.raw['sleepy'] = {}

        for attribute in attributes:

            if not attribute in self.raw['sleepy']:

                self.raw['sleepy'][attribute] = np.array([])

            setattr(self, attribute, self.raw['sleepy'][attribute])
