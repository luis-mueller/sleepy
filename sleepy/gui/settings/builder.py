
from sleepy.gui.settings.constants import SLASH
from sleepy.gui.builder import Builder
from PyQt5.QtCore import QSettings
from functools import partial
import pdb

class ApplicationSettingsBuilder(Builder):
    """This class loads :class:QSettings and displays them in a GUI interface"""

    def __init__(self, api, view):

        super().__init__()

        self.api = api

        self.view = view

    def build(self):

        buildTree = self.api.tree

        list(map(
            lambda id: self.buildTab(id), buildTree
        ))

        self.view.doneBuilding()

    def buildTab(self, id):

        tab = self.api.tree.copy()[id]

        title = tab.pop("title")

        self.view.addSettingsTab(title)

        boxesLayout = self.api.layouts[id]

        self.view.addSettingsBoxes(boxesLayout)

        self.view.doneWithTab()
