
from sleepy.tagging.model.event import Event

class PointEvent(Event):
    def __init__(self, point, dataSource, applicationSettings):

        super().__init__(dataSource, applicationSettings)

        self.point = point

    @property
    def interval(self):

        point = self.point

        nInterval = self.convertSeconds(self.intervalMin)

        pInterval = self.convertSeconds(self.intervalMax)

        return (point - nInterval, point + pInterval)

    @property
    def pointCoordinatesSeconds(self):

        time = self.convertSamples(self.point)

        relativePoint = self.point - self.epochInterval[0]

        voltage = self.dataSource.epoch[relativePoint]

        return (time, voltage)

    @property
    def currentPointInSeconds(self):
        return self.pointCoordinatesSeconds[0]

    def plot(self, axis):

        super().plot(axis)

        axis.plot(*self.pointCoordinatesSeconds, marker='o')
