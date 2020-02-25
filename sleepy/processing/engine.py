
import numpy as np
from scipy.signal import find_peaks
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QDoubleSpinBox, QLabel, QHBoxLayout, QWidget
from PyQt5.QtGui import QDoubleValidator
from sleepy.processing.constants import MU
from sleepy.processing.filters import BandPassFilter
from sleepy.gui.builder import Builder
from sleepy.processing.signal import Signal
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

        epochResult = self.computeResult()

        return np.concatenate(epochResult).ravel().astype(np.int32)

    def computeResult(self):

        channelDataSize = len(self.dataSet.channelData)

        maps = map(lambda i: self.computeEpoch(i), range(channelDataSize))

        return np.array(list(maps))

    def computeEpoch(self, index):

        data = self.dataSet.channelData[index]

        filteredData = self.applyFilter(data)

        epochStart = self.dataSet.epochs[index][0]

        return self.computeEpochAbsolute(filteredData, epochStart)

    def applyFilter(self, data):

        fs = self.dataSet.samplingRate

        return self.bandPassFilter.filter(data, fs)

    def computeEpochAbsolute(self, data, epochStart):

        signal = Signal(data, self.dataSet.samplingRate)

        relativeResult = self.algorithm.compute(signal)

        absoluteResult = relativeResult + epochStart

        return absoluteResult
