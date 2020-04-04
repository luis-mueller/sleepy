
import numpy as np
from scipy.signal import find_peaks
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QDoubleSpinBox, QLabel, QHBoxLayout, QWidget
from PyQt5.QtGui import QDoubleValidator
from sleepy.processing.constants import MU
from sleepy.gui.builder import Builder
from sleepy.processing.signal import Signal
import pdb

class Engine:

    def __init__(self):

        self.builder = Builder()

    def buffer(self, algorithm, dataSet):

        self.algorithm = algorithm
        self.dataSet = dataSet

    def run(self, algorithm, dataSet, filter):

        self.buffer(algorithm, dataSet)

        epochResult = self.computeResult(filter)

        return np.array([ np.concatenate(x).astype(np.int32) for x in epochResult.transpose() ])

    def computeResult(self, filter):

        numberOfEpochs = len(self.dataSet.data)

        maps = map(lambda i: self.computeEpoch(i, filter), range(numberOfEpochs))

        return np.array(list(maps))

    def computeEpoch(self, index, filter):

        numberOfChannels = len(self.dataSet.data[index])

        return [ self.computeChannelEpoch(index, channel, filter) for channel in range(len(self.dataSet.data[index]))]

    def computeChannelEpoch(self, index, channel, filter):

        data = self.dataSet.data[index][channel]

        filteredData = self.applyFilter(filter, data)

        self.dataSet.setFilteredData(index, channel, filteredData)

        epochStart = self.dataSet.epochs[index][0]

        return self.computeEpochAbsolute(filteredData, epochStart)

    def applyFilter(self, filter, data):

        if filter:

            fs = self.dataSet.samplingRate

            return filter.filter(data, fs)

        else:

            return data

    def computeEpochAbsolute(self, data, epochStart):

        signal = Signal(data, self.dataSet.samplingRate)

        relativeResult = self.algorithm.compute(signal)

        absoluteResult = relativeResult + epochStart

        return absoluteResult.astype(np.int32).tolist()
