
from sleepy.tagging.model.event.point import PointEvent
from functools import partial
import pdb

class UserPointEvent(PointEvent):

    def __init__(self, point, dataSource, applicationSettings):

        super().__init__(point, dataSource, applicationSettings)

        self.artist = None

    def plotSelected(self, axis):

        self.artist = axis.plot(*self.pointCoordinatesSeconds, marker='o', picker=5)[0]

    def plotVisible(self, axis):

        self.artist = axis.plot(*self.pointCoordinatesSeconds, marker='o', color="lightgreen", picker=5)[0]

    def onRemove(self):

        self.dataSource.removeEvent(self)
