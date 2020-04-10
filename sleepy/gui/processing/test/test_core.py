
from sleepy.test.core import TestBase
from sleepy.gui.processing.core import Preprocessing
from sleepy.gui.processing.supported import SUPPORTED_DATASETS
from sleepy.processing.dataset import Dataset

import unittest
from unittest.mock import MagicMock, patch
import numpy as np

class MockingDataset(Dataset):

    @property
    def userLabels(self):
        """User labels are squeezed on channel level.
        """
        return [np.array([3,4]),np.array([3,5])]

    def getDataSourceForLabel(self, channel, label):
        return TestBase.getDataSource()

class ProcessingTest(unittest.TestCase):

    def standardScenario(extension = "test"):
        """Creates a standard scenario for testing. Overrides SUPPORTED_DATASETS,
        to mock a dataset type.
        """

        _ , app, settings = TestBase.getBasics(active = False, name = "Test")

        app.supportedDatasets = { "TEST" : Dataset, "MOCK" : MockingDataset }
        app.supportedFilters = app.supportedAlgorithms = []

        proc = Preprocessing(app)

        proc.path = "path/to/test/file." + extension

        proc.view = MagicMock()

        SUPPORTED_DATASETS = { "test" : Dataset }

        dataSource = TestBase.getDataSource()

        events = TestBase.getChannelEvents([
            [1,6,8],
            [2,5,6]
        ], settings, dataSource)

        return app, settings, proc, events

    @patch('sleepy.gui.processing.core.Engine')
    def call(self, function, events_value, engine):
        """Patched call of a function calling engine.run in its core. Returns the
        engine_value to the caller.
        """

        engine.run = MagicMock(return_value = events_value)

        return function()

    def test_load_accepted(self):
        """Calling load leads to an accepted view (mocked).
        """

        app, settings, proc, events = ProcessingTest.standardScenario()

        self.call(proc.load, events)

        proc.view.accept.assert_called()

    def test_load_simple(self):
        """Calling load calls the Engine.run method with the only dataset
        available (test) and converts the returned events into a set of
        navigators.
        """

        app, settings, proc, events = ProcessingTest.standardScenario()

        self.call(proc.load, events)

        self.assertEqual(proc.navigators[0].events, events[0])
        self.assertEqual(proc.navigators[1].events, events[1])

        self.assertTrue(isinstance(proc.dataset, Dataset))

    def test_load_userEvents_created(self):
        """Calling load leads to user events being created on the navigator.
        """

        app, settings, proc, events = ProcessingTest.standardScenario("mock")

        self.call(proc.load, events)

        self.assertEqual(
            [ e.point for e in proc.navigators[0].userEvents ],
            [3,4]
        )

        self.assertEqual(
            [ e.point for e in proc.navigators[1].userEvents ],
            [3,5]
        )
