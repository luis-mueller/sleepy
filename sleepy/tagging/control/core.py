
from sleepy.gui.exceptions import UserCancel, NoNavigatorError
from sleepy.tagging.constants import PATTERN_COUNT, SPACE
from PyQt5.QtWidgets import QMessageBox
from functools import partial
from PyQt5.QtWidgets import QMenu, QAction
from PyQt5.QtGui import QCursor
import pdb

class TaggingControl:

    def __init__(self, environment):

        self.environment = environment
        self.counterString = ''

    @property
    def view(self):
        return self.environment.view

    @property
    def app(self):
        return self.environment.app

    @property
    def applicationSettings(self):
        return self.environment.app.applicationSettings

    @property
    def showIndex(self):
        return self.applicationSettings.showIndex

    @property
    def useCheckpoints(self):
        return self.applicationSettings.useCheckpoints

    @property
    def active(self):
        return self.environment.active

    @property
    def filename(self):
        return self.fileLoader.path.split('/')[-1]

    @property
    def navigator(self):
        try:
            return self._navigator
        except AttributeError:
            return None

    @navigator.setter
    def navigator(self, navigator):

        self._navigator = navigator

        self._navigator.onChangesMade.initialize(
            [self.onChangesMade]
        )

        self._navigator.onPosition.initialize(
            [self.onPosition]
        )

        self._navigator.onPosition.connect(
            [self.updateTimeline]
        )

    @navigator.deleter
    def navigator(self):
        del self._navigator

    def onNextClick(self):

        if self.active:

            self.navigator.selectNext(cyclic = True)

            self.visualizeTag()

    def onPreviousClick(self):

        if self.active:

            self.navigator.selectPrevious(cyclic = True)

            self.visualizeTag()

    def onTaggingClick(self):

        if self.active:

            self.navigator.switchSelectionTag()

            self.visualizeTag()

    def visualize(self):

        self.updateWindowTitle()

        self.view.open()

        self.visualizeTag()

    def visualizeTag(self):

        self.view.onTagging(self.navigator.selectionTag)

    def onSaveFile(self):

        try:
            self.save()
        except UserCancel:
            return

    def onPosition(self, position):

        self.view.plot(self.navigator.plot)

        self.setCounterString(position)

    def redraw(self):

        self.onPosition(self.navigator.position)

        self.updateWindowTitle()

    def updateTimeline(self, *args):

        _, currentPoint, currentLimits = self.navigator.getTimelineData()

        self.timeline.update(currentPoint, currentLimits)

        self.view.draw()

    def resetTimeline(self):
        self.timeline.reset()

    def onTimelineClick(self, time):

        self.navigator.selectClosestToTime(time)

    def onMainDblClick(self, event):

        userEvent = self.navigator.findUserEvent(event)

        if not userEvent:

            if self.navigator.onGraphClick(event):

                self.view.showMenuUserEventCreate(event)

        else:

            self.view.showMenuUserEventRemove(userEvent)

    def createUserEvent(self, event):

        self.navigator.addUserEvent(event)

        self.redraw()

    def removeUserEvent(self, userEvent):

        self.navigator.removeUserEvent(userEvent)

        self.redraw()

    def setCounterString(self, position):

        self.counterString = ''

        if self.showIndex:

            outOf = self.navigator.maximumPosition

            self.counterString = PATTERN_COUNT.format(position + 1, outOf)

        self.updateWindowTitle()

    def open(self, fileLoader):

        self.fileLoader = fileLoader
        navigator, dataset = self.fileLoader.load()

        try:
            self.validate(navigator)
        except NoNavigatorError:

            self.view.tellUserNavigationFlawed()

            raise UserCancel

        self.navigator = navigator
        self.dataset = dataset

        self.configureTimeline()

        self.restoreCheckPoint()

        self.visualize()

    def configureTimeline(self):
        """Lets the view create a new timeline and plots the timeline points.
        """

        self.timeline = self.view.getTimeline()

        timelineData = self.navigator.getTimelineData()

        self.timeline.plot(*timelineData)

    def validate(self, navigator):

        if navigator is None:
            raise NoNavigatorError

        if navigator.maximumPosition == 0:

            self.view.tellUserNoEventsFound()

            # By accepting the information, the user automatically cancels
            # the process
            raise NoNavigatorError

    def refresh(self):

        if self.navigator:
            self.onPosition(self.navigator.position)

    def save(self):

        self.fileLoader.saveAs()

        self.navigator.onSave()

    def onDeactivate(self):

        del self.navigator
        del self.fileLoader

        self.view.removeToolBar()

    def onChangesMade(self, changesMade):

        self.changesMade = changesMade

        self.updateMenuOptions()

        self.updateWindowTitle()

    def updateWindowTitle(self):

        if self.filename != '':

            windowTitle = '{} - {}'.format(self.app.name, self.filename)

        else:

            windowTitle = self.app.name

        if self.changesMade:

            windowTitle += '*'

        if self.counterString != '':
            windowTitle += " - Sample: {}".format(self.counterString)

        self.app.setWindowTitle(windowTitle)

    def updateMenuOptions(self):

        disableSaveOption = not self.changesMade
        self.app.saveFile.setDisabled(disableSaveOption)

        disableClearOption = not self.active
        self.app.clearFile.setDisabled(disableClearOption)

    def notifyUserOfSwitch(self):

        self.setCheckpoint()

        changesMade = self.navigator.changesMade

        # We want to enable that if the user cancels the Save-Dialog, it prompts
        # the question again
        while changesMade:

            reply = self.view.askUserForSwitch()

            if reply == QMessageBox.Cancel:
                raise UserCancel

            elif reply == QMessageBox.Save:

                try:

                    self.save()
                except UserCancel:
                    continue
            return

    def restoreCheckPoint(self):

        if self.applicationSettings.useCheckpoints:

            checkpoint = self.dataset.getCheckpoint()

            if checkpoint:

                answer = self.view.askUserForCheckPointRestore(checkpoint + 1)

                if answer == QMessageBox.Yes:

                    self.navigator.position = checkpoint

    def setCheckpoint(self):

        if self.applicationSettings.useCheckpoints:

            answer = self.view.askUserForCheckPoint()

            if answer == QMessageBox.Yes:

                checkpoint = self.navigator.position

                self.dataset.setCheckpoint(checkpoint)

                self.navigator.changesMade = True
