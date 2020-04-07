
from sleepy.processing._engine import Engine
from sleepy.io.dataset import Dataset
import unittest
from unittest.mock import MagicMock
import numpy as np
import pdb

class MockAlgorithmSimple:

    def extract(self, data):
        pass

    def compute(self, signal):
        # Returns samples whose corresponding amplitudes are lower equal .2
        # (after filtering)
        return [ x for x in range(len(signal.data)) if signal.data[x] <= .2]

    def filter(self, events, data):
        # Filter out values that are above .1 too
        # This is of course a bad example of this filter but it serves the
        # testing scenario, due to its lack of complexity.

        return [ e for e in events if e.amplitude <= .05 ]

class MockAlgorithmExtract:

    def extract(self, data):
        return .2

    def compute(self, threshold, signal):
        # Returns samples whose corresponding amplitudes are lower equal .2
        # (after filtering)
        return [ x for x in range(len(signal.data)) if signal.data[x] <= threshold]

    def filter(self, events, data):
        return events

class MockAlgorithmExtractMulti:

    def extract(self, data):
        return .1, .1

    def compute(self, thresholdA, thresholdB, signal):
        # Returns samples whose corresponding amplitudes are lower equal .2
        # (after filtering)
        return [ x for x in range(len(signal.data)) if signal.data[x] <= (thresholdA + thresholdB)]

    def filter(self, events, data):
        return events

class EngineTest(unittest.TestCase):

    def simpleData():

        data = np.array([
            np.array([
                np.array([.2, .4, .6, .8]),
                np.array([.1, .3, .5, .7]),
                np.array([.4, .3, .2, .05])
            ]),
            np.array([
                np.array([.8, .9, .6, .8]),
                np.array([.3, .3, 3, .05]),
                np.array([.5, .9, .2, .9])
            ])
        ])

        epochs = np.array([[0, 3],[4, 7]])

        return data, epochs

    def simpleScenario(filterMethod):
        """Uses the Dataset base class to create a dummy dataset whose attributes
        can simply be set and retrieved.
        """

        data, epochs = EngineTest.simpleData()

        dataset = Dataset()
        dataset.data = data
        dataset.epochs = epochs
        dataset.samplingRate = 10

        algorithm = MockAlgorithmSimple()

        filter = MagicMock()
        filter.filter = filterMethod

        settings = MagicMock()
        settings.plotFiltered = False

        return algorithm, filter, dataset, settings

    def extractScenario(filterMethod):
        """Like the simple scenario but with a algorithm that uses the extract
        step.
        """

        _, filter, dataset, settings = EngineTest.simpleScenario(lambda x, y: x*2)

        algorithm = MockAlgorithmExtract()

        return algorithm, filter, dataset, settings

    def extractMultiScenario(filterMethod):
        """Like the extract scenario but with a algorithm that uses the extract
        step with multiple parameters.
        """

        _, filter, dataset, settings = EngineTest.extractScenario(lambda x, y: x*2)

        algorithm = MockAlgorithmExtractMulti()

        return algorithm, filter, dataset, settings

    def test_simple_algorithm_computeStep_result(self):
        """Tests whether the correct labels are set to the dataset.
        """

        algorithm, filter, dataset, _ = EngineTest.simpleScenario(lambda x, y: x*2)

        # remove filter method
        algorithm.filter = lambda events, data: events

        result = Engine.run(algorithm, filter, dataset)

        self.assertEqual(len(dataset.labels), 3)

        self.assertEqual(dataset.labels[0].tolist(), [])
        self.assertEqual(dataset.labels[1].tolist(), [0, 7])
        self.assertEqual(dataset.labels[2].tolist(), [3])

    def test_simple_algorithm_result_not_filtered(self):
        """If the dataset calls the engine with the correct parameters,
        then the filter method should produce the desired result.
        """

        result = Engine.run(*EngineTest.simpleScenario(lambda x, y: x*2))

        self.assertEqual(len(result), 3)

        self.assertEqual([e.point for e in result[0]], [])
        self.assertEqual([e.point for e in result[1]], [7])
        self.assertEqual([e.point for e in result[2]], [3])

    def test_extract_algorithm_single_parameter(self):
        """Passes an extract parameter to the compute step.
        """

        result = Engine.run(*EngineTest.extractScenario(lambda x, y: x*2))

        self.assertEqual(len(result), 3)

        self.assertEqual([e.point for e in result[0]], [])
        self.assertEqual([e.point for e in result[1]], [0, 7])
        self.assertEqual([e.point for e in result[2]], [3])

    def test_extract_algorithm_multi_parameter(self):
        """Passes multiple extract parameters to the compute step.
        """

        result = Engine.run(*EngineTest.extractMultiScenario(lambda x, y: x*2))

        self.assertEqual(len(result), 3)

        self.assertEqual([e.point for e in result[0]], [])
        self.assertEqual([e.point for e in result[1]], [0, 7])
        self.assertEqual([e.point for e in result[2]], [3])
