
from sleepy.gui.exceptions import UserCancel, NoNavigatorError
from PyQt5.QtWidgets import QMessageBox
import pdb

def visualize(function):
    """Decorator function for methods that should only apply changes if the
    control is active and whose actions neccesitate a rerender of the ui.
    """

    def visualizing(self, *args):

        if self.active:

            function(self, *args)

            self.visualizeTag()

    return visualizing

class TaggingControl:

    def __init__(self, environment, settings):

        self.environment = environment
        self.settings = settings

    @property
    def view(self):
        return self.environment.view

    @property
    def app(self):
        return self.environment.app

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
        """Sets the navigator internally and registers event handlers for a set
        of data events of the navigator. On initialize, the corresponding event
        handlers get called with the initial value of the event and on future
        events, whereas connect only fires upon future events.
        """

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

    @visualize
    def onNextClick(self, *args):
        """Gets registered by the view and is called if the user navigates
        forward. Propagates this action to the navigator and ensures that
        the changes will be reflected by the view.
        """

        self.navigator.selectNext()

    @visualize
    def onPreviousClick(self, *args):
        """Gets registered by the view and is called if the user navigates
        backward. Propagates this action to the navigator and ensures that
        the changes will be reflected by the view.
        """

        self.navigator.selectPrevious()

    @visualize
    def onTaggingClick(self, *args):
        """Gets registered by the view and is called if the user tags an event.
        Propagates this action to the navigator and ensures that
        the changes will be reflected by the view.
        """

        self.navigator.switchSelectionTag()

    @visualize
    def visualizeOnOpen(self, *args):
        """Called when loading new data, before presentation. Updates the
        window title and propagates the open event to the view.
        """

        self.updateWindowTitle()

        self.view.open()

    def onPosition(self, position):
        """Event handler for the :class:`DataEvent` onPosition of the navigator.
        Gives the navigator access to letting its current event plot its
        data on the canvas provided by the view.
        """

        self.view.plot(self.navigator.plot)

        self.updateWindowTitle()

    def redraw(self):
        """Forces update on current position and updates the window title.
        This method is used when e.g. user events are added, to refresh the
        current plot even if the position of the current event has not changed.
        """

        self.onPosition(self.navigator.position)

        self.updateWindowTitle()

    def updateTimeline(self, *args):
        """Updates the timeline on a change of position. This does not require
        every point of the dataset to be redrawn. For that task compare method
        configureTimeline.
        """

        _, currentPoint, currentLimits = self.navigator.getTimelineData()

        self.timeline.update(currentPoint, currentLimits)

        self.view.draw()

    def onTimelineClick(self, time):
        """Handles a double-click on the timeline by telling the navigator
        to select the event that is closest to the timestamp that the user
        double-clicked.
        """

        self.navigator.selectClosestToTime(time)

    def onMainDblClick(self, event):
        """Called if the main figure in the view is double-clicked. This method
        tries to identify the given event as a user event. If this can be done,
        then the user is offered to remove the event. Otherwise, the user is
        offered to create a new user event here. The API-method of the view
        that are called build a context menu and move it to the current cursor
        position. The context menu for event creation is only displayed if the
        user actually clicked on the graph. The navigator offers a method to
        check that.
        """

        userEvent = self.navigator.findUserEvent(event)

        if not userEvent:

            if self.navigator.onGraphClick(event):

                self.view.showMenuUserEventCreate(event)

        else:

            self.view.showMenuUserEventRemove(userEvent)

    def createUserEvent(self, event):
        """Propagates to the navigator to add an event and then forces a redraw.
        """

        self.navigator.addUserEvent(event)

        self.redraw()

        self.configureTimeline()

    def removeUserEvent(self, userEvent):
        """Propagates to the navigator to add a user event and then forces a
        redraw.
        """

        self.navigator.removeUserEvent(userEvent)

        self.redraw()

        self.configureTimeline()

    def open(self, fileLoader):
        """Loads a navigator and a dataset from a specified file loader.
        Before accepting the new data, this method validates whether the
        navigator contains displayable data and tells the user that the
        navigation is flawed otherwise.
        If the navigator is valid, this method buffers navigator and dataset,
        configures the timeline with data from the navigator, restores potential
        checkpoints and fires an initial visualization of the view.
        """

        self.fileLoader = fileLoader
        navigators, dataset = self.fileLoader.load()

        self.installNavigator(navigators[0])

        self.navigators = navigators
        self.dataset = dataset

    def installNavigator(self, navigator):
        """Installs a navigator to the control and checks whether the navigator
        is valid.
        """

        try:
            self.validate(navigator)
        except NoNavigatorError:

            self.view.tellUserNavigationFlawed()

            raise UserCancel

        self.navigator = navigator

    @visualize
    def nextChannel(self):
        """Select the next channel and install the corresponding navigator
        """

        index = ( self.navigators.index(self.navigator) + 1 ) % len(self.navigators)

        self.installNavigator(
            self.navigators[index]
        )

        self.configureTimeline()

    @visualize
    def previousChannel(self):
        """Select the previous channel and install the corresponding navigator
        """

        index = ( self.navigators.index(self.navigator) - 1 ) % len(self.navigators)

        self.installNavigator(
            self.navigators[index]
        )

        self.configureTimeline()

    def onAfterActivate(self):
        """Do visualization after the control has been set active. This involves
        setting up the timeline, restoring checkpoints and visualizing the setup.
        This method should be called by the environment after it was activated.
        """

        self.configureTimeline()

        self.restoreCheckPoint()

        self.visualizeOnOpen()

    def configureTimeline(self):
        """Lets the view create a new timeline and plots the timeline points.
        This method can be used to rerender the entire timeline at any given
        point.
        """

        self.view.clearTimelineAxis()

        self.timeline = self.view.getTimeline()

        timelineData = self.navigator.getTimelineData()

        self.timeline.plot(*timelineData)

        self.view.draw_idle()

    def validate(self, navigator):
        """Validates whether a given navigator exists and contains data. Otherwise
        appropriate messages are displayed to the user and the method raises a
        NoNavigatorError exception.
        """

        if navigator is None:
            raise NoNavigatorError

        if navigator.maximumPosition == 0:

            self.view.tellUserNoEventsFound()

            # By accepting the information, the user automatically cancels
            # the process
            raise NoNavigatorError

    @visualize
    def refresh(self):
        """Forces an update on the current position. Can be used to apply any
        updates on settings-values or similar to the screen.
        """

        self.navigator.onPosition.trigger()

    def save(self):
        """Tells the fileLoader to save the current dataset. If this does not
        result in an exception, then the dataset is considered saved, which
        needs reflection in the navigator (e.g. reset changesMade flag).
        """

        self.fileLoader.saveAs()

        self.navigator.onSave()

    def onSaveFile(self):
        """Wraps around the save method but suppresses the UserCancel and
        returns None instead.
        """

        try:
            self.save()
        except UserCancel:
            return

    def onDeactivate(self):
        """Removes navigator and file loader from the control and tells the view
        to remove the toolbar.
        """

        del self.navigator
        del self.fileLoader

        self.view.removeToolBar()

    def onChangesMade(self, changesMade):
        """Event handler for the changesMade event of the navigator. Keeps track
        of whether changes are made, updates the menu options (save disabled if
        no changes made) and updates the window title.
        """

        self.changesMade = changesMade

        self.updateMenuOptions()

        self.updateWindowTitle()

    def updateWindowTitle(self):
        """Creates a window title for the application based on the currently
        selected filename, the name of the app, whether the user has made
        changes on the dataset and the counter of the current events with
        respect to the number of events detected.
        """

        if self.filename != '':

            windowTitle = '{} - {}'.format(self.app.name, self.filename)

        else:

            windowTitle = self.app.name

        if self.changesMade:

            windowTitle += '*'

        counterString = self.getCounterString()

        if counterString != '':
            windowTitle += " - Sample: {}".format(counterString)

        self.app.setWindowTitle(windowTitle)

    def getCounterString(self):
        """Creates a string containing the current position + 1 and the
        number of events managed by the navigator.
        """

        counterString = ''

        if self.settings.showIndex:

            outOf = self.navigator.maximumPosition

            counterString = '{}/{}'.format(self.navigator.position + 1, outOf)

        return counterString

    def updateMenuOptions(self):
        """Disables the save menu action if no changes are made and disables the
        clear menu action if the control is not active.
        """

        disableSaveOption = not self.changesMade
        self.app.saveFile.setDisabled(disableSaveOption)

        disableClearOption = not self.active
        self.app.clearFile.setDisabled(disableClearOption)

    def notifyUserOfSwitch(self):
        """Starts the creation of a potential checkpoint and asks the user
        whether it is alright to switch to a different dataset or to the
        null screen.
        """

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
        """Tries to recover the last checkpoint saved in the current dataset.
        """

        if self.settings.useCheckpoints:

            checkpoint = self.dataset.getCheckpoint()

            if checkpoint:

                answer = self.view.askUserForCheckPointRestore(checkpoint + 1)

                if answer == QMessageBox.Yes:

                    self.navigator.position = checkpoint

    def setCheckpoint(self):
        """Tries to save the current position as a checkpoint in the dataset.
        """

        if self.settings.useCheckpoints:

            answer = self.view.askUserForCheckPoint()

            if answer == QMessageBox.Yes:

                checkpoint = self.navigator.position

                self.dataset.setCheckpoint(checkpoint)

                self.navigator.changesMade = True

            elif answer == QMessageBox.Cancel:

                raise UserCancel


    def visualizeTag(self):
        """Called by the visualize decorator. This methods decides on the
        stylesheet and text of the tagging button and propagtes this change
        to the view.
        """

        if self.navigator.selectionTag:

            self.view.setButtonStyle(
                stylesheet = 'QPushButton { background-color: red; color: white; }',
                text = 'Tagged as False-Positive'
            )

        else:

            self.view.setButtonStyle(
                stylesheet = '',
                text = 'Not Tagged'
            )
