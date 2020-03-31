
from unittest.mock import MagicMock, Mock, patch, PropertyMock
import unittest
from sleepy.tagging.test.core import TestBase
import numpy as np

class NavigatorTest(unittest.TestCase):

    def setUp(self):

        self.base = TestBase(numberOfPoints = 5)

    def test_selectNext(self):

        loader, nav, dataset = self.base.create()

        nav.selectNext()

        self.assertEqual(
            nav.position,
            1
        )

    def test_selectPrevious(self):

        loader, nav, dataset = self.base.create()

        nav.selectPrevious()

        self.assertEqual(
            nav.position,
            self.base.numberOfPoints - 1
        )

    def test_selectClosestToTime(self):

        loader, nav, dataset = self.base.create()

        time = 3 / self.base.samplingRate + .003

        nav.selectClosestToTime(time)

        self.assertEqual(
            nav.selectedEvent.point,
            3
        )

    def test_plot_nonfilteredData(self):

        self.base.app.applicationSettings.plotFiltered = False
        self.base.app.applicationSettings.pointSize = MagicMock()

        loader, nav, dataset = self.base.create()

        axis = MagicMock()
        axis.plot = MagicMock(return_value = [0])

        nav.plot(axis)

        axis.plot.assert_called_with(
            0.5, 5, color="gray", marker="o",
            markersize=self.base.app.applicationSettings.pointSize
        )

    def test_plot_filteredData(self):

        self.base.app.applicationSettings.plotFiltered = True
        self.base.app.applicationSettings.pointSize = MagicMock()

        loader, nav, dataset = self.base.create()

        axis = MagicMock()
        axis.plot = MagicMock(return_value = [0])

        nav.plot(axis)

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

        nav.addUserEvent(event)

        event = MagicMock()
        event.xdata = 4

        nav.addUserEvent(event)

        computed, user = nav.getLabelPartition()

        self.assertEqual(user[0], 2 * self.base.samplingRate)
        self.assertEqual(user[1], 4 * self.base.samplingRate)
        self.assertEqual(len(user), 2)

    def test_addUserEvent_changesMade(self):
        """Test whether adding a user event causes a positive changesMade flag.
        """

        loader, nav, dataset = self.base.create()

        event = MagicMock()
        event.xdata = 2

        nav.addUserEvent(event)

        self.assertEqual(nav.changesMade, True)
