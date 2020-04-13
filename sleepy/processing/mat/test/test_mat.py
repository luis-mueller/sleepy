
from sleepy.processing.mat.core import MatDataset
from sleepy.test.core import TestBase
import unittest
from unittest.mock import MagicMock
import numpy as np
import pdb

class MatDatasetTest(unittest.TestCase):

    def basicRaw():
        """Basic raw data without sleepy content.
        """

        raw = {
            "trial" : np.array([ np.arange(0, 1, .1) for _ in range(5) ]),
            "sampleinfo" : np.array([
                [0, 9],
                [10, 19],
                [20, 29],
                [30, 39],
                [40, 49]
            ])
        }

        return raw

    def standardScenario():
        """Standard scenario for saving.
        """

        _ , _ , settings = TestBase.getBasics(active = True, name = 'TestApplication')

        dataSource = TestBase.getDataSource()

        events = TestBase.getEvents([1,2,3], settings, dataSource)

        navigator = TestBase.getNavigator(events, changesMade = False)

        event = MagicMock()
        event.xdata = 2 / dataSource.samplingRate
        navigator.addUserEvent(event)

        return navigator, events

    def test_data_and_epochs_extracted(self):
        """Inputting a basic raw creates a dataset with data and epochs supported.
        """

        raw = MatDatasetTest.basicRaw()

        dataset = MatDataset(raw, None)

        self.assertTrue(dataset.epochs is not None)
        self.assertTrue(dataset.data is not None)

    def test_empty_userLabels(self):
        """Creating the dataset without further input should create an empty array
        on the attribute userLabels.
        """

        raw = MatDatasetTest.basicRaw()

        dataset = MatDataset(raw, None)

        self.assertEqual(dataset.userLabels.tolist(), [])

    def test_set_userLabels_changesMade(self):
        """Setting new userLabels sets changesMade to true.
        """

        raw = MatDatasetTest.basicRaw()

        dataset = MatDataset(raw, None)

        dataset.userLabels = np.array([1,2,3])

        self.assertTrue(dataset.changesMade)

    def test_save_userLabels_and_tags_are_extracted_correctly(self):
        """Saving the dataset must set the raw data to the correct values from
        the navigators provided. The tags of the user events are ignored.
        The standard scenario adds one user event at sample 2.
        """

        navigator, events = MatDatasetTest.standardScenario()

        raw = MatDatasetTest.basicRaw()

        path = "/path/to/a/file"

        dataset = MatDataset(raw, None)

        dataset.saveToDisk = MagicMock(return_value = None)

        dataset.save(path, [navigator, navigator])

        self.assertEqual(dataset.userLabels.tolist(), [[2],[2]])
        self.assertEqual(dataset.tags.tolist(), [[0,0,0],[0,0,0]])

        dataset.saveToDisk.assert_called_with(path)
