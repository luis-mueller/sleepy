
from sleepy.processing.algorithms.core import Algorithm

class Massimi(Algorithm):

    def __init__(self):

        self.setAttributesRelative('processing/algorithms/massimi/massimi.json')

    def compute(self, signal):

        def isEvent(peak):

            valley = signal.findValley(peak)

            if valley:
                if valley.negativeToPositivePeak > self.negativeToPositivePeak:
                    if  valley.separation >= self.separation * signal.samplingRate:
                        return True

            return False

        negativePeaks = signal.getNegativePeaks(self.negativePeak)

        return list(filter(isEvent, negativePeaks))
