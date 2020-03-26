
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
        env.view.onTagging = MagicMock()
        env.active = False
        env.app = self.app
        return env

    def getNewApp(self):

        app = MagicMock()
        app.name = 'TestApplication'
        app.applicationSettings = MagicMock()
        app.applicationSettings.showIndex = False
        app.applicationSettings.useCheckpoints = False
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
            np.arange(*self.interval,1), self.interval, samplingRate = self.samplingRate
        )

        return list(
            map(lambda i: self.customPointSample(i), points)
        )

    def customPointSample(self, point):
        return PointEvent(point, self.dataSource, self.app.applicationSettings)

    def setUp(self):

        self.app = self.getNewApp()

        self.env = self.getEnvironment()

    def test_open_no_navigator(self):

        control = TaggingControl(self.env)

        loader = self.getFileLoader('test/path')

        try:
            control.open(loader)
        except UserCancel:
            self.assertTrue(True)
            return

        self.assertTrue(False)

    def test_open_empty_navigator(self):

        control = TaggingControl(self.env)

        loader = self.getFileLoader('test/path', self.getEvents([]), changesMade = False)

        try:
            control.open(loader)
        except UserCancel:
            self.assertTrue(True)
            return

        self.assertTrue(False)

    def test_open_valid_navigator_changesMade_False_no_checkpoints_no_index_with_filename(self):

        self.app.applicationSettings.useCheckpoints = False
        self.app.applicationSettings.showIndex = False

        control = TaggingControl(self.env)

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]), changesMade = False)

        self.navigator.switchSelectionTag()

        try:
            control.open(loader)
        except UserCancel:
            self.assertTrue(False)

        self.app.setWindowTitle.assert_called_with('TestApplication - TestFile*')

        self.env.view.onTagging.assert_called_with(True)

    def test_open_valid_navigator_changesMade_False_no_checkpoints_with_index_with_filename(self):

        self.app.applicationSettings.useCheckpoints = False
        self.app.applicationSettings.showIndex = True

        control = TaggingControl(self.env)

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]), changesMade = False)

        self.navigator.switchSelectionTag()

        try:
            control.open(loader)
        except UserCancel:
            self.assertTrue(False)

        self.app.setWindowTitle.assert_called_with('TestApplication - TestFile* - Sample: 1/3')

        self.env.view.onTagging.assert_called_with(True)

    def test_open_valid_navigator_changesMade_False_with_checkpoints_user_yes(self):

        self.app.applicationSettings.useCheckpoints = True

        self.env.view.askUserForCheckPointRestore = MagicMock(return_value = QMessageBox.Yes)

        control = TaggingControl(self.env)

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]))

        checkpoint = 2
        self.dataset.getCheckpoint = MagicMock(return_value = checkpoint)

        try:
            control.open(loader)
        except UserCancel:
            self.assertTrue(False)

        self.assertEqual(
            self.navigator.position,
            checkpoint
        )

    def test_open_valid_navigator_changesMade_False_with_checkpoints_user_no(self):

        self.app.applicationSettings.useCheckpoints = True

        self.env.view.askUserForCheckPointRestore = MagicMock(return_value = QMessageBox.No)

        control = TaggingControl(self.env)

        loader = self.getFileLoader('test/TestFile', self.getEvents([1,2,3]))

        checkpoint = 2
        self.dataset.getCheckpoint = MagicMock(return_value = checkpoint)

        try:
            control.open(loader)
        except UserCancel:
            self.assertTrue(False)

        self.assertEqual(
            self.navigator.position,
            0
        )
