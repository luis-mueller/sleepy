
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pdb

class Timeline:
    def __init__(self):

        self.initialized = False

    @property
    def points(self):
        try:
            return self._points
        except AttributeError:
            return None

    @points.setter
    def points(self, value):

        points = self.points

        self._points = value

        if points:
            if np.array_equal(points, value):

                self.initialized = False

    def plot(self, points, currentPoint, currentInterval, axis):

        self.axis = axis

        self.customize()

        if not self.initialized:
            self.points = points

        self.plotPoints(points)

        self.plotCurrentInterval(currentPoint, currentInterval)

        self.initialized = True

    def customize(self):

        self.axis.set_ylim(0,1)

        self.axis.yaxis.set_visible(False)

        self.axis.xaxis.set_ticks_position('bottom')

        self.axis.get_yaxis().set_ticklabels([])

    def plotPoints(self, points):

        if self.initialized:
            return

        list(map(
            lambda x: self.axis.axvline(x, c = 'darkgrey'), points
        ))

    def plotCurrentInterval(self, currentPoint, currentInterval):

        start, end = currentInterval

        width = end - start

        if not self.initialized:

            self.point = self.axis.axvline(currentPoint, linewidth=2 ,c='coral')
            self.interval = self.axis.axvspan(start, end, alpha=.7)

        else:

            xy = np.array([
                [start, 0],
                [start, 1],
                [end, 1],
                [end, 0],
                [start, 0]
            ])

            self.interval.set_xy(xy)
            self.point.set_xdata(currentPoint)
