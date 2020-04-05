
from sleepy.processing._engine import Engine
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

    def filter(self, labels, data):
        # Filter out values that are above .1 too
        # This is of course a bad example of this filter but it serves the
        # testing scenario, due to its lack of complexity.
        result = [
            [
                [
                    x for x in range(len(data[epoch])) if data[channel][epoch][x] <= .1
                ]
                for epoch in range(len(data[channel]))
            ]
            for channel in range(len(data))
        ]

        return np.array(result)

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

        data, epochs = EngineTest.simpleData()

        dataset = MagicMock()
        dataset.data = data
        dataset.epochs = epochs
        dataset.samplingRate = 10

        algorithm = MockAlgorithmSimple()

        filter = MagicMock()
        filter.filter = filterMethod

        return algorithm, filter, dataset

    def test_simple_algorithm(self):

        algorithm, filter, dataset = EngineTest.simpleScenario(lambda x, y: x*2)

        # remove filter method
        algorithm.filter = lambda labels, data: labels

        result = Engine.run(algorithm, filter, dataset)

        self.assertEqual(len(result), 3)

        self.assertEqual(result[0].tolist(), [])
        self.assertEqual(result[1].tolist(), [0, 7])
        self.assertEqual(result[2].tolist(), [3])

    def test_simple_algorithm_with_filter_step(self):

        algorithm, filter, dataset = EngineTest.simpleScenario(lambda x, y: x*2)

        result = Engine.run(algorithm, filter, dataset)

        self.assertEqual(len(result), 3)

        self.assertEqual(result[0].tolist(), [])
        self.assertEqual(result[1].tolist(), [7])
        self.assertEqual(result[2].tolist(), [3])
