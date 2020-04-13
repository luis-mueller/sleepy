
from sleepy.processing.dataset import Dataset
import unittest
from unittest.mock import MagicMock
import numpy as np
import pdb

class DatasetTest(unittest.TestCase):

    def standardScenario():
        """Standard test scenario creating a dataset with rudimental epochs
        and labels. No filtered data is specified.
        """

        dataset = Dataset(None, None)

        dataset.data = np.array([ np.arange(0, 1, .1) for _ in range(5) ])

        dataset.labels = np.array([range(5)])

        dataset.epochs = np.array([
            [0, 9],
            [10, 19],
            [20, 29],
            [30, 39],
            [40, 49]
        ])

        return dataset

    def test_no_tags_from_labels(self):
        """Tags are a numpy array of zeros with the same length as the labels if no
        tags are set otherwise.
        """

        dataset = DatasetTest.standardScenario()

        self.assertEqual([ t.tolist() for t in dataset.tags], [[0] * 5])

    def test_getDataSource_no_filtered_data(self):
        """If the dataset has a data attribute but no filteredData was set,
        simply the data is set as the filteredData.
        """

        dataset = DatasetTest.standardScenario()

        self.assertEqual(dataset.filteredData.tolist(), dataset.data.tolist())

    def test_getDataSource_empty_buffer(self):
        """Having an empty buffer, the dataset should create a new data source
        and retrieve it over the method getDataSource. Further the epoch interval
        of the data source matches the epoch the label belongs to.
        """

        dataset = DatasetTest.standardScenario()

        dataSource = dataset.getDataSource(channel = 0, label = 16)

        self.assertEqual(dataSource.epochInterval.tolist(), [10, 19])

    def test_getDataSource_with_buffer(self):
        """Having a data source in buffer, the dataset should not create a new data source
        but retrieve the existing data source over the method getDataSource.
        """

        dataset = DatasetTest.standardScenario()

        dataSource = dataset.getDataSource(channel = 0, label = 16)

        sameDataSource = dataset.getDataSource(channel = 0, label = 16)

        self.assertEqual(dataSource, sameDataSource)
