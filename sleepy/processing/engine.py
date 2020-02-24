
import numpy as np
from scipy.signal import find_peaks
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QDoubleSpinBox, QLabel, QHBoxLayout, QWidget
from PyQt5.QtGui import QDoubleValidator
from sleepy.processing.constants import MU
from sleepy.processing.filters import BandPassFilter
import pdb

class Engine:

    def __init__(self):

        self.builder = Builder()

        self.bandPassFilter = BandPassFilter()

    def buffer(self, algorithm, dataSet):

        self.algorithm = algorithm
        self.dataSet = dataSet

    def run(self, algorithm, dataSet):

        self.buffer(algorithm, dataSet)

        epochMaps = self.mapEpochs()

        epochResult = self.computeEpochs(epochMaps)

        return np.concatenate(epochResult).ravel().astype(np.int32)

    def mapEpochs(self):

        channelDataSize = len(self.dataSet.channelData)

        return map(lambda i: self.computeEpoch(i), range(channelDataSize))

    def computeEpochs(self, epochMaps):

        result = list(epochMaps)

        return np.array(result)

    def computeEpoch(self, index):

        data = self.dataSet.channelData[index]

        filteredData = self.bandPassFilter.filter(
            data,
            self.dataSet.samplingRate
        )

        epochStart = self.dataSet.epochs[index][0]

        return self.computeEpochAbsolute(filteredData, epochStart)

    def computeEpochAbsolute(self, data, epochStart):

        relativeResult = self.algorithm.compute(
            data,
            self.dataSet.samplingRate
        )

        absoluteResult = relativeResult + epochStart

        return absoluteResult
