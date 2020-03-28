
from unittest.mock import MagicMock, Mock, patch, PropertyMock
import unittest
from sleepy.tagging.model.datasource import DataSource
from sleepy.tagging.model import Navigator
from sleepy.tagging.model.event import PointEvent
import numpy as np

class TestBase:

    def __init__(self, numberOfPoints):

        self.app = self.getNewApp()

        self.env = self.getEnvironment(self.app)

        self.path = 'TestApplication/Testfile'

        self.samplingRate = 10

        self.numberOfPoints = numberOfPoints

        self.points = list(range(1,self.numberOfPoints + 1))

    def getEnvironment(self, app):

        env = MagicMock()
        env.view = MagicMock()
        env.view.setButtonStyle = MagicMock()
        env.active = False
        env.app = app
        return env

    def getNewApp(self):

        app = MagicMock()
        app.name = 'TestApplication'
        app.applicationSettings = MagicMock()
        app.applicationSettings.showIndex = False
        app.applicationSettings.useCheckpoints = False
        app.applicationSettings.setWindowTitle = MagicMock()
        return app

    def create(self, changesMade = False):

        events = self.getEvents(self.points)

        loader = MagicMock()
        loader.path = self.path
        loader.app = self.app

        dataset = MagicMock()

        if events is not None:
            navigator = Navigator(events, changesMade)
            loader.load = MagicMock(return_value=(navigator, dataset))
        else:
            loader.load = MagicMock(return_value=(None, dataset))

        return loader, navigator, dataset

    def getEvents(self, points):

        self.interval = (points[0] - 1, points[-1] + 1)

        self.dataSource = DataSource(
            np.arange(*self.interval,1), self.interval, self.samplingRate
        )

        return list(
            map(lambda i: self.customPointSample(i), points)
        )

    def customPointSample(self, point):
        return PointEvent(point, self.dataSource, self.app.applicationSettings)
