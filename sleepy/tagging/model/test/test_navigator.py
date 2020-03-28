
from unittest.mock import MagicMock, Mock, patch, PropertyMock
import unittest
from sleepy.tagging.test.core import TestBase

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
