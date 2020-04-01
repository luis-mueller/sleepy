
from sleepy.tagging.model import Navigator
from sleepy.tagging.model.event import EventTypeNotSupported, PointEvent, IntervalEvent
from sleepy.processing.algorithms import Massimi
from sleepy.processing.options import OptionView
from sleepy.processing.engine import Engine
from sleepy.processing import exceptions
from sleepy.processing.filters import BandPassFilter
from sleepy.tagging.model.event import UserPointEvent
from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QCheckBox, QComboBox
from PyQt5.QtWidgets import QStackedWidget
import numpy as np
import pdb

class FileProcessor:
    def __init__(self, applicationSettings):

        self.engine = Engine()

        self.algorithms = [Massimi(), Massimi()]

        self.filters = [BandPassFilter()]

        self.currentAlgorithm = None
        self.selectedFilter = None

        self.applicationSettings = applicationSettings

        self.labels = None
        self.dataSet = None

    @property
    def optionView(self):

        try:
            return self._optionView
        except AttributeError:

            self._optionView = OptionView(self)

            return self._optionView

    @property
    def options(self):
        return self.optionView.options

    def onAlgorithmSelection(self, index):
        """Given an index, selects either no algorithm or a corresponding algorithm
        in the algorithm list and returns its layout.
        """

        if index == 0:

            self.currentAlgorithm = None

        else:

            self.currentAlgorithm = self.algorithms[index - 1]

            try:
                return self.currentAlgorithm.options
            except AttributeError:
                pass

    def onFilterSelection(self, index):
        """Given an index, selects either no filter or a corresponding filter
        in the filter list and returns its layout.
        """

        if index == 0:

            self.selectedFilter = None

        else:

            self.selectedFilter = self.filters[index - 1]

            try:
                return self.selectedFilter.options
            except AttributeError:
                pass

    def run(self, algorithm, dataSet, filter = None):
        """Public API to execute an algorithm on a data-set. Is also used
        internally. The method calls its internal engine to provide a run-time
        environment for the algorithm.

        :param algorithm: Algorithm object that implements the method
        compute that receives a vector and a sampling rate and computes a list
        of either 2D-intervals or points.

        :param dataSet: Data-set object that provides the properties channelData,
        samplingRate and epochs.

        :param filter: Filter object, optional.
        """

        return self.engine.run(
            algorithm,
            dataSet,
            filter
        )

    def getLabels(self, dataSet):

        if self.currentAlgorithm:

            return self.run(self.currentAlgorithm, dataSet, self.selectedFilter)

        else:

            return dataSet.labels

    def computeLabels(self, dataSet):
        """Computes the labels based on the dataset and buffers dataset and
        computed labels. This needs to be called before computeNavigator.
        """

        self.dataSet = dataSet

        self.labels = self.getLabels(dataSet)

    def computeNavigator(self):
        """Computes a navigator instance from the buffered dataset and computed
        labels in computeLabels
        """

        self.checkComputeLabelsCalled()

        changesMade = self.updateLabels(self.labels)

        events = self.convertLabelsToEvents()

        self.navigator = Navigator(events, changesMade)

        self.addUserEventsToNavigator(self.navigator)

        return self.navigator

    def checkComputeLabelsCalled(self):

        if self.labels is None or self.dataSet is None:
            raise exceptions.ComputeLabelsNotCalled

    def updateLabels(self, labels):

        changesMade = self.resultDiffers(labels) or self.dataSet.changesMade

        self.dataSet.labels = labels

        if changesMade:
            self.dataSet.removeCheckpoint()

        return changesMade

    def showNumberOfLabels(self):

        self.checkComputeLabelsCalled()

        self.optionView.showNumberOfLabels(len(self.labels))

    def resultDiffers(self, result):

        if result.shape == self.dataSet.labels.shape:

            return not (result.tolist() == self.dataSet.labels.tolist())

        return True

    def convertLabelsToEvents(self):

        events = []

        for labelIndex in range(self.dataSet.numberOfLabels):

            dataSource = self.dataSet.getDataSourceFor(labelIndex)

            tag = self.dataSet.tags[labelIndex]

            event = self.deriveEvent(labelIndex, dataSource)

            if tag > 0:
                event.switchTag()

            events.append(event)

        return events

    def deriveEvent(self, labelIndex, dataSource):

        label = self.dataSet.labels[labelIndex]

        # Currently unclear, how to solve this other than by checking shapes
        if isinstance(label, np.int32) or isinstance(label, np.int64):

            return PointEvent(label, dataSource, self.applicationSettings)

        elif label.shape == (2,):

            return IntervalEvent(*label, dataSource, self.applicationSettings)

        else:

            raise EventTypeNotSupported

    def addUserEventsToNavigator(self, navigator):
        """Add the stored user labels as events to the navigator.
        """

        for userLabel in self.dataSet.userLabels:

            userLabel = userLabel.squeeze().tolist()

            dataSource = self.dataSet.getDataSourceForLabel(userLabel)

            userEvent = UserPointEvent(userLabel, dataSource, self.applicationSettings)

            navigator.addCreatedUserEvent(userEvent)

            # User events are stored in dataset
            navigator.onSave()
