
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
            2
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

    def test_changesMade_switchSelectionTag(self):
        """When tag is switched, changes made should be changed.
        """

        _, _, _, navigator = NavigatorTest.standardScenario([1,2,3,4,5])

        self.assertFalse(navigator.changesMade)

        navigator.switchSelectionTag()

        self.assertTrue(navigator.changesMade)

    def test_addUserEvent_getLabelPartition(self):
        """Add two user event and check whether the method getLabelPartition
        returns exactly those two events and no others.
        """

        _, dataSource, _, navigator = NavigatorTest.standardScenario([1,2,3,4,5])

        event = MagicMock()
        event.xdata = 2

        navigator.addUserEvent(event)

        event = MagicMock()
        event.xdata = 4

        navigator.addUserEvent(event)

        computed, user = navigator.getLabelPartition()

        self.assertEqual(user[0], 2 * dataSource.samplingRate)
        self.assertEqual(user[1], 4 * dataSource.samplingRate)
        self.assertEqual(len(user), 2)

    def test_addUserEvent_changesMade(self):
        """Test whether adding a user event causes a positive changesMade flag.
        """

        _, _, _, navigator = NavigatorTest.standardScenario([1,2,3,4,5])

        event = MagicMock()
        event.xdata = 2

        navigator.addUserEvent(event)

        self.assertEqual(navigator.changesMade, True)
