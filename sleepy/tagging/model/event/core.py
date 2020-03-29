
import numpy as np
from matplotlib.axes import Axes
import pdb

class Event:

    def __init__(self, dataSource, applicationSettings):

        self.dataSource = dataSource
        dataSource.addEvent(self)

        self.applicationSettings = applicationSettings
        self.binaryTag = 0

        self.lineArtist = None

    @property
    def label(self):
        raise NotImplementedError

    @property
    def intervalMin(self):
        return self.applicationSettings.intervalMin

    @property
    def intervalMax(self):
        return self.applicationSettings.intervalMax

    @property
    def epochInterval(self):
        return self.dataSource.epochInterval

    @property
    def interval(self):
        raise NotImplementedError

    @property
    def samplingRate(self):
        return self.dataSource.samplingRate

    @property
    def currentPointInSeconds(self):
        raise NotImplementedError

    def convertSeconds(self, seconds):

        return int(
            float(seconds) * self.samplingRate
        )

    def convertSamples(self, samples):

        return samples / self.samplingRate

    @property
    def absoluteLimits(self):

        epochStart, epochEnd = self.epochInterval
        eventStart, eventEnd = self.interval

        if eventStart < epochStart:
            eventStart = epochStart

        if eventEnd > epochEnd:
            eventEnd = epochEnd

        return eventStart, eventEnd

    @property
    def relativeLimits(self):

        eventStart, eventEnd = self.absoluteLimits

        return eventStart - self.epochInterval[0], eventEnd - self.epochInterval[0]

    @property
    def absoluteLimitsInSeconds(self):

        start, end = self.absoluteLimits

        return (start / self.samplingRate, end / self.samplingRate)

    def plot(self, axis):

        x = np.arange(*self.absoluteLimits, 1) / self.samplingRate

        y = self.getYData()

        self.lineArtist = axis.plot(x, y, picker = 2)[0]

        self.setTicks(axis)

        self.labelAxes(axis)

    def getYData(self):
        """Get the data for the Y-axis. This is eiter the raw or the filtered
        data.
        """

        limits = self.relativeLimits

        if self.applicationSettings.plotFiltered:

            return self.dataSource.getFiltered(*limits)

        else:

            return self.dataSource.get(*limits)

    def setTicks(self, axis):

        tickFrequency = int(self.applicationSettings.plotGridSize * self.samplingRate)

        axis.set(
            xticks = np.arange(*self.absoluteLimits, tickFrequency) / self.samplingRate,
            xticklabels = np.arange(*self.absoluteLimits, 1) / self.samplingRate
        )


    def labelAxes(self, axis):

        if not isinstance(axis, Axes):

            axis.xlabel("Time (s)")
            axis.ylabel("Voltage ($\mu V$)")

        else:

            axis.set_xlabel("Time (s)")
            axis.set_ylabel("Voltage ($\mu V$)")

    @property
    def tagged(self):
        return self.binaryTag

    def switchTag(self):

        if self.binaryTag == 0:

            self.binaryTag = 1
        else:

            self.binaryTag = 0

    def onGraphClick(self, event):

        return self.lineArtist.contains(event)[0]
