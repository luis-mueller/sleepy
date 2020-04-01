
from sleepy.gui.builder import Builder
import numpy as np
from scipy.signal import find_peaks
from PyQt5.QtWidgets import QWidget
from sleepy import SLEEPY_ROOT_DIR
import pdb

class Algorithm:

    def setAttributesRelative(self, path):

        self.setAttributes(SLEEPY_ROOT_DIR + '/' + path)

    def setAttributes(self, path):

        viewData = Builder.loadJSON(path)

        self.name = viewData["name"]
        self.parameters = viewData["parameters"]

        Builder.setAttributesFromJSON(self.parameters, self, level = 1)

    @property
    def options(self):

        try:
            return self.widget
        except AttributeError:

            self.widget = QWidget()

            layout = Builder.build(self.parameters, self, level = 1)

            self.widget.setLayout(layout)

            return self.widget
