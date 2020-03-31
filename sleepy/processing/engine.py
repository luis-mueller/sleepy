
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

        formattedResult = self.formatResult(epochResult)

        return formattedResult

    def formatResult(self, result):

        concatResult = np.concatenate(result)

        flatResult = self.flattenFirstDimension(concatResult)

        return flatResult.astype(np.int32)

    def flattenFirstDimension(self, result):

        if result.shape[0] > 1:
            return result.reshape(-1, result.shape[-1]).squeeze()
        else:
            return result

    def computeResult(self, filter):

        channelDataSize = len(self.dataSet.channelData)

        maps = map(lambda i: self.computeEpoch(i, filter), range(channelDataSize))

        return np.array(list(maps))

    def computeEpoch(self, index, filter):

        data = self.dataSet.channelData[index]

        filteredData = self.applyFilter(filter, data)

        self.dataSet.setFilteredData(index, filteredData)

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

        return absoluteResult
