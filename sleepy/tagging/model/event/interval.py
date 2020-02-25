
from sleepy.tagging.model.event import Event

class IntervalEvent(Event):
    def __init__(self, start, stop, dataSource, applicationSettings):

        super().__init__(dataSource, applicationSettings)

        self.interval = (start, stop)

        #axis.axvspan(*self.limits, alpha = .5)

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = value
