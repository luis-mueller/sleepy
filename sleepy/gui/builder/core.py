
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QCheckBox
from sleepy.gui.builder.updateunit import UpdateObject
from sleepy.gui.builder.exceptions import NoBuildTreeAvailable

class Builder:

    def __init__(self):

        self.updateObjects = []

    @property
    def tree(self):
        return self._tree

    @tree.setter
    def tree(self, value):

        if value is None:
            raise NoBuildTreeAvailable()

        self._tree = value

    def build(self, buildTree):

        self.tree = buildTree

        self.layout = QVBoxLayout()

        list(map(
            lambda p: self.layout.addLayout(
                self.constructBoxLayout(self.tree[p]
                )
            ),
            self.tree
        ))

        return self.layout

    def constructBoxLayout(self, box):

        layout = QVBoxLayout()

        title = box['title']

        groupBox = QGroupBox(title)
        boxLayout = QVBoxLayout()

        fields = box['fields']

        list(map(
            lambda p: boxLayout.addLayout(
                self.constructFieldLayout(p, fields[p]
                )
            ),
            fields
        ))

        groupBox.setLayout(boxLayout)

        layout.addWidget(groupBox)

        return layout

    def constructFieldLayout(self, identifier, field):

        title = field['title']
        type = field['widgetType']
        unit = field['unit']

        updateObject = UpdateObject(identifier, type, unit)

        layout = QHBoxLayout()

        if not issubclass(type, QCheckBox):

            label = QLabel(title)
            layout.addWidget(label)
        else:

            updateObject.widget.setText(title)

        layout.addWidget(updateObject.widget)

        self.updateObjects.append(updateObject)

        return layout
