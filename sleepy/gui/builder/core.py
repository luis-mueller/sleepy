
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QCheckBox, QTabWidget, QWidget
from PyQt5.QtWidgets import QDoubleSpinBox, QSpinBox
from sleepy.gui.builder.exceptions import NoBuildTreeAvailable
from sleepy.gui.builder.customwidgets import CustomQSpinBox, CustomQCheckBox, CustomQDoubleSpinBox, Custom0To1DoubleSpinBox
from functools import partial
from pydoc import locate
import pdb

class Builder:

    def callback(function):
        """Decorator function for callback functions used in the build tree that
        precomputes the updated value and supplies it to the callback function.
        This serves PyQt5-agnositics with respect to the user.
        """

        def update(self, key, fieldType, widget):

            value = fieldType(widget.value())

            function(self, key, value)

        return update

    def buildTabs(buildTree, control):
        """Builds a tabbed layout from a level-3-buildtree.
        """

        layout = QVBoxLayout()

        tabs = QTabWidget()

        for key in buildTree.keys():

            title, content = Builder.extractTabData(**buildTree[key])

            tabLayout = Builder.build(content, control)

            tab = QWidget()

            tab.setLayout(tabLayout)

            tabs.addTab(tab, title)

        layout.addWidget(tabs)

        return layout

    def extractTabData(title, content):
        return title, content

    def build(buildTree, control):

        layout = QVBoxLayout()

        list(map(
            lambda p: layout.addLayout(
                Builder.constructBoxLayout(buildTree[p], control
                )
            ),
            buildTree
        ))

        return layout

    def constructBoxLayout(box, control):

        layout = QVBoxLayout()

        title = box['title']

        groupBox = QGroupBox(title)
        boxLayout = QVBoxLayout()

        fields = box['fields']

        for key in fields.keys():

            fieldLayout = Builder.constructFieldLayout(key, control, **fields[key])

            boxLayout.addLayout(fieldLayout)

        groupBox.setLayout(boxLayout)

        layout.addWidget(groupBox)

        return layout

    def constructFieldLayout(identifier, control, title, fieldType, default):

        fieldType = Builder.recoverBuiltInType(fieldType)

        widget = Builder.mapBuiltInTypeToWidget(fieldType)()

        widget.valueChanged.connect(
            partial(
                control.getCallback(identifier),
                fieldType,
                widget
            )
        )

        # Trigger the callback for initialization
        widget.setValue(default)

        return Builder.getLayoutForWidget(widget, title)

    def getLayoutForWidget(widget, title):
        """Creates a horizontal ayout for a widget containing the widget itself and
        a descriptive title attached to it.
        """

        layout = QHBoxLayout()

        if not isinstance(widget, CustomQCheckBox):

            label = QLabel(title)
            layout.addWidget(label)
        else:

            widget.setText(title)

        layout.addWidget(widget)

        return layout

    def mapBuiltInTypeToWidget(fieldType):
        """Maps a list of built-in types to an appropriate widget type. Hence,
        the user can be agnostic of PyQt5 when using the builder, since only
        so many types are supported anyways. The custom widgets are wrappers
        around the original widgets to implement a unified interface
        """

        if fieldType == int:

            return CustomQSpinBox

        elif fieldType == float:

            return CustomQDoubleSpinBox

        elif fieldType == bool:

            return CustomQCheckBox

        else:
            raise TypeError("Field type {} is not supported".format(str(fieldType)))

    def recoverBuiltInType(fieldType):
        """To support JSON input, builtin types must be recovered. However, for
        security reasons, it is best to use pydoc.locate, which recovers only
        builtin types from string, not functions or classes.
        """

        return fieldType if type(fieldType) != str else locate(fieldType)
