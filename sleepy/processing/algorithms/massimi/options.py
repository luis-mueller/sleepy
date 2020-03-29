
from sleepy.processing.constants import MU
from sleepy.gui.builder import Builder, UpdateUnit

class MassimiOptionView:

    def __init__(self):

        self.separation = UpdateUnit(.3)
        self.negativePeak = UpdateUnit(40)
        self.negativeToPositivePeak = UpdateUnit(70)

        self.builder = Builder()

    @property
    def options(self):

        try:
            return self._widget
        except AttributeError:
            pass

        self._widget = QWidget()
        self._widget.setLayout(self.layout)

        return self._widget

    @property
    def layout(self):

        return self.builder.build({
            "params" : {
                "title" : "Parameters",
                "fields" : {
                    "separation" : {
                        "title" : "Separation of zero-crossings (seconds)",
                        "fieldType" : "float",
                        "default" : self.separation
                    },
                    "negativePeak" : {
                        "title" : "Required height of negative peak (-{}V)".format(MU),
                        "fieldType" : "float",
                        "default" : self.negativePeak
                    },
                    "negativeToPositivePeak" : {
                        "title" : "Negative-To-Positive peak ({}V)".format(MU),
                        "fieldType" : "float",
                        "default" : self.negativeToPositivePeak
                    }
                }
            }
        })
