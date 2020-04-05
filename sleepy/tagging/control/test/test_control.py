

import unittest
from unittest.mock import MagicMock
from sleepy.tagging.control import TaggingControl
from sleepy.gui.exceptions import UserCancel
from PyQt5.QtWidgets import QMessageBox
from sleepy.test.core import TestBase

class ControlTest(unittest.TestCase):

    def standardScenario():

        env, app, settings = TestBase.getBasics(active = True, name = 'TestApplication')

        control = TaggingControl(env, settings)

        events = TestBase.getEvents([1,2,3], settings, TestBase.getDataSource())

        navigator = TestBase.getNavigator(events, changesMade = False)

        loader = TestBase.getFileLoader(path = "test/path/TestFile", navigators = [navigator])

        return env, app, settings, control, navigator, loader

    def test_open_no_navigator(self):
        """Opening the loader should cause a UserCancel exception.
        """

        env, app, settings = TestBase.getBasics(active = False, name = 'TestApplication')

        control = TaggingControl(env, settings)

        loader = TestBase.getFileLoader(navigators = [])

        try:
            control.open(loader)

        except UserCancel:
            self.assertTrue(True)
            return

        self.assertTrue(False)

    def test_open_empty_navigator(self):
        """Opening the loader should be possible but when the control tries to
        find a navigator in the onAfterActivate method, there should be a UserCancel.
        """

        env, app, settings = TestBase.getBasics(active = False, name = 'TestApplication')

        control = TaggingControl(env, settings)

        events = TestBase.getEvents([], settings)

        loader = TestBase.getFileLoader(navigators = [TestBase.getNavigator(events)])

        control.open(loader)

        env.active = True

        try:
            control.onAfterActivate()
        except UserCancel:
            self.assertTrue(True)
            return

        self.assertTrue(False)

    def test_open_valid_navigator_windowtitle_and_button_red(self):
        """Window title must contain an asterisk.
        """

        env, app, settings, control, navigator, loader = ControlTest.standardScenario()

        navigator.switchSelectionTag()

        control.open(loader)

        control.onAfterActivate()

        app.setWindowTitle.assert_called_with('TestApplication - TestFile*')

    def test_open_valid_navigator_windowtitle_showIndex_no_asterisk(self):
        """Window title must not contain an asterisk but channel and sample
        counter information.
        """

        env, app, settings, control, navigator, loader = ControlTest.standardScenario()

        settings.showIndex = True

        control.open(loader)

        control.onAfterActivate()

        app.setWindowTitle.assert_called_with('TestApplication - TestFile - Channel: 1/1 - Sample: 1/3')

    def test_open_valid_navigator_windowtitle_showIndex(self):
        """Window title must contain an asterisk as well as channel and sample
        counter information.
        """

        env, app, settings, control, navigator, loader = ControlTest.standardScenario()

        settings.showIndex = True

        navigator.switchSelectionTag()

        control.open(loader)

        control.onAfterActivate()

        app.setWindowTitle.assert_called_with('TestApplication - TestFile* - Channel: 1/1 - Sample: 1/3')

    def test_open_valid_navigator_visualizeTag_active_tagged(self):
        """Tagging button must be red on selection-tag switch.
        """

        env, app, settings, control, navigator, loader = ControlTest.standardScenario()

        navigator.switchSelectionTag()

        control.open(loader)
        control.onAfterActivate()

        env.view.setButtonStyle.assert_called_with(
            stylesheet = 'QPushButton { background-color: red; color: white; }',
            text = 'Tagged as False-Positive'
        )

    def test_open_valid_navigator_visualizeTag_active_not_tagged(self):
        """Button must be set gray if not tagged.
        """

        env, app, settings, control, navigator, loader = ControlTest.standardScenario()

        control.open(loader)
        control.onAfterActivate()

        env.view.setButtonStyle.assert_called_with(
            stylesheet = '',
            text = 'Not Tagged'
        )

    def test_open_valid_navigator_with_checkpoints_user_yes(self):
        """Position of navigator should be set to the checkpoint that the
        user approved of.
        """

        env, app, settings, control, navigator, loader = ControlTest.standardScenario()

        settings.useCheckpoints = True

        env.view.askUserForCheckPointRestore = MagicMock(return_value = QMessageBox.Yes)

        checkpoint = 2
        dataset = TestBase.getDataset()
        dataset.getCheckpoint = MagicMock(return_value = checkpoint)

        loader.load = MagicMock(return_value=([navigator], dataset))

        control.open(loader)
        control.onAfterActivate()

        self.assertEqual(
            navigator.position,
            checkpoint
        )

    def test_open_valid_navigator_with_checkpoints_user_no(self):
        """Position of navigator should not be set to the checkpoint that the
        user did not approve of.
        """

        env, app, settings, control, navigator, loader = ControlTest.standardScenario()

        settings.useCheckpoints = True

        env.view.askUserForCheckPointRestore = MagicMock(return_value = QMessageBox.No)

        checkpoint = 2
        dataset = TestBase.getDataset()
        dataset.getCheckpoint = MagicMock(return_value = checkpoint)

        loader.load = MagicMock(return_value=([navigator], dataset))

        control.open(loader)
        control.onAfterActivate()

        self.assertEqual(
            navigator.position,
            0
        )

    def test_open_timeline_intial_call(self):
        """Timeline mock is called with proper arguments given a set of points
        in a navigator.
        """

        env, app, settings, control, navigator, loader = ControlTest.standardScenario()

        control.open(loader)
        control.onAfterActivate()

        dataSource = navigator.events[0].dataSource

        # Timeline is a mock supplied from the view
        control.timeline.plot.assert_called_with(
            [1/dataSource.samplingRate, 2/dataSource.samplingRate, 3/dataSource.samplingRate],
            1/dataSource.samplingRate,
            (0.0, 1.1)
        )

    def test_navigate_timeline_supplied(self):
        """Timeline mock is called with proper arguments given a set of points
        in a navigator on a position update.
        """

        env, app, settings, control, navigator, loader = ControlTest.standardScenario()

        control.open(loader)
        control.onAfterActivate()

        control.onNextClick()

        dataSource = navigator.events[0].dataSource

        control.timeline.update.assert_called_with(
            2/dataSource.samplingRate,
            (0.0, 1.2)
        )

    def test_navigate_forward_active(self):
        """Navigating forward two times increases the position of navigator about
        two.
        """

        env, app, settings, control, navigator, loader = ControlTest.standardScenario()

        control.open(loader)
        control.onAfterActivate()

        self.assertEqual(navigator.position, 0)

        control.onNextClick()
        control.onNextClick()

        self.assertEqual(navigator.position, 2)

    def test_navigate_backward_active(self):
        """Navigating forward two times decreases the position of navigator about
        two.
        """

        env, app, settings, control, navigator, loader = ControlTest.standardScenario()

        control.open(loader)
        control.onAfterActivate()

        self.assertEqual(
            navigator.position,
            0
        )

        control.onPreviousClick()
        control.onPreviousClick()

        self.assertEqual(
            navigator.position,
            1
        )

    def test_onTaggingClick_active_set(self):
        """Clicking on tagging should set the tag of the selected event.
        """

        env, app, settings, control, navigator, loader = ControlTest.standardScenario()

        control.open(loader)
        control.onAfterActivate()

        self.assertEqual(navigator.selectionTag, 0)

        control.onTaggingClick()

        self.assertEqual(navigator.selectionTag, 1)

    def test_onTaggingClick_active_reset(self):
        """Clicking twice on tagging should set and then reset the tag of the selected event.
        """

        env, app, settings, control, navigator, loader = ControlTest.standardScenario()

        control.open(loader)
        control.onAfterActivate()

        self.assertEqual(navigator.selectionTag, 0)

        control.onTaggingClick()
        control.onTaggingClick()

        self.assertEqual(navigator.selectionTag, 0)

    def test_notifyUserOfSwitch_no_changes(self):
        """Without changes made the user should not be asked for saving and
        the save method should not be called.
        """

        env, app, settings, control, navigator, loader = ControlTest.standardScenario()
        env.view.askUserForSwitch = MagicMock()
        control.save = MagicMock()

        control.open(loader)
        control.onAfterActivate()

        control.notifyUserOfSwitch()

        env.view.askUserForSwitch.assert_not_called()
        control.save.assert_not_called()

    def test_notifyUserOfSwitch_changes_cancel(self):
        """Changes were made but checkpoints are disabled in the settings.
        The user cancels the saving process.
        """

        env, app, settings, control, navigator, loader = ControlTest.standardScenario()
        env.view.askUserForSwitch = MagicMock(return_value = QMessageBox.Cancel)
        control.save = MagicMock()

        control.open(loader)
        control.onAfterActivate()

        navigator.switchSelectionTag()

        try:
            control.notifyUserOfSwitch()

            self.assertTrue(False)
        except UserCancel:
            pass

        env.view.askUserForSwitch.assert_called()
        control.save.assert_not_called()

    def test_notifyUserOfSwitch_changes_discard(self):
        """Changes were made but checkpoints are disabled in the settings.
        The user discards the saving process. No UserCancel but also no saving
        methods are called
        """

        env, app, settings, control, navigator, loader = ControlTest.standardScenario()
        env.view.askUserForSwitch = MagicMock(return_value = QMessageBox.Discard)
        control.save = MagicMock()

        control.open(loader)
        control.onAfterActivate()

        navigator.switchSelectionTag()

        control.notifyUserOfSwitch()

        env.view.askUserForSwitch.assert_called()
        control.save.assert_not_called()

        self.assertEqual(navigator.changesMade, True)

    def test_notifyUserOfSwitch_changes_save(self):
        """Changes were made but checkpoints are disabled in the settings.
        The user accepts the saving process.
        1. the loader was called to save the data.
        2. the navigator's onSave method has been called, i.e. changes made are
           reset.
        """

        env, app, settings, control, navigator, loader = ControlTest.standardScenario()
        env.view.askUserForSwitch = MagicMock(return_value = QMessageBox.Save)

        control.open(loader)
        control.onAfterActivate()

        navigator.switchSelectionTag()

        control.notifyUserOfSwitch()

        env.view.askUserForSwitch.assert_called()
        loader.saveAs.assert_called()

        self.assertEqual(navigator.changesMade, False)

    def test_notifyUserOfSwitch_checkpoints_user_no(self):
        """No changes but checkpoints are activated. User answers no.
        """

        env, app, settings, control, navigator, loader = ControlTest.standardScenario()
        env.view.askUserForCheckPoint = MagicMock(return_value = QMessageBox.No)
        settings.useCheckpoints = True

        dataset = TestBase.getDataset()
        dataset.setCheckpoint = MagicMock()

        loader.load = MagicMock(return_value=([navigator], dataset))

        control.open(loader)
        control.onAfterActivate()

        control.notifyUserOfSwitch()

        env.view.askUserForCheckPoint.assert_called()
        dataset.setCheckpoint.assert_not_called()

    def test_notifyUserOfSwitch_checkpoints_user_yes(self):
        """No changes but checkpoints are activated. User answers yes.
        Checkpoint must be set in dataset.
        """

        env, app, settings, control, navigator, loader = ControlTest.standardScenario()
        env.view.askUserForCheckPoint = MagicMock(return_value = QMessageBox.Yes)
        settings.useCheckpoints = True

        dataset = TestBase.getDataset()
        dataset.setCheckpoint = MagicMock()

        loader.load = MagicMock(return_value=([navigator], dataset))

        control.open(loader)
        control.onAfterActivate()

        control.onNextClick()

        control.notifyUserOfSwitch()

        env.view.askUserForCheckPoint.assert_called()
        dataset.setCheckpoint.assert_called_with(1)
