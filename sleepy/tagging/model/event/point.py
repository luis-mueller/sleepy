
from sleepy.tagging.model.event import Event
import pdb

class PointEvent(Event):
    def __init__(self, point, dataSource, applicationSettings):

        super().__init__(dataSource, applicationSettings)

        self.point = point

    @property
    def label(self):
        return self.point

    @property
    def interval(self):

        point = self.point

        nInterval = self.convertSeconds(self.intervalMin)

        pInterval = self.convertSeconds(self.intervalMax)

        return (point - nInterval, point + pInterval + 1)

    @property
    def pointCoordinatesSeconds(self):

        time = self.convertSamples(self.point)

        relativePoint = self.point - self.epochInterval[0]

        voltage = self.getVoltage(relativePoint)

        return (time, voltage)

    @property
    def currentPointInSeconds(self):
        return self.pointCoordinatesSeconds[0]

    def plot(self, axis):

        super().plot(axis)

        for event in self.dataSource.events:

            if event == self:

                self.plotPointSelected(axis)

            elif event.inInterval(self.absoluteLimits):

                event.plotPointVisible(axis)

    def getVoltage(self, relativePoint):
        """Returns either the raw or filtered voltage amount for the point of
        this event.
        """

        if self.applicationSettings.plotFiltered:

            return self.dataSource.epochFiltered[relativePoint]

        else:

            return self.dataSource.epoch[relativePoint]

    def plotPointSelected(self, axis):

        axis.plot(*self.pointCoordinatesSeconds, marker='o')

    def plotPointVisible(self, axis):

        axis.plot(*self.pointCoordinatesSeconds, marker='o', color="gray")

    def inInterval(self, interval):

        return self.point >= interval[0] and self.point <= interval[1]
