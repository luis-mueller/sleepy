
import unittest
from unittest.mock import MagicMock, Mock, patch, PropertyMock
import numpy as np
from numpy import array
from sleepy.io.matfiles import MatDataSet
from sleepy.processing import FileProcessor
import pdb

class MatDataSetTest(unittest.TestCase):

    def setUp(self):

        vectorSize = 25

        # IMPORTANT: Creating a realistic channelData for this filetype requires
        # to squeeze the data in the first and only the first dimension. This
        # creates data is not akin to the actual loadmat-results but can be used
        # to mock the MatDataSet. Further: Length of vecotrs > 15, as filtfilt
        # produces and error otherwise
        self.dataSet = MatDataSet(
            {
                '__header__': b'Testdata', '__version__': '1.0', '__globals__': [],
                'channelData': np.array([[
                    [np.zeros(vectorSize)],
                    [np.zeros(vectorSize)]
                ]]),
                'label': np.array([[ 1,  3]]),
                'sampleInfo': np.array([[  0,  (vectorSize - 1)],[ vectorSize, (2 * vectorSize) -1]])
            }
        )

        self.dataSetTagged = MatDataSet(
            {
                '__header__': b'Testdata', '__version__': '1.0', '__globals__': [],
                'channelData': np.array([[
                    [np.zeros(vectorSize)],
                    [np.zeros(vectorSize)]
                ]]),
                'label': np.array([1, 3, 25, 27]),
                'sampleInfo': np.array([[  0,  (vectorSize - 1)],[ vectorSize, (2 * vectorSize) -1]]),
                'tags': np.array([[0,0,1,1]])
            }
        )

    def test_property_labels_migrate_tags(self):

        self.dataSetTagged.labels = np.array([0,4,25,29])

        self.assertTrue(
            np.array_equal(
                self.dataSetTagged.tags,
                np.array([0,0,1,0])
            )
        )

        self.assertTrue(
            np.array_equal(
                self.dataSetTagged.labels,
                np.array([0,4,25,29])
            )
        )

    def test_property_labels_migrate_tags_incompliant_type(self):

        self.dataSetTagged.labels = np.array([[0,1],[4,5],[25,26],[29,30]])

        self.assertTrue(
            np.array_equal(
                self.dataSetTagged.tags,
                np.array([0,0,0,0])
            )
        )

    def test_getDataSourceFor_sameEpoch(self):

        self.dataSet.labels = np.array([0,4,25,29])

        self.assertTrue(
            self.dataSet.getDataSourceFor(0) == self.dataSet.getDataSourceFor(1)
        )

        self.assertTrue(
            self.dataSet.getDataSourceFor(2) == self.dataSet.getDataSourceFor(3)
        )

    def test_getDataSourceFor_notSameEpoch(self):

        self.dataSet.labels = np.array([0,4,25,29])

        self.assertTrue(
            self.dataSet.getDataSourceFor(0) != self.dataSet.getDataSourceFor(2)
        )
