
from sleepy.processing.algorithms.options import MassimiOptionView
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
    def zeroCrossings(self):

        try:
            return self._zeroCrossings
        except AttributeError:
            self._zeroCrossings = self.computeZeroCrossings()

            return self._zeroCrossings

    @property
    def positivePeaks(self):

        try:
            return self._positivePeaks
        except AttributeError:
            self._positivePeaks, _ = find_peaks(self.data, height = 0)

            return self._positivePeaks

    @property
    def negativePeaks(self):

        try:
            return self._negativePeaks
        except AttributeError:
            self._negativePeaks, _ = find_peaks(-self.data, height = self.optionView.negativePeak.value)

            return self._negativePeaks

    def compute(self, data, sampleRate):

        self.data = data
        self.sampleRate = sampleRate

        return list(
            filter(
                lambda peak: self.isEvent(peak),
                self.negativePeaks
            )
        )

    def isEvent(self, peak):

        try:

            pCrossing, nCrossing, nextPeak = self.computeLocalIndices(peak)
        except IndexError:

            return False

        separationValid = (pCrossing - nCrossing) >= self.optionView.separation.value * self.sampleRate

        if self.data[nextPeak] - self.data[peak] > 70 and separationValid:
            return True

        return False

    def computeLocalIndices(self, peak):

        pCrossing, nCrossing = self.getSurroundingCrossings(peak)

        nextPeak = list(filter(lambda p: p > pCrossing, self.positivePeaks))[0]

        return pCrossing, nCrossing, nextPeak


    def getSurroundingCrossings(self, peak):

        cross = self.zeroCrossings

        pCrossing = list(filter(lambda c: c > peak, cross))[0]

        nCrossing = list(filter(lambda c: c < peak, cross))[-1]

        return pCrossing, nCrossing

    def computeZeroCrossings(self):

        signs = np.sign(self.data)

        # Treat 0 as a positive sign
        binarySigns = np.where(signs == 0, 1, signs)

        # https://stackoverflow.com/questions/3843017/efficiently-detect-sign-changes-in-python
        return np.where(np.diff(binarySigns))[0]
