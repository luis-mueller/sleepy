
import numpy as np
from scipy.signal import find_peaks
from sleepy.processing.valley import Valley

class Signal:

    def __init__(self, data, samplingRate):

        self.data = data
        self.samplingRate = samplingRate

        self.negativePeak = 40

    @property
    def zeroCrossings(self):

        try:
            return self._zeroCrossings
        except AttributeError:

            signs = np.sign(self.data)

            # Treat 0 as a positive sign
            binarySigns = np.where(signs == 0, 1, signs)

            # https://stackoverflow.com/questions/3843017/efficiently-detect-sign-changes-in-python
            self._zeroCrossings = np.where(np.diff(binarySigns))[0]

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
            self._negativePeaks, _ = find_peaks(-self.data, height = self.negativePeak)

            return self._negativePeaks

    def findValley(self, peak):

        nCrossing = self.findClosestNCrossing(peak)
        pCrossing = self.findClosestPCrossing(peak)

        nextPeak = list(filter(lambda p: p > pCrossing, self.positivePeaks))[0]

        return Valley(
            nCrossing,
            pCrossing,
            peak,
            nextPeak,
            self.data
        )

    def findClosestPCrossing(self, peak):

        cross = self.zeroCrossings

        pCrossing = list(filter(lambda c: c > peak, cross))[0]

        return pCrossing

    def findClosestNCrossing(self, peak):

        cross = self.zeroCrossings

        nCrossing = list(filter(lambda c: c < peak, cross))[-1]

        return nCrossing
