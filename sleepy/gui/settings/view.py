
from PyQt5.QtWidgets import QDialog, QTabWidget, QGroupBox, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtCore import QSettings

class ApplicationSettingsView(QDialog):
    """Handles the display of the global settings (as saved and restored with
    :class:`QSettings`).
    """

    def __init__(self, app, api):

        super().__init__(app)

        self.app = app
        self.api = api

        self.setMinimumWidth(600)

        self.layout = QVBoxLayout()
        self.tabWidget = QTabWidget()

    def initializeButtonBox(self):

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton("Save", QDialogButtonBox.AcceptRole)
        self.buttonBox.accepted.connect(self.save)

        self.buttonBox.addButton("Cancel", QDialogButtonBox.RejectRole)
        self.buttonBox.rejected.connect(self.reject)

        self.layout.addWidget(self.buttonBox)

    def addSettingsTab(self, tab):

        self.tab = QWidget()
        self.tabName = tab

        self.tabWidget.addTab(self.tab, tab)

        self.tabLayout = QVBoxLayout()

    def addSettingsBoxes(self, boxesLayout):

        self.tabLayout.addLayout(boxesLayout)

    def doneWithTab(self):

        self.tab.setLayout(self.tabLayout)

    def doneBuilding(self):

        self.layout.addWidget(self.tabWidget)

        self.initializeButtonBox()

        self.setLayout(self.layout)

    def save(self):
        
        self.app.onRefresh()

        self.accept()

    def onExecute(self):

        self.exec_()
