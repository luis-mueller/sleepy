
from PyQt5.QtWidgets import QDialog, QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QDialogButtonBox
from sleepy.gui.builder import Builder
import pdb
import json

class SettingsView(QDialog):

    def __init__(self, control, application):

        super().__init__(application)

        #self.layout = self.buildLayout(control)

        print(json.dumps({
                "general" : {
                    "title" : "General",
                    "content" : {
                        "checkpoints" : {
                          "title" : "Checkpoints",
                          "fields" : {
                            "useCheckpoints" : {
                                "title" : 'Use Checkpoints',
                                "fieldType" : 'bool',
                                "default" : False
                            }
                          }
                        },
                        "windowBar" : {
                          "title" : "Window Bar",
                          "fields" : {
                            "showIndex" : {
                                "title" : 'Show number of current event',
                                "fieldType" : 'bool',
                                "default" : True
                            }
                          }
                        }
                    }
                },
                "events" : {
                    "title" : "Events",
                    "content" : {
                        "intervals" : {
                          "title" : "Displayed intervals",
                          "fields" : {
                            "intervalMin" : {
                                "title" : 'Seconds displayed before event',
                                "fieldType" : 'float',
                                "default" : 3.0
                            },
                            "intervalMax" : {
                                "title" : 'Seconds displayed after event',
                                "fieldType" : 'float',
                                "default" : 3.0
                            }
                          }
                        }
                    }
                }
            }))

        layout = Builder.buildTabs({
                "general" : {
                    "title" : "General",
                    "content" : {
                        "checkpoints" : {
                          "title" : "Checkpoints",
                          "fields" : {
                            "useCheckpoints" : {
                                "title" : 'Use Checkpoints',
                                "fieldType" : bool,
                                "default" : False
                            }
                          }
                        },
                        "windowBar" : {
                          "title" : "Window Bar",
                          "fields" : {
                            "showIndex" : {
                                "title" : 'Show number of current event',
                                "fieldType" : bool,
                                "default" : True
                            }
                          }
                        }
                    }
                },
                "events" : {
                    "title" : "Events",
                    "content" : {
                        "intervals" : {
                          "title" : "Displayed intervals",
                          "fields" : {
                            "intervalMin" : {
                                "title" : 'Seconds displayed before event',
                                "fieldType" : float,
                                "default" : 3.0
                            },
                            "intervalMax" : {
                                "title" : 'Seconds displayed after event',
                                "fieldType" : float,
                                "default" : 3.0
                            }
                          }
                        }
                    }
                }
            }, control)

        layout.addWidget(self.buildButtonBox(control))

        self.setLayout(layout)

    def buildLayout(self, control):
        """Creates a vertical layout adding a :class:`QTabWidget` and extending
        that widget with multiple tabs.
        """

        layout = QVBoxLayout()

        tabs = QTabWidget()

        tabs.addTab(*self.buildGeneralTab(control))

        tabs.addTab(*self.buildEventsTab(control))

        layout.addWidget(tabs)

        layout.addWidget(self.buildButtonBox(control))

        return layout

    def buildGeneralTab(self, control):
        """Uses the :class:`Builder` to create a layout for the general tab.
        """

        tab = QWidget()

        tabLayout = Builder.build({
            "checkpoints" : {
              "title" : "Checkpoints",
              "fields" : {
                "useCheckpoints" : {
                    "title" : 'Use Checkpoints',
                    "fieldType" : bool,
                    "default" : False
                }
              }
            },
            "windowBar" : {
              "title" : "Window Bar",
              "fields" : {
                "showIndex" : {
                    "title" : 'Show number of current event',
                    "fieldType" : bool,
                    "default" : True
                }
              }
            }
          }, control)

        tab.setLayout(tabLayout)

        return tab, "General"

    def buildEventsTab(self, control):
        """Uses the :class:`Builder` to create a layout for the events tab.
        """

        tab = QWidget()

        tabLayout = Builder.build({
            "intervals" : {
              "title" : "Displayed intervals",
              "fields" : {
                "intervalMin" : {
                    "title" : 'Seconds displayed before event',
                    "fieldType" : float,
                    "default" : 3.0
                },
                "intervalMax" : {
                    "title" : 'Seconds displayed after event',
                    "fieldType" : float,
                    "default" : 3.0
                }
              }
            }
          }, control)

        tab.setLayout(tabLayout)

        return tab, "Events"

    def buildButtonBox(self, control):

        buttonBox = QDialogButtonBox()
        buttonBox.addButton("Save", QDialogButtonBox.AcceptRole)
        buttonBox.accepted.connect(control.update)
        buttonBox.accepted.connect(super().accept)

        buttonBox.addButton("Cancel", QDialogButtonBox.RejectRole)
        buttonBox.rejected.connect(control.recover)
        buttonBox.rejected.connect(super().reject)

        return buttonBox
