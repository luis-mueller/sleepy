
from sleepy.io.preproc.supported import SUPPORTED_FILTERS, SUPPORTED_ALGORITHMS, SUPPORTED_DATASETS
from sleepy.io.preproc.view import PreprocessingView
from sleepy.gui.exceptions import UserCancel
from sleepy.tagging.model import Navigator
from PyQt5.QtWidgets import QFileDialog

class Preprocessing:
    """Application starting a preprocessing screen from which the user can
    select a dataset, a filter and a algorithm. Uses the :class:`Engine` class
    to produce a list of navigators and returns them to the caller.
    """

    def __init__(self, parent):
        """Configures the application by setting a default path, creating the
        :class:`QDialog` and rendering filters and algorithms.

        :param parent: The parent application.

        :raises UserCancel: The user cancelled the initial path selection and thus,
        wants to abort the preprocessing.
        """

        self.parent = parent

        # Initially do not catch the UserCancel to signal the initial cancel
        # to the parent
        self.path = self.selectPath()
        self.algorithms = self.renderAlgorithms()
        self.filters = self.renderFilters()
        self.view = PreprocessingView(parent, self)

    def run(self):
        """Runs the preprocessing by starting the view's window and returns the
        computed navigators in Preprocessing.load. If the navigators were not
        computed then the window must have been rejected. This is propagated
        forward by raising UserCancel.

        :returns: A list of navigators, one for each channel.

        :raises UserCancel: Window was rejected by the user.
        """

        self.view.exec_()

        try:
            return self.navigators
        except AttributeError:
            raise UserCancel

    def compute(self):
        """Compute events with the given settings but do not create navigators
        yet. The result of the computation is displayed to the user via the view.
        """

        events = self.__computeEvents()

        numberOfEvents = sum([ len(eventList) for eventList in events ])
        numberOfChannels = len(events)

        self.view.showNumberOfEvents(numberOfEvents, numberOfChannels)

    def load(self):
        """Load navigators from events computed with the given settings. Calls
        the accept method of the view to accept the dialog and return to the
        calling method (Preprocessing.run).
        """

        events = self.__computeEvents()

        self.navigators = [ Navigator(eventList, changesMade) for eventList in events ]

        self.view.accept()

    def onAlgorithmChange(self, index):
        """Called on change of algorithm selection. Sets the algorithm with
        the corresponding index and tries to set the algorithm's parameters
        to the view.

        :param index: Index of the algorithm to select.
        """

        self.algorithm = self.algorithms[index]

        try:

            self.view.setAlgorithmParameters(self.algorithm.options)

        except AttributeError:

            self.view.setNoAlgorithmParameters()

    def onFilterChange(self, index):
        """Called on change of filter selection. Sets the filter with
        the corresponding index and tries to set the filter's parameters
        to the view.

        :param index: Index of the filter to select.
        """

        self.filter = self.filters[index]

        try:

            self.view.setFilterParameters(self.filter.options)

        except AttributeError:

            self.view.setNoFilterParameters()

    def __computeEvents(self):
        """Computes the events given algorithm and filter. The dataset is also
        loaded at this step based on the path that is currently selected.
        The settings are inherited from the parent. Note that in this case 'parent'
        does not refer to a super-class but to the application calling this
        application.
        """

        dataset = self.__loadDataset()

        try:

            if self.algorithm and self.filter:

                settings = self.parent.settings

                return Engine.run(self.algorithm, self.filter, dataset, settings)

        except AttributeError:
            return dataset.labels

    def __loadDataset(self):
        """Loads a :class:`Dataset` instance based on the path currently selected.
        Parses the path to find the file extension and finds the appropriate
        instance via the supported file. The resulting class must implement a
        static load method that returns a raw data object with which an instance
        of said class can be constructed.
        """

        extension = self.__getFileExtension()

        DatasetClass = SUPPORTED_DATASETS[extension]

        raw = DatasetClass.load()

        return DatasetClass(raw)

    def __selectPath(self):
        """Tries to load the path to a new dataset. If no path was selected
        raise a UserCancel.
        """

        path, _ = QFileDialog.getOpenFileName(self.parent, 'Open File')
        if path != '':

            self.view.setPath(path)

            return path
        else:
            raise UserCancel

    def __renderFilters(self):
        """Renders the list of supported filters, drawn from the supported
        file. At the top of the list is a NoneType, indicating that no
        filter was selected.
        """

        return [None] + [ f().render() for f in SUPPORTED_FILTERS ]

    def __renderAlgorithms(self):
        """Renders the list of supported algorithms, drawn from the supported
        file. At the top of the list is a NoneType, indicating that no
        algorithm was selected.
        """

        return [None] + [ a().render() for a in SUPPORTED_ALGORITHMS ]

    def __getFileExtension(self):
        """Returns the file extension of the current path in upper-case letters.
        """

        return self.path.rsplit('.', 1)[-1].upper()
