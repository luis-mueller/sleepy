
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLineEdit, QDialogButtonBox, QDialog, QMessageBox
from PyQt5.QtWidgets import QHBoxLayout, QGroupBox, QWidget, QComboBox, QStackedWidget, QLabel

class PreprocessingView(QDialog):

    def __init__(self, app, control):
        super().__init__(app)

        self.control = control

        self.setWindowTitle("Preprocessing")
        self.setMinimumWidth(600)

        self.initializeLayout()

    def initializeLayout(self):

        self.layout = QVBoxLayout(self)

        self.initializePathSelector()
        self.initializeOptions()
        self.initializeButtonBox()

    def initializePathSelector(self):

        self.pathSelectorBox = QGroupBox('Dataset')

        self.pathSelectorLayout = QHBoxLayout()

        self.pathEdit = QLineEdit(self.control.path)
        self.pathSelectorLayout.addWidget(self.pathEdit)

        self.changePathButton = QPushButton('...')
        self.changePathButton.clicked.connect(self.control.selectPath)

        self.pathSelectorLayout.addWidget(self.changePathButton)

        self.pathSelectorBox.setLayout(self.pathSelectorLayout)

        self.layout.addWidget(self.pathSelectorBox)

    # https://doc.qt.io/archives/qq/qq19-buttons.html#
    def initializeButtonBox(self):

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton("Load", QDialogButtonBox.AcceptRole)
        self.buttonBox.accepted.connect(self.control.load)

        self.computeButton = QPushButton("Compute")
        self.buttonBox.addButton(self.computeButton, QDialogButtonBox.ActionRole)
        self.computeButton.clicked.connect(self.control.compute)

        self.buttonBox.addButton("Cancel", QDialogButtonBox.RejectRole)
        self.buttonBox.rejected.connect(self.reject)

        self.layout.addWidget(self.buttonBox)

    def initializeOptions(self):

        self.optionsWidget = QWidget()

        self.optionsLayout = QVBoxLayout()

        self.optionsLayout.addWidget(self.filterOptions())

        self.optionsLayout.addWidget(self.algorithmOptions())

        self.optionsLayout.addWidget(self.computationStatus)

        self.optionsWidget.setLayout(self.optionsLayout)

        self.layout.addWidget(self.optionsWidget)

    @property
    def computationStatus(self):

        try:
            return self._computationStatus
        except AttributeError:

            self._computationStatus = QLabel("")
            return self._computationStatus

    def filterOptions(self):

        self.filterSelection = QComboBox()

        self.filterSelection.addItem("No filter")

        list(map(
            lambda f: self.filterSelection.addItem(f.name),
            self.control.filters[1:]
        ))

        self.filterBox = QGroupBox('Filters')

        layout = QVBoxLayout()

        layout.addWidget(self.filterSelection)

        self.filterParameters = QStackedWidget()

        self.noFilterParameters = QWidget()
        self.filterParameters.addWidget(self.noFilterParameters)

        list(map(
            lambda f: self.filterParameters.addWidget(f.options),
            self.control.filters[1:]
        ))

        layout.addWidget(self.filterParameters)

        self.filterBox.setLayout(layout)

        self.filterSelection.currentIndexChanged.connect(self.control.onFilterChange)

        return self.filterBox

    def algorithmOptions(self):

        self.algorithmSelection = QComboBox()

        self.algorithmSelection.addItem("No processing")

        list(map(
            lambda a: self.algorithmSelection.addItem(a.name),
            self.control.algorithms[1:]
        ))

        self.algorithmBox = QGroupBox('Algorithms')

        layout = QVBoxLayout()

        layout.addWidget(self.algorithmSelection)

        self.algorithmParameters = QStackedWidget()

        self.noParameters = QWidget()
        self.algorithmParameters.addWidget(self.noParameters)

        list(map(
            lambda a: self.algorithmParameters.addWidget(a.options),
            self.control.algorithms[1:]
        ))

        layout.addWidget(self.algorithmParameters)

        self.algorithmBox.setLayout(layout)

        self.algorithmSelection.currentIndexChanged.connect(self.control.onAlgorithmChange)

        return self.algorithmBox

    def setPath(self, path):
        """Abstraction around setting the text of the pathEdit widget.
        """

        self.pathEdit.setText(path)

    def setNoAlgorithmParameters(self):

        self.algorithmParameters.setCurrentWidget(self.noParameters)

    def setNoFilterParameters(self):

        self.filterParameters.setCurrentWidget(self.noFilterParameters)

    def setAlgorithmParameters(self, parameters):

        self.algorithmParameters.setCurrentWidget(parameters)

    def setFilterParameters(self, parameters):

        self.filterParameters.setCurrentWidget(parameters)

    def showNumberOfEvents(self, numberOfEvents, numberOfChannels):
        """Abstraction around setting the text to the computationStatus
        widget, formatting the number of events and the number of channels
        supplied.
        """

        self.computationStatus.setText(
            "{} events found in {} channels.".format(
                numberOfEvents,
                numberOfChannels
            )
        )

        QApplication.processEvents()

    def showFileNotSupported(self, extension):
        """Show a pop-up window, notifying the user that the file type is not
        supported.
        """

        error = QMessageBox(self.window)
        error.setWindowTitle('Error')
        error.setIcon(QMessageBox.Critical)
        error.setText(
            'Files of type .{} are not supported.'.format(extension.lower())
        )
        error.exec_()
