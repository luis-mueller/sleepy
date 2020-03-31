from unittest.mock import MagicMock, Mock, patch, PropertyMock
import unittest
from sleepy.tagging.test.core import TestBase
from sleepy.tagging.model.datasource import DataSource
from sleepy.tagging.model.event import PointEvent, IntervalEvent
import numpy as np
import pdb

class EventTest(unittest.TestCase):

    def setUp(self):
        pass

    def called_with_args(self, mockObject, callIndex = 0, *args):
        """Util for comparing called arguments of a mockObject. callIndex refers
        to the (callIndex + 1)th call of mockObject.
        """

        arguments = mockObject.call_args_list[callIndex][0]

        for index in range(len(arguments)):

            if issubclass(type(args[index]), np.ndarray):

                valid = np.array_equal(args[index], arguments[index])

                if not valid:
                    print("{} != {}". format(args[index], arguments[index]))
                self.assertTrue(valid)

            else:

                self.assertEqual(args[index], arguments[index])


    def newDataSource(interval, samplingRate):

        start, end = interval

        return DataSource(
            np.random.rand(end - start + 1),
            np.random.rand(end - start + 1),
            interval,
            samplingRate
        )

    def newSettings():

        settings = MagicMock()
        settings.intervalMin = 3.0
        settings.intervalMax = 3.0
        settings.plotFiltered = False

        return settings

    def newPointEvent(point, start, end, samplingRate = 10):

        dataSource = EventTest.newDataSource((start, end), samplingRate)
        settings = EventTest.newSettings()

        event = PointEvent(point, dataSource, settings)

        return event, dataSource, settings

    def newIntervalEvent(intervalStart, intervalEnd, start, end, samplingRate = 10):

        dataSource = EventTest.newDataSource((start, end), samplingRate)
        settings = EventTest.newSettings()

        event = IntervalEvent(intervalStart, intervalEnd, dataSource, settings)

        return event, dataSource, settings

    def test_switchTag_single(self):

        event, _, _ = EventTest.newPointEvent(2, 0, 7, 10)

        event.switchTag()

        self.assertEqual(
            event.binaryTag,
            1
        )

    def test_switchTag_double(self):

        event, _, _  = EventTest.newPointEvent(2, 0, 7, 10)

        event.switchTag()
        event.switchTag()

        self.assertEqual(
            event.binaryTag,
            0
        )

    def test_point_plot_intervals_min_max_wider(self):
        """Test whether the correct data is plotted if the intervalMin, intervalMax
        settings are set to be wider than the actual epoch interval.
        This should display the whole epoch data.
        """

        samplingRate = 10
        point = 2
        start = 0
        end = 7

        event, dataSource, settings = EventTest.newPointEvent(point, start, end, samplingRate)

        # ensure wider than epochInterval
        settings.intervalMin = end / samplingRate
        settings.intervalMax = end / samplingRate

        axis = MagicMock()
        axis.plot = MagicMock(return_value = [None])

        event.plot(axis)

        self.called_with_args(axis.plot, 0,
            np.array([0,1,2,3,4,5,6,7]) / samplingRate,
            dataSource.epoch
        )

    def test_point_plot_intervals_min_max_narrower(self):
        """Test whether the correct data is plotted if the intervalMin, intervalMax
        settings are set to be narrower than the actual epoch interval.
        This should display only a part of the data.
        """

        samplingRate = 10
        point = 2
        start = 0
        end = 7

        event, dataSource, settings = EventTest.newPointEvent(point, start, end, samplingRate)

        # ensure 1,2,3 samples
        settings.intervalMin = 1 / samplingRate
        settings.intervalMax = 1 / samplingRate

        axis = MagicMock()
        axis.plot = MagicMock(return_value = [None])

        event.plot(axis)

        self.called_with_args(axis.plot, 0,
            np.array([1,2,3]) / samplingRate,
            np.array([dataSource.epoch[1],dataSource.epoch[2],dataSource.epoch[3]]),

            # Needed for comparison
            2
        )

    def test_interval_plot_intervals_min_max_wider(self):
        """Test whether the correct data is plotted if the intervalMin, intervalMax
        settings are set to be wider than the actual epoch interval.
        This should display the whole epoch data.
        """

        samplingRate = 10
        intervalStart, intervalEnd = 3, 5
        start = 0
        end = 7

        event, dataSource, settings = EventTest.newIntervalEvent(intervalStart, intervalEnd, start, end, samplingRate)

        # ensure wider than epochInterval
        settings.intervalMin = end / samplingRate
        settings.intervalMax = end / samplingRate

        axis = MagicMock()
        axis.plot = MagicMock(return_value = [None])

        event.plot(axis)

        self.called_with_args(axis.plot, 0,
            np.array([0,1,2,3,4,5,6,7]) / samplingRate,
            dataSource.epoch,

            # Needed for comparison
            2
        )

    def test_interval_plot_intervals_min_max_narrower(self):
        """Test whether the correct data is plotted if the intervalMin, intervalMax
        settings are set to be narrower than the actual epoch interval.
        This should display only a part of the data.
        """

        samplingRate = 10
        intervalStart, intervalEnd = 3, 5
        start = 0
        end = 7

        event, dataSource, settings = EventTest.newIntervalEvent(intervalStart, intervalEnd, start, end, samplingRate)

        # ensure 2,3,4,5,6 samples
        settings.intervalMin = 1 / samplingRate
        settings.intervalMax = 1 / samplingRate

        axis = MagicMock()
        axis.plot = MagicMock(return_value = [None])

        event.plot(axis)

        self.called_with_args(axis.plot, 0,
            np.array([2,3,4,5,6]) / samplingRate,
            np.array([dataSource.epoch[2],dataSource.epoch[3],dataSource.epoch[4],dataSource.epoch[5],dataSource.epoch[6]]),

            # Needed for comparison
            2
        )

    def test_point_plot_other_events_in_range(self):
        """Point: Tests that events in the the same dataSource are plotted too,
        if they are in the visible range.
        """

        samplingRate = 10
        start = 0
        end = 7

        event, dataSource, settings = EventTest.newPointEvent(2, start, end, samplingRate)

        eventIn = PointEvent(3, dataSource, settings)
        eventIn.plotVisible = MagicMock()
        eventOut = PointEvent(6, dataSource, settings)
        eventOut.plotVisible = MagicMock()

        # ensure 1,2,3 samples
        settings.intervalMin = 1 / samplingRate
        settings.intervalMax = 1 / samplingRate

        axis = MagicMock()
        axis.plot = MagicMock(return_value = [None])

        event.plot(axis)

        eventIn.plotVisible.assert_called()
        eventOut.plotVisible.assert_not_called()

    def test_interval_plot_other_events_in_range(self):
        """Interval: Tests that events in the the same dataSource are plotted too,
        if they are in the visible range.
        """

        samplingRate = 10
        start = 0
        end = 7

        event, dataSource, settings = EventTest.newIntervalEvent(2,3, start, end, samplingRate)

        eventIn = IntervalEvent(3,4, dataSource, settings)
        eventIn.plotVisible = MagicMock()
        eventOut = IntervalEvent(6,7, dataSource, settings)
        eventOut.plotVisible = MagicMock()

        # Start is inside of visible area, but end is not
        eventOutOverlap = IntervalEvent(3,5, dataSource, settings)
        eventOutOverlap.plotVisible = MagicMock()

        # ensure 2,3,4 samples
        settings.intervalMin = 1 / samplingRate
        settings.intervalMax = 1 / samplingRate

        axis = MagicMock()
        axis.plot = MagicMock(return_value = [None])

        event.plot(axis)

        eventIn.plotVisible.assert_called()
        eventOut.plotVisible.assert_not_called()
        eventOutOverlap.plotVisible.assert_not_called()
