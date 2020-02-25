
from sleepy.tagging.core import DataEvent
from sleepy.tagging.constants import SLASH
import numpy as np
import pdb

class Navigator:
    def __init__(self, events, changesMade = False):

        self.events = events

        self.maximumPosition = len(events)

        self.finished = False

        self.stateBeforeChanges = self.getCurrentTags()

        self.changesMadeBeforeCreation = changesMade

        self.onChangesMade = DataEvent(changesMade)
        self.onPosition = DataEvent(0)

    @property
    def position(self):
        return self.onPosition.value

    @position.setter
    def position(self, value):
        self.onPosition.value = value

    @property
    def changesMade(self):
        return self.onChangesMade.value

    @changesMade.setter
    def changesMade(self, value):
        self.onChangesMade.value = value

    @property
    def currentPointInSeconds(self):
        return self.selectedEvent.currentPointInSeconds

    @property
    def currentLimitsInSeconds(self):
        return self.selectedEvent.absoluteLimitsInSeconds

    @property
    def pointsInSeconds(self):
        return list(map(lambda e: e.currentPointInSeconds, self.events))

    @property
    def selectedEvent(self):
        if not self.finished:
            return self.events[self.position]

    @property
    def tagsInSeconds(self):

        selectedEvents = list(filter(lambda e: e.tagged, self.events))

        return list(map(lambda e: e.currentPointInSeconds, selectedEvents))

    @property
    def selectionTag(self):
        return self.selectedEvent.tagged

    def selectNext(self, cyclic = True):

        if (self.position + 1) == self.maximumPosition:
            if cyclic:
                self.position = 0
            else:
                self.finished = True
        else:
            self.position += 1

    def selectPrevious(self, cyclic = True):

        if self.position == 0:
            if cyclic:
                self.position = self.maximumPosition - 1
            else:
                self.finished = True
        else:
            self.position -= 1

    def selectClosestToTime(self, time):

        pointsInSeconds = np.array(self.pointsInSeconds)

        self.position = np.argmin(np.abs(pointsInSeconds - time))

    def reset(self):
        self.finished = False
        self.position = 0

    def plot(self, axis):
        self.selectedEvent.plot(axis)

    def switchSelectionTag(self):
        self.selectedEvent.switchTag()

        self.changesMade = not np.all(
            self.stateBeforeChanges == self.getCurrentTags()
        ) or self.changesMadeBeforeCreation

    def onSave(self):

        self.changesMade = False

        self.changesMadeBeforeCreation = False

        self.stateBeforeChanges = self.getCurrentTags()

    def getCurrentTags(self):

        tags = []

        for event in self.events:
            tags.append(event.tagged)

        return np.array(tags)
