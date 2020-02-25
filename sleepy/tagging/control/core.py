
from sleepy.gui.exceptions import UserCancel, NoNavigatorError
from sleepy.tagging.constants import PATTERN_COUNT, SPACE
from sleepy.tagging.model.timeline import Timeline
from PyQt5.QtWidgets import QMessageBox
from functools import partial

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
        return self.view.app.applicationSettings

    @property
    def showIndex(self):

        return self.applicationSettings.showIndex.value

    @property
    def useCheckpoints(self):

        return self.applicationSettings.useCheckpoints.value

    @property
    def active(self):
        return self.environment.active

    @property
    def filename(self):
        return self.fileLoader.path.split('/')[-1]

    @property
    def timeline(self):

        try:
            return self._timeline
        except AttributeError:

            self._timeline = Timeline()

            return self._timeline

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
            [self.onPosition, self.updateTimeline]
        )

    @navigator.deleter
    def navigator(self):
        del self._navigator

    def onNextClick(self):

        if self.active:

            self.navigator.selectNext(cyclic = True)

    def onPreviousClick(self):

        if self.active:

            self.navigator.selectPrevious(cyclic = True)

    def onTaggingClick(self):

        if self.active:

            self.navigator.switchSelectionTag()

            self.visualizeTag()

    def visualize(self):

        self.updateWindowTitle()

        self.view.addToolBar()

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

    def updateTimeline(self, position):

        points = self.navigator.pointsInSeconds

        currentPoint = self.navigator.currentPointInSeconds

        currentLimits = self.navigator.currentLimitsInSeconds

        plotFunction = partial(
            self.timeline.plot,
            points,
            currentPoint,
            currentLimits
        )

        self.view.plotTimeline(plotFunction)

    def onTimelineClick(self, time):

        self.navigator.selectClosestToTime(time)

    def setCounterString(self, position):

        self.counterString = ''

        if self.showIndex:

            outOf = self.navigator.maximumPosition

            self.counterString = PATTERN_COUNT.format(position + 1, outOf)

        self.updateWindowTitle()

    def open(self, fileLoader):

        self.fileLoader = fileLoader
        navigator = self.fileLoader.load()

        if navigator is None:
            raise NoNavigatorError

        self.navigator = navigator

        self.visualize()

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

        changesMade = self.navigator.changesMade

        # We want to enable that if the user cancels the Save-Dialog, it prompts
        # the question again
        while changesMade:

            reply = self.askUserForSwitch()

            if reply == QMessageBox.Cancel:
                raise UserCancel

            elif reply == QMessageBox.Save:

                try:

                    self.save()
                except UserCancel:
                    continue
            return

    def askUserForSwitch(self):

        return QMessageBox.question(
            self.app, 'Confirm', 'Save changes?',
            QMessageBox.Discard | QMessageBox.Save | QMessageBox.Cancel,
            QMessageBox.Cancel
        )
