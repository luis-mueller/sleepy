
from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QCheckBox, QComboBox, QLabel
from PyQt5.QtWidgets import QStackedWidget, QWidget, QApplication

class OptionView:

    def __init__(self, control):

        self.control = control

    @property
    def options(self):

        try:
            return self._optionsWidget
        except AttributeError:
            pass

        self._optionsWidget = QWidget()

        self._optionsLayout = QVBoxLayout()

        self._optionsLayout.addWidget(self.filterOptions)

        self._optionsLayout.addWidget(self.algorithmOptions)

        self._optionsLayout.addWidget(self.computationStatus)

        self._optionsWidget.setLayout(self._optionsLayout)

        return self._optionsWidget

    @property
    def computationStatus(self):

        try:
            return self._computationStatus
        except AttributeError:

            self._computationStatus = QLabel("")
            return self._computationStatus

    @property
    def filterOptions(self):

        self.filterSelection = QComboBox()

        self.filterSelection.addItem("No filter")

        list(map(
            lambda f: self.filterSelection.addItem(f.name),
            self.control.filters
        ))

        self.filterBox = QGroupBox('Filters')

        layout = QVBoxLayout()

        layout.addWidget(self.filterSelection)

        self.filterParameters = QStackedWidget()

        self.noFilterParameters = QWidget()
        self.filterParameters.addWidget(self.noFilterParameters)

        list(map(
            lambda f: self.filterParameters.addWidget(f.options),
            self.control.filters
        ))

        layout.addWidget(self.filterParameters)

        self.filterBox.setLayout(layout)

        self.filterSelection.currentIndexChanged.connect(self.onFilterChange)

        return self.filterBox

    @property
    def algorithmOptions(self):

        self.algorithmSelection = QComboBox()

        self.algorithmSelection.addItem("No processing")

        list(map(
            lambda a: self.algorithmSelection.addItem(a.name),
            self.control.algorithms
        ))

        self.algorithmBox = QGroupBox('Algorithms')

        layout = QVBoxLayout()

        layout.addWidget(self.algorithmSelection)

        self.algorithmParameters = QStackedWidget()

        self.noParameters = QWidget()
        self.algorithmParameters.addWidget(self.noParameters)

        list(map(
            lambda a: self.algorithmParameters.addWidget(a.options),
            self.control.algorithms
        ))

        layout.addWidget(self.algorithmParameters)

        self.algorithmBox.setLayout(layout)

        self.algorithmSelection.currentIndexChanged.connect(self.onAlgorithmChange)

        return self.algorithmBox

    def newWidgetFromLayout(self, layout):

        widget = QWidget()

        widget.setLayout(layout)

        return widget

    def onAlgorithmChange(self, index):

        options = self.control.onAlgorithmSelection(index)

        if not options:

            self.algorithmParameters.setCurrentWidget(self.noParameters)

        else:

            self.algorithmParameters.setCurrentWidget(options)

    def onFilterChange(self, index):

        options = self.control.onFilterSelection(index)

        if not options:

            self.filterParameters.setCurrentWidget(self.noFilterParameters)

        else:

            self.filterParameters.setCurrentWidget(options)

    def showNumberOfLabels(self, numberOfLabels):

        self.computationStatus.setText("{} labels found.".format(numberOfLabels))

        QApplication.processEvents()
