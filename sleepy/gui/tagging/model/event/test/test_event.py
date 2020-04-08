from unittest.mock import MagicMock
import unittest
from sleepy.test.core import TestBase
from sleepy.gui.tagging.model.event import PointEvent
import numpy as np
import pdb

class EventTest(unittest.TestCase):

    def getSettings():

        settings = TestBase.getSettings()

        settings.intervalMin = 3.0
        settings.intervalMax = 3.0
        settings.plotFiltered = False

        return settings

    def getPointEvent(point, interval = (0,100)):
        """Creates a new point event for mocking.
        """

        settings = EventTest.getSettings()

        dataSource = TestBase.getDataSource(interval = interval)

        event = PointEvent(point, dataSource, settings)

        return event, dataSource, settings

    def newSettings():

        settings = MagicMock()
        settings.intervalMin = 3.0
        settings.intervalMax = 3.0
        settings.plotFiltered = False

        return settings

    def test_switchTag_single(self):
        """Switching the tag once should set the tag.
        """

        point, interval = 2, (0,7)

        event, _, _ = EventTest.getPointEvent(point, interval)

        event.switchTag()

        self.assertEqual(
            event.binaryTag,
            1
        )

    def test_switchTag_double(self):
        """Switching the tag double should reset the tag.
        """

        point, interval = 2, (0,7)

        event, _, _ = EventTest.getPointEvent(point, interval)

        event.switchTag()
        event.switchTag()

        self.assertEqual(
            event.binaryTag,
            0
        )

    """
        def test_plot_nonfilteredData(self):

            points = [1,2,3]

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

            argumentsPlot = axis.plot.call_args_list[0][0]

            self.assertEqual(
                argumentsPlot[0].tolist(),
                (np.array(points) / dataSource.samplingRate).tolist()
            )

            self.assertEqual(
                argumentsPlot[1].tolist(),
                (np.array(points) / dataSource.samplingRate).tolist()
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
    """
