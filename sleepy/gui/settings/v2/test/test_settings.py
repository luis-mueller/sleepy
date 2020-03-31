
import unittest
import pdb
import numpy as np
from unittest.mock import MagicMock, Mock, patch, PropertyMock
from sleepy.gui.settings.v2.core import Settings

class SettingsTest(unittest.TestCase):

    def test_construct(self):
        
        settings = Settings()

        try:
            settings.showIndex

            self.assertTrue(True)
        except AttributeError:
            self.assertFalse(True)
