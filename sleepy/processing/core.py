
from sleepy.tagging.model import Navigator
from sleepy.tagging.model.event import EventTypeNotSupported, PointEvent, IntervalEvent
from sleepy.processing.algorithms import Massimi
from sleepy.processing.options import OptionView
from sleepy.processing.engine import Engine
from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QCheckBox, QComboBox
from PyQt5.QtWidgets import QStackedWidget
import numpy as np
import pdb

class FileProcessor:
    def __init__(self, applicationSettings):

        self.engine = Engine()

        self.algorithms = [Massimi(self.engine), Massimi(self.engine)]

        self.currentAlgorithm = self.algorithms[0]

        self.applicationSettings = applicationSettings

    @property
    def options(self):

        try:
            return self._optionView.options
        except AttributeError:

            self._optionView = OptionView(self)

            return self._optionView.options

    def onAlgorithmSelection(self, index):

        self.currentAlgorithm = self.algorithms[index]

        return self.currentAlgorithm.options

    def run(self, algorithm, dataSet):
        """Public API to execute an algorithm on a data-set. Is also used
        internally. The method calls its internal engine to provide a run-time
        environment for the algorithm.

        :param algorithm: Algorithm object that implements the method
        compute that receives a vector and a sampling rate and computes a list
        of either 2D-intervals or points.

        :param dataSet: Data-set object that provides the properties channelData,
        samplingRate and epochs.
        """

        return self.engine.run(
            algorithm,
            dataSet
        )

    def computeNavigator(self, dataSet):

        self.dataSet = dataSet

        labels = self.run(self.currentAlgorithm, dataSet)

        changesMade = self.updateLabels(labels)

        events = self.convertLabelsToEvents()

        self.navigator = Navigator(events, changesMade)

        return self.navigator

    def updateLabels(self, labels):

        changesMade = self.resultDiffers(labels)

        self.dataSet.labels = labels

        return changesMade

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
        if isinstance(label, np.int32):

            return PointEvent(label, dataSource, self.applicationSettings)

        elif label.shape == (2,):

            return IntervalEvent(*label, dataSource, self.applicationSettings)

        else:

            raise EventTypeNotSupported
