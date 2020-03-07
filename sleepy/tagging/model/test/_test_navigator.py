
import unittest
from unittest.mock import MagicMock, Mock, patch, PropertyMock
from eegplot.gui import LabellingEnvironment
from eegplot.gui.control import LabellingControl
from eegplot.gui.view import LabellingView
#from eegplot.FileLoader import FileLoader
from eegplot.gui.exceptions import UserCancel, NoNavigatorError
from eegplot.gui.model import Navigator

from eegplot.data.source import DataSource
from eegplot.event import PointEvent, PointSample
import numpy as np

import pdb

class ControlTest(unittest.TestCase):

    def setUp(self):

        self.settings = MagicMock()
        self.settings.intervalMin = 0
        self.settings.intervalMax = 10

        self.samplingRate = 10
        self.interval = (0,100)
        self.dataSource = DataSource(
            np.arange(*self.interval,1), self.interval, samplingRate = self.samplingRate
        )

        self.samples = list(
            map(lambda i: self.customPointSample(i), range(3))
        )

    def customPointSample(self, point):

        event = PointEvent(point, self.dataSource, self.settings)

        return PointSample(event)

    """Requirement: The navigator returns the current state of currently
    selected sample. This means that if we navigate through the samples
    we can observe a change in the status.
    """
    def test_isSelectionLabelled_no_navigation(self):

        self.samples[1].switchLabel()

        nav = Navigator(self.samples)

        self.assertFalse(nav.isSelectionLabelled())

    def test_isSelectionLabelled_navigation_labelled(self):

        self.samples[1].switchLabel()

        nav = Navigator(self.samples)

        nav.selectNext()
        self.assertTrue(nav.isSelectionLabelled())

    def test_isSelectionLabelled_navigation_not_labelled(self):

        self.samples[1].switchLabel()

        nav = Navigator(self.samples)

        nav.selectPrevious()
        self.assertFalse(nav.isSelectionLabelled())

    """Requirement: Calling selectClosestToTime(time) sets the navigation to
    the point closest to time in the time-domain.
    """
    def test_selectClosestToTime(self):

        self.samples[2].switchLabel()

        nav = Navigator(self.samples)

        pointInSeconds = 5 / self.samplingRate

        nav.selectClosestToTime(pointInSeconds)

        self.assertTrue(nav.isSelectionLabelled())



if __name__ == '__main__':
    unittest.main()
