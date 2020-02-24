
from sleepy.tagging.model import Navigator
from sleepy.tagging.model.event import EventTypeNotSupported, PointEvent, IntervalEvent
from eegplot.algorithms import Massimi
from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QCheckBox, QComboBox
from PyQt5.QtWidgets import QStackedWidget
from sleepy.processing.options import OptionView
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

    def run(self):

        return self.engine.run(
            self.currentAlgorithm,
            self.self.dataSet
        )

    def computeNavigator(self, dataSet):

        self.dataSet = dataSet

        labels = self.run()

        changesMade = self.updateLabels(labels)

        samples = self.convertLabelsToEvents()

        self.navigator = Navigator(samples, changesMade)

        return self.navigator

    def updateLabels(self, labels):

        changesMade = self.resultDiffers(labels)

        self.dataSet.labels = result

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
