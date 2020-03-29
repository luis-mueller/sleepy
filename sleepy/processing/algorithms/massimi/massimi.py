
from sleepy.gui.builder import Builder
import numpy as np
from scipy.signal import find_peaks
from PyQt5.QtWidgets import QWidget
from sleepy import SLEEPY_ROOT_DIR
import pdb

class Massimi:

    def __init__(self, engine):

        self.engine = engine

        Builder.setAttributesFromJSON(SLEEPY_ROOT_DIR + '/processing/algorithms/massimi/massimi.json', self)

    @property
    def name(self):
        return 'Massimi (2004)'

    @property
    def options(self):

        try:
            return self.widget
        except AttributeError:

            self.widget = QWidget()

            layout = Builder.build(SLEEPY_ROOT_DIR + '/processing/algorithms/massimi/massimi.json', self)

            self.widget.setLayout(layout)

            return self.widget

    def compute(self, signal):

        self.customizeSignal(signal)

        negativePeaks = self.signal.negativePeaks

        detectedEvents = list(
            filter(
                lambda peak: self.isEvent(peak),
                negativePeaks
            )
        )

        return detectedEvents

    def customizeSignal(self, signal):

        signal.negativePeak = self.negativePeak

        self.signal = signal

    def isEvent(self, peak):

        try:

            valley = self.signal.findValley(peak)
        except IndexError:
            return False

        threshold = self.convertSeparationThreshold(self.signal.samplingRate)

        if valley.negativeToPositivePeak > self.negativeToPositivePeak and valley.separation >= threshold:
            return True

        return False

    def convertSeparationThreshold(self, samplingRate):

        return self.separation * samplingRate
