
from sleepy.processing.algorithms.massimi.options import MassimiOptionView
import numpy as np
from scipy.signal import find_peaks
import pdb

class Massimi:

    def __init__(self, engine):

        self.engine = engine

        self.optionView = MassimiOptionView()

    @property
    def name(self):
        return 'Massimi (2004)'

    @property
    def options(self):
        return self.optionView.options

    @property
    def negativeToPositivePeak(self):
        return self.optionView.negativeToPositivePeak.value

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

        signal.negativePeak = self.optionView.negativePeak.value

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

        return self.optionView.separation.value * samplingRate
