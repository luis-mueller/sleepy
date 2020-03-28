
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QShortcut
from PyQt5.QtGui import QKeySequence
from sleepy.gui.stack import EnvironmentStack
from sleepy.io.manager import FileManager
from sleepy.gui.settings.v2.core import Settings

class Window(QMainWindow):
    """Initializes the menu bar and creates a stack of widgets which can be
    swapped contextually. It inherits :class:`PyQt5.QMainWindow` and serves mostly as
    a frame to the different contexts. For more information about contexts refer
    to the documenation of :class:`ContextWidget` and all its subclasses.

    :param name: Necessary for contexts to manipulate the window title relative
                 to the application title.
    """

    def __init__(self, name, supportedLoaders):

        super().__init__()

        if supportedLoaders:

            self.fileManager = FileManager(self, supportedLoaders)
        else:

            self.fileManager = FileManager(self)

        self.name = name

        self.applicationSettings = Settings(self, self.onRefresh)
        self.applicationSettings.update()

        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        self.initializeMenu()
        self.initializeShortcuts()

        self.stack = EnvironmentStack(self)
        self.setCentralWidget(self.stack)

    def initializeMenu(self):
        """Builds the menu bar and connects the below handlers to the respective
        events."""

        self.applicationMenuBar = self.menuBar()

        fileMenu = self.applicationMenuBar.addMenu('File')
        openFile = QAction('Open', self)
        openFile.triggered.connect(self.onOpenFile)
        fileMenu.addAction(openFile)

        self.saveFile = QAction('Save', self)
        fileMenu.addAction(self.saveFile)

        self.clearFile = QAction('Clear', self)
        self.clearFile.triggered.connect(self.onClearFile)
        fileMenu.addAction(self.clearFile)

        userMenu = self.applicationMenuBar.addMenu('User')
        settings = QAction('Settings', self)
        settings.triggered.connect(self.applicationSettings.view.exec_)
        userMenu.addAction(settings)

    def initializeShortcuts(self):

        self.openFile = QShortcut(QKeySequence("Ctrl+O"), self)
        self.openFile.activated.connect(self.onOpenFile)

        self.openSettings = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.openSettings.activated.connect(self.applicationSettings.view.exec_)

    def onOpenFile(self):
        """Triggered when the user wants to open a new file to work with. Handed over
        to the stack to try to switch to a labelling context with this file."""

        fileLoader = self.fileManager.openNew()

        if fileLoader:

            self.stack.switchToTagging(fileLoader)

    def onRefresh(self):

        try:
            self.stack.refresh()
        except AttributeError:
            pass

    def onClearFile(self):
        """Triggered when the user wants to clear the currently loaded file. This
        neccessitates a context switch and has to be confirmed."""

        self.stack.switchToNull()

    def closeEvent(self, event):
        """Triggered when the user wants to close the application. This amounts to
        a context switch similar to a null switch and therefore has to be confirmed."""

        # If we can switch to Null then we can also close
        switchSuccessful = self.stack.switchToNull()

        if switchSuccessful:
            event.accept()
        else:
            event.ignore()
