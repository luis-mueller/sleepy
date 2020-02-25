
from sleepy.tagging.model.event import Event

class IntervalEvent(Event):
    def __init__(self, start, stop, dataSource, applicationSettings):

        super().__init__(dataSource, applicationSettings)

        self.interval = (start, stop)

        #axis.axvspan(*self.limits, alpha = .5)
