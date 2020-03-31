
from sleepy.gui.builder import Builder
from scipy.signal import butter, filtfilt
from sleepy import SLEEPY_ROOT_DIR
from PyQt5.QtWidgets import QWidget

class BandPassFilter:

    def __init__(self):

        Builder.setAttributesFromJSON(SLEEPY_ROOT_DIR + '/processing/filters/bandpass.json', self)

    @property
    def name(self):
        return 'Bandpass'

    @property
    def options(self):

        try:
            return self.widget
        except AttributeError:
            widget = QWidget()

            widget.setLayout(
                Builder.build(SLEEPY_ROOT_DIR + '/processing/filters/bandpass.json', self)
            )

            self.widget = widget

            return widget

    # Implements:
    # https://stackoverflow.com/questions/12093594/how-to-implement-band-pass-butterworth-filter-with-scipy-signal-butter
    def filter(self, data, samplingRate):

        b, a = butter(
            self.order,
            [
                self.lowCutFrequency / (0.5 * samplingRate),
                self.highCutFrequency / (0.5 * samplingRate)
            ],
            btype = "bandpass"
        )

        return filtfilt(b, a, data)
