
import numpy as np

class DataEvent:

    def __init__(self, default):

        self._value = default
        self._onTrigger = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):

        oldValue = self.value

        self._value = value

        if oldValue != value:

            self.trigger()

    def connect(self, toConnect):
        """toConnect can be a single function or a list of functions. This
        method first transforms any input into an iterable and then
        adds every object in that iterable into the list of connected
        functions."""

        functions = self.makeIterable(toConnect)

        self._onTrigger.extend(functions)

    def trigger(self):

        list( map( lambda f: f(self.value), self._onTrigger ) )

    def initialize(self, toConnect):
        """Initialize corresponds to connecting and triggering at the same time.
        This can be useful when an object needs an initial propagation of the
        default value that this event observes"""

        self.connect(toConnect)

        self.trigger()

    def makeIterable(self, value):

        return np.array(value).flatten()
