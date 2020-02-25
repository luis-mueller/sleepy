
import unittest
from unittest.mock import MagicMock, Mock, patch, PropertyMock
import numpy as np
from numpy import array
from sleepy.io.matfiles import MatDataSet
from sleepy.processing import FileProcessor
from sleepy.tagging.model.event import IntervalEvent, PointEvent
import pdb

class ProcessingTest(unittest.TestCase):

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

    def prepareFileProcessor(self, returnLabels):

        proc = FileProcessor(applicationSettings = None)

        proc.currentAlgorithm = MagicMock()
        proc.currentAlgorithm.compute = MagicMock(return_value = returnLabels)

        return proc

    def test_massimi_algorithm_matfile_run(self):

        proc = self.prepareFileProcessor([0,4])

        labels = proc.run(proc.currentAlgorithm, self.dataSet)

        self.assertTrue(
            np.array_equal(
                labels,

                # Result absolute (includes start of epoch)
                np.array([0,4,25,29])
            )
        )

    def test_massimi_algorithm_matfile_computeNavigator_maximumPosition(self):

        proc = self.prepareFileProcessor([0,4])

        nav = proc.computeNavigator(self.dataSet)

        self.assertTrue(nav.maximumPosition == 4)

    def test_massimi_algorithm_matfile_computeNavigator_event_type_interval(self):

        proc = self.prepareFileProcessor([[0,1],[4,5]])

        nav = proc.computeNavigator(self.dataSet)

        self.assertTrue(isinstance(nav.events[0], IntervalEvent))

        self.assertEqual(nav.events[0].interval, (0,1))
        self.assertEqual(nav.events[1].interval, (4,5))

    def test_massimi_algorithm_matfile_computeNavigator_event_type_point(self):

        proc = self.prepareFileProcessor([0,1,4,23])

        nav = proc.computeNavigator(self.dataSet)

        self.assertTrue(isinstance(nav.events[0], PointEvent))

        self.assertEqual(nav.events[0].point, 0)
        self.assertEqual(nav.events[1].point, 1)
        self.assertEqual(nav.events[2].point, 4)
        self.assertEqual(nav.events[3].point, 23)
