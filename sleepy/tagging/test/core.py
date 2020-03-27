"""
from unittest.mock import MagicMock, Mock, patch, PropertyMock
import unittest

class TestBase:

    def getIO(path, events = None, changesMade = False):

        loader = MagicMock()
        loader.path = path
        loader.app = self.app

        dataset = MagicMock()

        if events is not None:
            navigator = Navigator(events, changesMade)
            loader.load = MagicMock(return_value=(navigator, dataset))
        else:
            loader.load = MagicMock(return_value=(None, dataset))

        return loader, navigator, dataset

    def getEvents(self, points):

        self.samplingRate = 10
        self.interval = (0,100)
        self.dataSource = DataSource(
            np.arange(*self.interval,1), self.interval, samplingRate = self.samplingRate
        )

        return list(
            map(lambda i: self.customPointSample(i), points)
        )

    def customPointSample(self, point):
        return PointEvent(point, self.dataSource, self.app.applicationSettings)
"""
