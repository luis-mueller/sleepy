
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QCheckBox, QMenu, QAction
import PyQt5.Qt as Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QStackedWidget, QShortcut
from PyQt5.QtGui import QKeySequence
from functools import partial
import matplotlib
from matplotlib.figure import Figure
import matplotlib.backends.backend_qt5agg as pltQt5
#matplotlib.use('QT5Agg')
from matplotlib.ticker import ScalarFormatter
matplotlib.rcParams['axes.formatter.useoffset'] = False
import pdb
from sleepy.tagging.model.timeline import Timeline

class NullView(QWidget):
    """Implements the null context. The null context disables save and clear
    options in the menu and sets the window title to the application name.
    The :class:`CustomStackedWidget` stacks an instance of this class. Inherits
    from :class:`ContextWidget`.
    """
    def __init__(self, app):

        super().__init__(app)

        self.app = app

        self.initializeLayout()

    def initializeLayout(self):

        #self.app.setStyleSheet("QMainWindow { background-color: #2F2F2F }")

        self.labelLayout = QVBoxLayout()

        self.nullLabel = QLabel("Load a dataset to get started.")
        self.nullLabel.setStyleSheet("QLabel { font: 11pt; font-family: 'Arial'; color : black; }")
        self.nullLabel.move(
            ( self.app.width() - self.nullLabel.width() ) / 2,
            ( self.app.height() - self.nullLabel.height() ) / 2
        )
        self.nullLabel.setAlignment(Qt.Qt.AlignCenter)

        self.labelLayout.addWidget(self.nullLabel)

        self.setLayout(self.labelLayout)

    def open(self):
        """Disables unnecessary menu features and resets the window title."""

        self.app.clearFile.setDisabled(True)
        self.app.saveFile.setDisabled(True)
        self.app.reloadFile.setDisabled(True)

        self.app.setWindowTitle(self.app.name)

