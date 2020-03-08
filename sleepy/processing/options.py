
from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QCheckBox, QComboBox
from PyQt5.QtWidgets import QStackedWidget, QWidget

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

        self._optionsLayout.addLayout(self.filterOptions)

        self._optionsLayout.addWidget(self.algorithmOptions)

        self._optionsWidget.setLayout(self._optionsLayout)

        return self._optionsWidget

    @property
    def filterOptions(self):
        return self.control.engine.bandPassFilter.layout

    @property
    def algorithmOptions(self):

        self.algorithmSelection = QComboBox()

        self.algorithmSelection.addItem("No processing")

        list(map(
            lambda a: self.algorithmSelection.addItem(a.name),
            self.control.algorithms
        ))

        self.algorithmBox = QGroupBox('Algorithms')
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.algorithmSelection)

        self.algorithmParameters = QStackedWidget()

        self.noParameters = QWidget()
        self.algorithmParameters.addWidget(self.noParameters)

        list(map(
            lambda a: self.algorithmParameters.addWidget(a.options),
            self.control.algorithms
        ))

        self.layout.addWidget(self.algorithmParameters)

        self.algorithmBox.setLayout(self.layout)

        self.algorithmSelection.currentIndexChanged.connect(self.onAlgorithmChange)

        return self.algorithmBox

    def onAlgorithmChange(self, index):

        options = self.control.onAlgorithmSelection(index)

        if not options:

            self.algorithmParameters.setCurrentWidget(self.noParameters)

        else:

            self.algorithmParameters.setCurrentWidget(options)
