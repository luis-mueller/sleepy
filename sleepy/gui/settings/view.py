
from PyQt5.QtWidgets import QDialogButtonBox, QDialog
from sleepy.gui.builder import Builder
from sleepy import SLEEPY_ROOT_DIR

class SettingsView(QDialog):

    def __init__(self, control, application):

        super().__init__(application)

        layout = Builder.build(SLEEPY_ROOT_DIR + '/gui/settings/view.json', control, level = 3)

        layout.addStretch()

        layout.addWidget(self.buildButtonBox(control))

        self.setLayout(layout)

    def buildButtonBox(self, control):

        buttonBox = QDialogButtonBox()
        buttonBox.addButton("Save", QDialogButtonBox.AcceptRole)
        buttonBox.accepted.connect(control.update)
        buttonBox.accepted.connect(super().accept)

        buttonBox.addButton("Cancel", QDialogButtonBox.RejectRole)
        buttonBox.rejected.connect(control.reset)
        buttonBox.rejected.connect(super().reject)

        return buttonBox
