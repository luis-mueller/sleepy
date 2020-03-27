
from sleepy.gui.builder import Builder, UpdateUnit
from PyQt5.QtWidgets import QDoubleSpinBox, QSpinBox
from scipy.signal import butter, filtfilt

class BandPassFilter:

    def __init__(self):

        self.builder = Builder()

        self.lowCutFrequency = UpdateUnit(0.1)
        self.highCutFrequency = UpdateUnit(4.0)
        self.order = UpdateUnit(2)

    @property
    def layout(self):

        return self.builder.build({
            'bandPassFilter' : {
                'title' : 'Bandpass Filter',
                'fields' : {

                    # Descriptions taken from https://mne.tools/0.13/generated/mne.filter.band_pass_filter.html
                    'lowCutFrequency' : {
                        'title' : 'Low cut-off frequency in Hz',
                        'widgetType' : QDoubleSpinBox,
                        'unit' : self.lowCutFrequency
                    },
                    'highCutFrequency' : {
                        'title' : 'High cut-off frequency in Hz',
                        'widgetType' : QDoubleSpinBox,
                        'unit' : self.highCutFrequency
                    },
                    'order' : {
                        'title' : 'Order',
                        'widgetType' : QSpinBox,
                        'unit' : self.order
                    }
                }
            }
        })

    # Implements:
    # https://stackoverflow.com/questions/12093594/how-to-implement-band-pass-butterworth-filter-with-scipy-signal-butter
    def filter(self, data, samplingRate):

        b, a = butter(
            self.order.value,
            [
                self.lowCutFrequency.value / (0.5 * samplingRate),
                self.highCutFrequency.value / (0.5 * samplingRate)
            ],
            btype = 'bandpass'
        )

        return filtfilt(b, a, data)
