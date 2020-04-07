
from sleepy.gui.tagging.model.event import Event
import numpy as np

class IntervalEvent(Event):
    def __init__(self, start, stop, dataSource, applicationSettings):

        super().__init__(dataSource, applicationSettings)

        self.interval = (start, stop)

    @property
    def label(self):
        return np.array(self._interval)

    @property
    def interval(self):

        nInterval = self.convertSeconds(self.intervalMin)

        pInterval = self.convertSeconds(self.intervalMax)

        return (self._interval[0] - nInterval, self._interval[1] + pInterval)

    @interval.setter
    def interval(self, value):
        self._interval = value

    @property
    def intervalInSeconds(self):

        start = self.convertSamples(self._interval[0])
        end = self.convertSamples(self._interval[1])

        return (start, end)

    @property
    def point(self):

        return ( self._interval[0] + self._interval[1] ) / 2

    @property
    def currentPointInSeconds(self):

        timeStart = self.convertSamples(self._interval[0])
        timeEnd = self.convertSamples(self._interval[1])

        return ( timeStart + timeEnd ) / 2

    def plotSelected(self, axis):

        axis.axvspan(*self.intervalInSeconds, alpha = .5, color=self.applicationSettings.plotSelectedColor)

    def plotVisible(self, axis):

        axis.axvspan(*self.intervalInSeconds, alpha = .5, color="gray")

    def inInterval(self, interval):
        """Checks whether the event is inside of a given interval. This is true,
        if and only if the start of the event's interval is later than or equal to
        the start of the interval and is earlier or equal to the end of the interval.
        """

        return self._interval[0] >= interval[0] and self._interval[1] <= interval[1]
