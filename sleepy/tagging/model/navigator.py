
from sleepy.tagging.core import DataEvent
from sleepy.tagging.model.event import UserPointEvent
from sleepy.tagging.model.exceptions import UserEventExists
import numpy as np
import pdb

class Navigator:
    def __init__(self, events, changesMade = False):

        self.events = events
        self.userEvents = []

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

    def getCurrentLabels(self):

        labels = []

        for event in self.events:
            labels.append(event.label)

        return np.array(labels)

    def createUserEvent(self, time):

        pointInSamples = self.selectedEvent.convertSeconds(time)

        currentUserPoints = list(map(lambda e: e.point, self.userEvents))

        if pointInSamples not in currentUserPoints:

            # User-events are always point-events
            return UserPointEvent(
                pointInSamples,
                self.selectedEvent.dataSource,
                self.selectedEvent.applicationSettings
            )
        else:
            raise UserEventExists

    def addUserEvent(self, event):

        try:
            userEvent = self.createUserEvent(event.xdata)
        except UserEventExists:
            return

        selectedEvent = self.selectedEvent

        self.events.append(userEvent)
        self.userEvents.append(userEvent)

        self.ensureConsistency()

        # Make sure that position is updated if inserted before current
        # event
        if selectedEvent.point > userEvent.point:
            self.position += 1

    def removeUserEvent(self, userEvent):

        selectedEvent = self.selectedEvent

        self.events.remove(userEvent)
        self.userEvents.remove(userEvent)

        userEvent.onRemove()

        self.ensureConsistency()

        # Make sure that position is updated if inserted before current
        # event
        if selectedEvent.point > userEvent.point:
            self.position -= 1

    def findUserEvent(self, event):

        userEvent = [
            e for e in self.userEvents if e.artist.contains(event)[0]
        ]

        if userEvent:
            return userEvent[0]

    def onGraphClick(self, event):

        return self.selectedEvent.onGraphClick(event)

    def ensureConsistency(self):

        oldEvents = self.events

        self.events = sorted(
            self.events, key = lambda event: event.point
        )

        self.maximumPosition = len(self.events)

        if oldEvents != self.events:
            self.changesMade = True

    def getTimelineData(self):
        """Returns a set of all points, the currently selected point and the
        currently selected interval, which specifies the data for a timeline,
        as a tuple.
        """

        return (
            self.pointsInSeconds,
            self.currentPointInSeconds,
            self.currentLimitsInSeconds
        )
