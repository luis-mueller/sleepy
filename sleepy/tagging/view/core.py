
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QCheckBox
import PyQt5.Qt as Qt
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QStackedWidget, QShortcut
from PyQt5.QtGui import QKeySequence
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_qt5agg as pltQt5
matplotlib.use('QT5Agg')
from matplotlib.ticker import ScalarFormatter
matplotlib.rcParams['axes.formatter.useoffset'] = False
import pdb

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

        self.app.setWindowTitle(self.app.name)

class TaggingView(QWidget):

    def __init__(self, app, control):

        super().__init__(app)

        self.app = app
        self.control = control

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

        self.figure, (self.axis, self.timelineAxis) = plt.subplots(2,1, gridspec_kw={'height_ratios': [8, 1]})
        self.figure.tight_layout(pad=2.0)
        self.figureCanvas = pltQt5.FigureCanvas(self.figure)

        self.layout.addWidget(self.figureCanvas)
        self.plotToolBar = pltQt5.NavigationToolbar2QT(self.figureCanvas, self)

        noOffset = ScalarFormatter(useOffset=False)
        self.axis.xaxis.set_major_formatter(noOffset)
        self.timelineAxis.xaxis.set_major_formatter(noOffset)

        self.figure.canvas.mpl_connect('button_press_event', self.onClick)

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

    def onTagging(self, tag):

        if tag:

            self.buttonTagging.setStyleSheet('QPushButton { background-color: red; color: white; }')
            self.buttonTagging.setText('Tagged as False-Positive')

        else:
            self.buttonTagging.setStyleSheet('')
            self.buttonTagging.setText('Not tagged')

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

    def plotTimeline(self, plotFunction):

        plotFunction(self.timelineAxis)
        self.figure.canvas.draw()

    def onClick(self, event):

        if event.inaxes == self.timelineAxis and event.dblclick:

            self.control.onTimelineClick(event.xdata)
