
from sleepy.gui.builder.customwidgets import CustomQCheckBox, CustomQDoubleSpinBox
from sleepy.gui.settings.updateunit import ApplicationSettingsUnit
from sleepy.gui.builder import Builder
import pdb

class ApplicationSettingsAPI:

    def __init__(self, app):

        self.app = app

        self.useCheckpoints = ApplicationSettingsUnit("useCheckpoints", 1)
        self._intervalMin = ApplicationSettingsUnit("intervalMin", .0)
        self._intervalMax = ApplicationSettingsUnit("intervalMax", .0)
        self.showIndex = ApplicationSettingsUnit("showIndex", 0)

        self.builder = Builder()

        self.layouts = {}

        self.build()

    @property
    def updateObjects(self):
        return self.builder.updateObjects

    @property
    def intervalMin(self):
        return self._intervalMin.value

    @property
    def intervalMax(self):
        return self._intervalMax.value

    @property
    def tree(self):

        return {
            "plots" : {
                "title" : "Plots",
                "checkpoints" : {
                    "title" : "Checkpoints",
                    "fields" : {
                            "useCheckpoints" : {
                            "title" : "Enable Checkpoints",
                            "widgetType" : CustomQCheckBox,
                            "unit" : self.useCheckpoints
                        }
                    }
                },
                "intervals" : {
                    "title" : "Intervals",
                    "fields" : {
                            "intervalMin" : {
                            "title" : "Interval Min (seconds)",
                            "widgetType" : CustomQDoubleSpinBox,
                            "unit" : self._intervalMin
                        },
                            "intervalMax" : {
                            "title" : "Interval Max (seconds)",
                            "widgetType" : CustomQDoubleSpinBox,
                            "unit" : self._intervalMax
                        }
                    }
                },
                "index" : {
                    "title" : "Index",
                    "fields" : {
                        "showIndex" : {
                            "title" : "Show index of plots",
                            "widgetType" : CustomQCheckBox,
                            "unit" : self.showIndex
                        }
                    }
                }
            }
        }

    def build(self):

        list(map(
            lambda id: self.buildTab(id), self.tree
        ))

    def buildTab(self, id):

        tab = self.tree[id]

        tab.pop("title")

        self.layouts[id] = self.builder.build(tab)

    def getValue(self, variable):

        updateObject = self.findUpdateObject(variable)

        if updateObject:

            return updateObject.getSettingFor("value")

    def findUpdateObject(self, variable):

        objects = list(
            filter(
                lambda object: object.name == variable,
                self.builder.updateObjects
            )
        )

        if len(objects) > 0:

            return objects[0]
        else:

            return None
