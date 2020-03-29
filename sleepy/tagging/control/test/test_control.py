
import unittest
import pdb
import numpy as np
from unittest.mock import MagicMock, Mock, patch, PropertyMock
from sleepy.tagging.environments import TaggingEnvironment
from sleepy.tagging.model import Navigator
from sleepy.tagging.model.event import PointEvent
from sleepy.tagging.control import TaggingControl
from sleepy.tagging.model import DataSource
from sleepy.gui.exceptions import UserCancel, NoNavigatorError
from PyQt5.QtWidgets import QMessageBox

class ControlTest(unittest.TestCase):

    def getEnvironment(self):

        env = MagicMock()
        env.view = MagicMock()
        env.view.setButtonStyle = MagicMock()
        env.active = False
        env.app = self.app
        return env

    def getNewApp(self):

        app = MagicMock()
        app.name = 'TestApplication'
        app.applicationSettings = MagicMock()
        app.applicationSettings.setWindowTitle = MagicMock()
        return app

    def getFileLoader(self, path, events = None, changesMade = False):

        loader = MagicMock()
        loader.path = path
        loader.app = self.app

        self.dataset = MagicMock()

        if events is not None:
            self.navigator = Navigator(events, changesMade)
            loader.load = MagicMock(return_value=(self.navigator, self.dataset))
        else:
            loader.load = MagicMock(return_value=(None, self.dataset))
        return loader

    def getEvents(self, points):

        self.samplingRate = 10
        self.interval = (0,100)
        self.dataSource = DataSource(
            np.arange(*self.interval,1),np.arange(*self.interval,1), self.interval, samplingRate = self.samplingRate
        )

        return list(
            map(lambda i: self.customPointSample(i), points)
        )

    def customPointSample(self, point):
        return PointEvent(point, self.dataSource, self.app.applicationSettings)

    def setUp(self):

        self.app = self.getNewApp()

        self.env = self.getEnvironment()

        self.settings = MagicMock()
        self.settings.showIndex = False
        self.settings.useCheckpoints = False

    def test_open_no_navigator(self):

        control = TaggingControl(self.env, self.settings)

        loader = self.getFileLoader('test/path')

        try:
            control.open(loader)
            control.onAfterActivate()
        except UserCancel:
            self.assertTrue(True)
            return

        self.assertTrue(False)

    def test_open_empty_navigator(self):

        control = TaggingControl(self.env, self.settings)

        loader = self.getFileLoader('test/path', self.getEvents([]), changesMade = False)

        try:
            control.open(loader)
            control.onAfterActivate()
        except UserCancel:
            self.assertTrue(True)
            return

        self.assertTrue(False)

    def test_open_valid_navigator_changesMade_False_no_checkpoints_no_index_with_filename(self):

        self.settings.useCheckpoints = False
        self.settings.showIndex = False

        control = TaggingControl(self.env, self.settings)

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]), changesMade = False)

        self.navigator.switchSelectionTag()

        control.open(loader)
        control.onAfterActivate()

        self.app.setWindowTitle.assert_called_with('TestApplication - TestFile*')

        self.env.view.setButtonStyle.assert_not_called()

    def test_open_valid_navigator_changesMade_False_no_checkpoints_with_index_with_filename(self):

        self.settings.useCheckpoints = False
        self.settings.showIndex = True

        control = TaggingControl(self.env, self.settings)

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]), changesMade = False)

        self.navigator.switchSelectionTag()

        control.open(loader)
        control.onAfterActivate()

        self.app.setWindowTitle.assert_called_with('TestApplication - TestFile* - Sample: 1/3')

        self.env.view.setButtonStyle.assert_not_called()

    def test_open_valid_navigator_changesMade_Initially_no_checkpoints_no_index_with_filename(self):

        self.settings.useCheckpoints = False
        self.settings.showIndex = True

        control = TaggingControl(self.env, self.settings)

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]), changesMade = True)

        control.open(loader)
        control.onAfterActivate()

        self.app.setWindowTitle.assert_called_with('TestApplication - TestFile* - Sample: 1/3')

        self.env.view.setButtonStyle.assert_not_called()

    def test_open_valid_navigator_visualizeTag_active_tagged(self):

        control = TaggingControl(self.env, self.settings)

        self.env.active = True

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]), changesMade = False)

        self.navigator.switchSelectionTag()

        control.open(loader)
        control.onAfterActivate()

        self.env.view.setButtonStyle.assert_called_with(
            stylesheet = 'QPushButton { background-color: red; color: white; }',
            text = 'Tagged as False-Positive'
        )

    def test_open_valid_navigator_visualizeTag_active_tagged(self):

        control = TaggingControl(self.env, self.settings)

        self.env.active = True

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]), changesMade = True)

        control.open(loader)
        control.onAfterActivate()

        self.env.view.setButtonStyle.assert_called_with(
            stylesheet = '',
            text = 'Not Tagged'
        )

    def test_open_valid_navigator_changesMade_False_with_checkpoints_user_yes(self):

        self.settings.useCheckpoints = True

        self.env.view.askUserForCheckPointRestore = MagicMock(return_value = QMessageBox.Yes)

        control = TaggingControl(self.env, self.settings)

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]))

        checkpoint = 2
        self.dataset.getCheckpoint = MagicMock(return_value = checkpoint)

        control.open(loader)
        control.onAfterActivate()

        self.assertEqual(
            self.navigator.position,
            checkpoint
        )

    def test_open_valid_navigator_changesMade_False_with_checkpoints_user_no(self):

        self.settings.useCheckpoints = True

        self.env.view.askUserForCheckPointRestore = MagicMock(return_value = QMessageBox.No)

        control = TaggingControl(self.env, self.settings)

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]))

        checkpoint = 2
        self.dataset.getCheckpoint = MagicMock(return_value = checkpoint)

        control.open(loader)
        control.onAfterActivate()

        self.assertEqual(
            self.navigator.position,
            0
        )

    def test_open_timeline_intial_call(self):

        control = TaggingControl(self.env, self.settings)

        self.env.active = True

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]))

        control.open(loader)
        control.onAfterActivate()

        timeline = control.timeline

        timeline.plot.assert_called_with(
            [1/self.samplingRate, 2/self.samplingRate, 3/self.samplingRate],
            1/self.samplingRate,
            (0.0, 1.1)
        )

    def test_navigate_non_active(self):

        control = TaggingControl(self.env, self.settings)

        self.env.active = False

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]))

        control.open(loader)
        control.onAfterActivate()

        self.assertEqual(
            self.navigator.position,
            0
        )

        # Supposed random sequence of navigation
        control.onNextClick()
        control.onNextClick()
        control.onPreviousClick()
        control.onNextClick()
        control.onNextClick()
        control.onPreviousClick()

        self.assertEqual(
            self.navigator.position,
            0
        )

    def test_navigate_forward_active(self):

        control = TaggingControl(self.env, self.settings)

        self.env.active = True

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]))

        control.open(loader)
        control.onAfterActivate()

        self.assertEqual(
            self.navigator.position,
            0
        )

        control.onNextClick()
        control.onNextClick()

        self.assertEqual(
            self.navigator.position,
            2
        )

    def test_navigate_backward_active(self):

        control = TaggingControl(self.env, self.settings)

        self.env.active = True

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3,4,5]))

        control.open(loader)
        control.onAfterActivate()

        self.assertEqual(
            self.navigator.position,
            0
        )

        control.onPreviousClick()
        control.onPreviousClick()

        self.assertEqual(
            self.navigator.position,
            3
        )

    def test_onTaggingClick_non_active(self):

        control = TaggingControl(self.env, self.settings)

        self.env.active = False

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]))

        control.open(loader)
        control.onAfterActivate()

        self.assertEqual(
            self.navigator.selectionTag,
            0
        )

        control.onTaggingClick()

        self.assertEqual(
            self.navigator.selectionTag,
            0
        )

    def test_onTaggingClick_active_set(self):

        control = TaggingControl(self.env, self.settings)

        self.env.active = True

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]))

        control.open(loader)
        control.onAfterActivate()

        self.assertEqual(
            self.navigator.selectionTag,
            0
        )

        control.onTaggingClick()

        self.assertEqual(
            self.navigator.selectionTag,
            1
        )

    def test_onTaggingClick_active_reset(self):

        control = TaggingControl(self.env, self.settings)

        self.env.active = False

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]))

        control.open(loader)
        control.onAfterActivate()

        self.assertEqual(
            self.navigator.selectionTag,
            0
        )

        control.onTaggingClick()
        control.onTaggingClick()

        self.assertEqual(
            self.navigator.selectionTag,
            0
        )

    def test_navigate_timeline_supplied(self):

        control = TaggingControl(self.env, self.settings)

        self.env.active = True

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]))

        control.open(loader)
        control.onAfterActivate()

        control.onNextClick()

        timeline = control.timeline

        timeline.update.assert_called_with(
            2/self.samplingRate,
            (0.0, 1.2)
        )

    def test_notifyUserOfSwitch_no_checkpoints_no_changes(self):

        control = TaggingControl(self.env, self.settings)

        self.env.active = True

        self.env.view.askUserForSwitch = MagicMock()
        control.save = MagicMock()

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]))

        control.open(loader)
        control.onAfterActivate()

        control.notifyUserOfSwitch()

        self.env.view.askUserForSwitch.assert_not_called()
        control.save.assert_not_called()

    def test_notifyUserOfSwitch_no_checkpoints_changes_cancel(self):

        control = TaggingControl(self.env, self.settings)

        self.env.active = True

        self.env.view.askUserForSwitch = MagicMock(return_value = QMessageBox.Cancel)
        control.save = MagicMock()

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]), changesMade = True)

        control.open(loader)
        control.onAfterActivate()

        try:
            control.notifyUserOfSwitch()

            self.assertTrue(False)
        except UserCancel:
            self.assertTrue(True)

        self.env.view.askUserForSwitch.assert_called()
        control.save.assert_not_called()

    def test_notifyUserOfSwitch_no_checkpoints_changes_save(self):

        control = TaggingControl(self.env, self.settings)

        self.env.active = True

        self.env.view.askUserForSwitch = MagicMock(return_value = QMessageBox.Save)
        control.save = MagicMock()

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]), changesMade = True)

        control.open(loader)
        control.onAfterActivate()

        control.notifyUserOfSwitch()

        self.env.view.askUserForSwitch.assert_called()
        control.save.assert_called()

    def test_notifyUserOfSwitch_no_checkpoints_changes_answer_no(self):

        control = TaggingControl(self.env, self.settings)

        self.env.active = True

        self.env.view.askUserForSwitch = MagicMock(return_value = QMessageBox.Discard)
        control.save = MagicMock()

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]), changesMade = True)

        control.open(loader)
        control.onAfterActivate()

        control.notifyUserOfSwitch()

        self.env.view.askUserForSwitch.assert_called()
        control.save.assert_not_called()

    def test_notifyUserOfSwitch_with_checkpoints_answer_no_no_changes(self):

        control = TaggingControl(self.env, self.settings)

        self.settings.useCheckpoints = True
        self.env.active = True

        self.env.view.askUserForCheckPoint = MagicMock(return_value = QMessageBox.Yes)

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]))

        control.open(loader)
        control.onAfterActivate()

        control.dataset.setCheckpoint = MagicMock()

        control.onNextClick()
        control.notifyUserOfSwitch()

        self.env.view.askUserForCheckPoint.assert_called()
        control.dataset.setCheckpoint.assert_called_with(1)

    def test_notifyUserOfSwitch_with_checkpoints_answer_cancel(self):

        control = TaggingControl(self.env, self.settings)

        self.settings.useCheckpoints = True
        self.env.active = True

        self.env.view.askUserForCheckPoint = MagicMock(return_value = QMessageBox.Cancel)

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]))

        control.open(loader)
        control.onAfterActivate()

        control.dataset.setCheckpoint = MagicMock()

        control.onNextClick()

        try:
            control.notifyUserOfSwitch()

            self.assertFalse(True)
        except UserCancel:
            self.assertTrue(True)

        self.env.view.askUserForCheckPoint.assert_called()
        control.dataset.setCheckpoint.assert_not_called()
