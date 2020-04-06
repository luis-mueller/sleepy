
import numpy as np
from functools import partial
from sleepy.processing.signal import Signal

class Engine:

    def run(algorithm, filter, dataset):
        """Executes an algorithm and a filter on a dataset. The execution follows
        a pipeline concept. The algorithm first gets called with the entire data
        and produces a set of parameters. Then every epoch in every channel is
        processed by the algorithm isolatedly and is additionally supplied the
        parameters pre-processed. Afterwards the result of each call is
        aggregated and filtered by a post-processing step.

        :param algorithm: Algorithm object that implements a subset of the
        methods extract, compute and filter. Extracts receives the entire data
        and returns a set of parameters. These parameters are plugged into
        compute which is called for each signal in every epoch and every channel.
        The results are aggregated and filtered in the filter method.

        :param filter: Filter object, optional. Must support a call via the
        filter-method.

        :param dataset: Data-set object that provides the properties data,
        samplingRate and epochs.

        :returns: A :class:`np.array` with an entry for every channel. Each
        entry is another :class:`np.array` containing all samples which were
        identified as events for this channel over all epochs.
        """


        Engine.__applyPreFilter(filter, dataset)

        computing = Engine.__getComputeMethod(algorithm, dataset.filteredData)

        computeStepResult = Engine.__computeStep(
            computing,
            dataset.filteredData,
            dataset.epochs,
            dataset.samplingRate
        )

        filterStepResult = algorithm.filter(computeStepResult, dataset.filteredData)

        return Engine.__format(filterStepResult)

    def __format(labels):
        """Formats labels from channel by epoch by label to channel by concatenated
        epoch labels.
        """

        return np.array([
            np.concatenate(x).astype(np.int32)
                for x in labels
        ])


    def __applyPreFilter(filter, dataset):
        """Applies a given filter to a given dataset and hands the result to
        the dataset in the appropriate format (channel by epoch).
        """

        epochs = range(len(dataset.data))

        filteredData = Engine.__preFilter(filter, dataset, epochs)

        dataset.filteredData = Engine.__transposeFirstTwoDimensions(filteredData)

    def __preFilter(filter, dataset, epochs):
        """Filters the entire dataset for the extract step.
        """

        filteredData = [
            [
                filter.filter(dataset.data[epoch][channel], dataset.samplingRate)
                    for channel in range(len(dataset.data[epoch]))
            ]
                for epoch in epochs
        ]

        return np.array(filteredData)

    def __getComputeMethod(algorithm, data):
        """Executes the extract step and attaches the parameters to the compute
        method of the algorithm.
        """

        extractParameters = algorithm.extract(data)

        if extractParameters is not None:

            return partial(algorithm.compute, *extractParameters)

        else:

            return algorithm.compute

    def __computeStep(computing, data, epochIntervals, samplingRate):
        """Performs the compute step for each signal in the filtered dataset.
        """

        compute = partial(Engine.__compute, computing, samplingRate)

        channels = range(len(data))

        computeStepResult = [
            [
                compute(data[channel][epoch], epochIntervals[epoch][0])
                    for epoch in range(len(data[channel]))
            ]
            for channel in channels
        ]

        return np.array(computeStepResult)

    def __compute(computing, samplingRate, data, epochStart):
        """Computes the result of a signal applied to a given algorithm.
        """

        signal = Signal(data, samplingRate)

        labels = computing(signal)

        return ( labels + epochStart ).astype(np.int32).tolist()

    def __transposeFirstTwoDimensions(array):
        """Transposes the first two dimensions of a given array
        """

        lengthOfShape = len(array.shape)

        flippedShape = list(range(lengthOfShape))

        flippedShape[0] = 1
        flippedShape[1] = 0

        return array.transpose(tuple(flippedShape))