class TaggingView(QWidget):

    def __init__(self, app, control):
        """UI-part of the tagging environment. Does not implement application
        logic but abstracts UI-functionality to the control. The :class:`TaggingView`
        also creates all PyQt5-objects and connects them to the control (if needed).
        """

        super().__init__(app)

        self.app = app
        self.control = control
        self.plotFunction = None

        self.initializeLayout()

        self.initializeShortcuts()

        self.app.saveFile.triggered.connect(self.control.onSaveFile)

    def initializeLayout(self):

        self.layout = QVBoxLayout(self)
        self.initializeFigure()

        self.buttonLayout = QHBoxLayout()
        self.initializeButtons()

        self.layout.addLayout(self.buttonLayout)

    def initializeFigure(self):

        self.figure = Figure()
        self.axis, self.timelineAxis = self.figure.subplots(2,1, gridspec_kw={'height_ratios': [8, 1]})

        self.figure.set_tight_layout(True)
        self.figureCanvas = pltQt5.FigureCanvas(self.figure)

        self.layout.addWidget(self.figureCanvas)
        self.plotToolBar = pltQt5.NavigationToolbar2QT(self.figureCanvas, self)

        noOffset = ScalarFormatter(useOffset=False)
        self.axis.xaxis.set_major_formatter(noOffset)
        self.timelineAxis.xaxis.set_major_formatter(noOffset)

        self.figure.canvas.mpl_connect('button_press_event', self.onClick)

        self.timeline = Timeline(self.timelineAxis)

    def initializeButtons(self):

        self.buttonPrevious = QPushButton('Previous')
        self.buttonPrevious.clicked.connect(self.control.onPreviousClick)

        self.buttonTagging = QPushButton()
        self.buttonTagging.clicked.connect(self.control.onTaggingClick)

        self.buttonNext = QPushButton('Next')
        self.buttonNext.clicked.connect(self.control.onNextClick)

        self.buttonLayout.addWidget(self.buttonPrevious)
        self.buttonLayout.addWidget(self.buttonTagging)
        self.buttonLayout.addWidget(self.buttonNext)

    def initializeShortcuts(self):

        self.navigateRight = QShortcut(QKeySequence("Right"), self.app)
        self.navigateRight.activated.connect(self.control.onNextClick)

        self.navigateLeft = QShortcut(QKeySequence("Left"), self.app)
        self.navigateLeft.activated.connect(self.control.onPreviousClick)

        self.selectPress = QShortcut(QKeySequence("P"), self.app)
        self.selectPress.activated.connect(self.control.onTaggingClick)

        self.selectPressAlternative = QShortcut(QKeySequence("Up"), self.app)
        self.selectPressAlternative.activated.connect(self.control.onTaggingClick)

        self.savePress = QShortcut(QKeySequence("Ctrl+S"), self.app)
        self.savePress.activated.connect(self.control.onSaveFile)

    def open(self):

        self.addToolBar()

        self.app.clearFile.setDisabled(False)
        self.app.reloadFile.setDisabled(False)

    def setButtonStyle(self, stylesheet, text):

        self.buttonTagging.setStyleSheet(stylesheet)
        self.buttonTagging.setText(text)

    def removeToolBar(self):

        self.app.removeToolBar(self.plotToolBar)

    def addToolBar(self):

        self.app.addToolBar(self.plotToolBar)

    def plot(self, plotFunction):

        # Resets the toolbar-history
        self.plotToolBar.update()

        self.axis.cla()

        if self.app.applicationSettings.plotGrid:
            self.axis.grid()

        plotFunction(self.axis)

        self.figure.canvas.draw_idle()

    def draw(self):
        """Abstracts calling the draw method of the figure canvas.
        """

        self.figure.canvas.draw()

    def refreshTimeline(self):
        """Clears the plot on the timeline axis and requests the control to
        initialize a new timeline and plot it.
        """

        self.timelineAxis.cla()

        self.control.configureTimeline()

        self.figure.canvas.draw_idle()

    def getTimeline(self):
        """Creates a new Timeline object for the control and supplies a
        proper axis to plot to.
        """

        return Timeline(self.timelineAxis)

    def onClick(self, event):
        """Called when user clicks any plot. Can be used to redirect clicks
        dependent on the the axis or the type of click.
        """

        if event.inaxes == self.timelineAxis and event.dblclick:

            self.control.onTimelineClick(event.xdata)

        elif event.inaxes == self.axis and event.dblclick:

            self.control.onMainDblClick(event)

        # Button == 3 <=> right-click
        if event.inaxes == self.timelineAxis and event.button == 3:
            self.showMenuTimlineRightClick()

    def showMenuUserEventRemove(self, userEvent):

        menu = QMenu(self.app)

        remove = QAction("Remove User-Event", self.app)

        removeUserEvent = partial(self.control.removeUserEvent, userEvent)
        remove.triggered.connect(removeUserEvent)

        menu.addAction(remove)

        menu.move(QCursor().pos())
        menu.show()

    def showMenuUserEventCreate(self, event):

        menu = QMenu(self.app)

        create = QAction("Create User-Event", self.app)

        createUserEvent = partial(self.control.createUserEvent, event)
        create.triggered.connect(createUserEvent)

        menu.addAction(create)

        menu.move(QCursor().pos())
        menu.show()

    def showMenuTimlineRightClick(self):

        menu = QMenu(self.app)

        reset = QAction("Reset Timeline", self.app)

        reset.triggered.connect(self.refreshTimeline)

        menu.addAction(reset)

        menu.move(QCursor().pos())
        menu.show()

    def tellUserNavigationFlawed(self):

        return QMessageBox.critical(
            self.app, 'Event Detection', '[INTERNAL ERROR]: Unable to load events, please try again.',
            QMessageBox.Ok
        )

    def askUserForCheckPoint(self):

        return QMessageBox.question(
            self.app, 'Checkpoints', 'Would you like to set a checkpoint for the current sample? Warning: This will be stored in the dataset.',
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Cancel
        )

    def askUserForCheckPointRestore(self, checkpoint):

        return QMessageBox.question(
            self.app, 'Checkpoints', 'Recover checkpoint at sample {}?'.format(checkpoint),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )

    def tellUserNoEventsFound(self):

        return QMessageBox.information(
            self.app, 'Event Detection', 'The algorithm was unable to find events with the given parameters.',
            QMessageBox.Ok
        )

    def askUserForSwitch(self):

        return QMessageBox.question(
            self.app, 'Confirm', 'Save changes?',
            QMessageBox.Discard | QMessageBox.Save | QMessageBox.Cancel,
            QMessageBox.Cancel
        )
