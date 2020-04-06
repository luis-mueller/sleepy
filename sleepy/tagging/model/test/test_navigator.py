
from unittest.mock import MagicMock
import unittest
from sleepy.test.core import TestBase
import numpy as np

class NavigatorTest(unittest.TestCase):

    def standardScenario(points):
        """Set up a standard scenario for mocking.
        """

        settings = TestBase.getSettings()

        dataSource = TestBase.getDataSource()

        events = TestBase.getEvents(points, settings, dataSource)

        navigator = TestBase.getNavigator(events, changesMade = False)

        return settings, dataSource, events, navigator

    def test_selectNext(self):
        """Navigation forward should increase the position by one.
        """

        settings, dataSource, events, navigator = NavigatorTest.standardScenario([1,2,3])

        navigator.selectNext()

        self.assertEqual(
            navigator.position,
            1
        )

    def test_selectPrevious(self):
        """Navigation backward should decrease the position by one.
        """

        settings, dataSource, events, navigator = NavigatorTest.standardScenario([1,2,3])

        navigator.selectPrevious()

        self.assertEqual(
            navigator.position,
            self.base.numberOfPoints - 1
        )

    def test_selectNext_cyclic(self):
        """Navigation forward as many times as there are events should reset
        the position to 0.
        """

        points = [1,2,3,4,5]

        settings, dataSource, events, navigator = NavigatorTest.standardScenario(points)

        for _ in points:
            navigator.selectNext()

        self.assertEqual(
            navigator.position,
            0
        )

    def test_selectPrevious_cyclic(self):
        """Navigation backward as many times as there are events should reset
        the position to 0.
        """

        points = [1,2,3,4,5]

        settings, dataSource, events, navigator = NavigatorTest.standardScenario(points)

        for _ in points:
            navigator.selectNext()

        self.assertEqual(
            navigator.position,
            0
        )

    def test_selectClosestToTime(self):
        """Construct as time that is very close to the third position. Method
        selectClosestToTime should select the third position.
        """

        _, dataSource, _, navigator = NavigatorTest.standardScenario([1,2,3,4,5])

        time = 3 / dataSource.samplingRate + .003

        navigator.selectClosestToTime(time)

        self.assertEqual(
            navigator.selectedEvent.point,
            3
        )

    def test_plot_nonfilteredData(self):

        settings, dataSource, events, navigator = NavigatorTest.standardScenario(points)

        settings.plotFiltered = False
        settings.pointSize = MagicMock()

        axis = MagicMock()
        axis.plot = MagicMock(return_value = [0])

        navigator.plot(axis)

        axis.plot.assert_called_with(
            0.5, 5, color="gray", marker="o",
            markersize=settings.pointSize
        )

    def test_plot_filteredData(self):

        self.base.app.applicationSettings.plotFiltered = True
        self.base.app.applicationSettings.pointSize = MagicMock()

        loader, nav, dataset = self.base.create()

        axis = MagicMock()
        axis.plot = MagicMock(return_value = [0])

        navigator.plot(axis)

        axis.plot.assert_called_with(
            0.5, 2.5, color="gray", marker="o",
            markersize=self.base.app.applicationSettings.pointSize
        )

    def test_addUserEvent_getLabelPartition(self):
        """Add two user event and check whether the method getLabelPartition
        returns exactly those two events and no others.
        """

        loader, nav, dataset = self.base.create()

        event = MagicMock()
        event.xdata = 2

        navigator.addUserEvent(event)

        event = MagicMock()
        event.xdata = 4

        navigator.addUserEvent(event)

        computed, user = navigator.getLabelPartition()

        self.assertEqual(user[0], 2 * self.base.samplingRate)
        self.assertEqual(user[1], 4 * self.base.samplingRate)
        self.assertEqual(len(user), 2)

    def test_addUserEvent_changesMade(self):
        """Test whether adding a user event causes a positive changesMade flag.
        """

        loader, nav, dataset = self.base.create()

        event = MagicMock()
        event.xdata = 2

        navigator.addUserEvent(event)

        self.assertEqual(navigator.changesMade, True)
