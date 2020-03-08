
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLineEdit, QDialogButtonBox, QDialog
from PyQt5.QtWidgets import QHBoxLayout, QAction, QFileDialog, QGroupBox
from sleepy.io.gui.constants import WINDOW_TITLE, WINDOW_WIDTH

class FileLoaderView(QDialog):

    def __init__(self, app, control):
        super().__init__(app)

        self.control = control

        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumWidth(WINDOW_WIDTH)

        self.initializeLayout()

    @property
    def path(self):
        return self.control.path

    def initializeLayout(self):

        self.layout = QVBoxLayout(self)

        self.initializePathSelector()

        self.layout.addWidget(self.control.options)

        self.initializeButtonBox()

    def initializePathSelector(self):

        self.pathSelectorBox = QGroupBox('Path')

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
        self.buttonBox.accepted.connect(self.control.computeAndAccept)

        self.computeButton = QPushButton("Compute")
        self.buttonBox.addButton(self.computeButton, QDialogButtonBox.ActionRole)
        self.computeButton.clicked.connect(self.control.showNumberOfLabels)

        self.buttonBox.addButton("Cancel", QDialogButtonBox.RejectRole)
        self.buttonBox.rejected.connect(self.reject)

        self.layout.addWidget(self.buttonBox)
