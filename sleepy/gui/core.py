
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings
from sleepy.gui.window import Window
from sleepy.gui.constants import ORGANIZATION, APPLICATION, ICON

class SleePyGUI(QApplication):
    """Used to load the GUI. It builds the starting window and sets a provisional
    GUI title as well as an icon. Inherits form :class:`PyQt5.QApplication`
    """

    def __init__(self, supportedLoaders = None):

        super().__init__(list())

        self.setOrganizationName(ORGANIZATION)
        self.setApplicationName(APPLICATION)

        #QSettings().clear()

        self.name = APPLICATION
        self.icon = ICON

        self.supportedLoaders = supportedLoaders

    def run(self):
        """Creates a new main window, sets title and icon and starts it. For a
        rich documentation of the features inside of the window refer to the
        corresponding class, namely :class:`Window`
        """

        window = Window(self.name, self.supportedLoaders)

        window.setWindowTitle(self.name)

        if self.icon:
            path = os.path.dirname(os.path.realpath(__file__))
            iconObject = QIcon(path + os.path.sep + self.icon)
            window.setWindowIcon(iconObject)

        window.show()

        self.exec_()
