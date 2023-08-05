# vim: set fileencoding=utf-8 :
###############################################################################
#                                                                             #
# Copyright (c) 2019 Idiap Research Institute, http://www.idiap.ch/           #
# Contact: beat.support@idiap.ch                                              #
#                                                                             #
# This file is part of the beat.editor module of the BEAT platform.           #
#                                                                             #
# Commercial License Usage                                                    #
# Licensees holding valid commercial BEAT licenses may use this file in       #
# accordance with the terms contained in a written agreement between you      #
# and Idiap. For further information contact tto@idiap.ch                     #
#                                                                             #
# Alternatively, this file may be used under the terms of the GNU Affero      #
# Public License version 3 as published by the Free Software and appearing    #
# in the file LICENSE.AGPL included in the packaging of this file.            #
# The BEAT platform is distributed in the hope that it will be useful, but    #
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY  #
# or FITNESS FOR A PARTICULAR PURPOSE.                                        #
#                                                                             #
# You should have received a copy of the GNU Affero Public License along      #
# with the BEAT platform. If not, see http://www.gnu.org/licenses/.           #
#                                                                             #
###############################################################################

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from ..backend.asset import AssetType
from ..backend.assetmodel import DataFormatModel
from ..decorators import frozen
from ..utils import dataformat_basetypes
from .dialogs import NameInputDialog
from .editor import AbstractAssetEditor
from .scrollwidget import ScrollWidget
from .validatedhelpers import NameLineEdit


def create_button_layout(button):
    """Returns a ready to use layout with a button in it"""

    button_layout = QHBoxLayout()
    button_layout.addStretch(1)
    button_layout.addWidget(button)
    return button_layout


def create_add_button_layout():
    """Returns a ready to use layout as well as add actions"""

    add_pushbutton = QPushButton(QCoreApplication.translate("Dataformat", "Add"))

    add_menu = QMenu(add_pushbutton)
    add_type_action = add_menu.addAction(
        QCoreApplication.translate("Dataformat", "Type")
    )
    add_object_action = add_menu.addAction(
        QCoreApplication.translate("Dataformat", "Object")
    )
    add_type_array_action = add_menu.addAction(
        QCoreApplication.translate("Dataformat", "Type array")
    )
    add_object_array_action = add_menu.addAction(
        QCoreApplication.translate("Dataformat", "Object array")
    )

    add_pushbutton.setMenu(add_menu)

    button_layout = create_button_layout(add_pushbutton)
    return (
        button_layout,
        add_type_action,
        add_object_action,
        add_type_array_action,
        add_object_array_action,
    )


def default_dataformat():
    return dataformat_basetypes()[0]


def default_object_dataformat():
    return {QCoreApplication.translate("Dataformat", "Change_me"): default_dataformat()}


class NameWidget(QWidget):

    foldToggled = pyqtSignal(bool)
    deletionRequested = pyqtSignal()
    textChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.delete_button = QPushButton(self.tr("-"))
        self.delete_button.setFixedSize(30, 30)

        self.fold_button = QPushButton()
        self.fold_button.setFixedSize(30, 30)
        self.fold_button.setCheckable(True)

        self.name_lineedit = NameLineEdit()

        self.name_layout = QHBoxLayout(self)
        self.name_layout.addWidget(QLabel(self.tr("Name:")))
        self.name_layout.addWidget(self.name_lineedit, 10)
        self.name_layout.addStretch(1)
        self.name_layout.addWidget(self.delete_button)
        self.name_layout.addWidget(self.fold_button)

        self.delete_button.clicked.connect(self.deletionRequested)
        self.fold_button.toggled.connect(self.foldToggled)
        self.name_lineedit.textChanged.connect(self.textChanged)

        self.__onFoldToggled(False)

    def __onFoldToggled(self, checked):
        """
        Update the fold button content based on its checked state.

        :param checked bool: Whether the fold button is checked
        """

        icon = (
            QStyle.SP_TitleBarShadeButton
            if checked
            else QStyle.SP_TitleBarUnshadeButton
        )
        tooltip = self.tr("Show") if checked else self.tr("Hide")
        self.fold_button.setIcon(self.style().standardIcon(icon))
        self.fold_button.setToolTip(tooltip)

    def text(self):
        """Text property getter"""

        return self.name_lineedit.text()

    def setText(self, text):
        """Text property setter

        :param text str: Text of the widget
        """

        self.name_lineedit.setText(text)

    text = pyqtProperty(str, fget=text, fset=setText, notify=textChanged)

    def setDeleteToolTip(self, tooltip):
        """Set the tooltip of the delete button

        :param tooltip text: Tooltip of the delete button
        """

        self.delete_button.setToolTip(tooltip)

    def setRemovable(self, removable):
        """Sets whether this widget can be removed

        :param removable bool: is this widget removable
        """

        self.delete_button.setEnabled(removable)
        self.delete_button.setVisible(removable)


class DataformatBaseWidget(QGroupBox):
    """Base widget to build the various 'sub-editors'"""

    nameChanged = pyqtSignal()
    dataChanged = pyqtSignal()
    deletionRequested = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor

        :param parent QWidget: parent of this widget
        """

        super().__init__(parent)

        self.__has_name = False

        self.name_widget = NameWidget()
        self.content_widget = QWidget()
        self.form_layout = QFormLayout(self.content_widget)
        self.form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        layout = QVBoxLayout(self)
        layout.addWidget(self.name_widget)
        layout.addWidget(self.content_widget)

        self.name_widget.textChanged.connect(self.dataChanged)
        self.name_widget.deletionRequested.connect(self.deletionRequested)
        self.name_widget.foldToggled.connect(self.__onFoldToggled)

    @pyqtSlot(bool)
    def __onFoldToggled(self, checked):
        """Fold/unfold the content of the widget

        :param checked bool: Whether the toggle button is checked.
        """

        self.content_widget.setVisible(not checked)

    def setRemovable(self, removable):
        """Sets whether this widget can be removed

        :param removable bool: is this widget removable
        """

        self.name_widget.setRemovable(removable)

    def setHasName(self, has_name):
        """Sets whether the entry shown by this widget has a name

        :param has_name bool: has this widget a name
        """

        self.__has_name = has_name

        self.name_widget.setVisible(self.__has_name)
        # self.form_layout.labelForField(self.name_layout).setVisible(self.__has_name)

    def hasName(self):
        """Returns whether the entry shown by this widget has a name"""

        return self.__has_name

    def setName(self, name):
        """Set the name of the entry shown by this widget

        :param name str: the name of the entry
        """
        self.setHasName(name is not None)
        self.name_widget.setText(name)

    def name(self):
        """Returns the name of the entry shown by this widget"""

        name = ""
        if self.hasName():
            name = self.name_widget.text
        return name


class DataformatWidget(DataformatBaseWidget):
    """Widget representing a type entry"""

    def __init__(self, dataformat_model, parent=None):
        """Constructor

        :param dataformat_model DataFormatModel: model containing the list of
               available dataformats
        :param parent QWidget: parent of this widget
        """

        super().__init__(parent)
        self.dataformat_model = dataformat_model

        self.name_widget.setDeleteToolTip(self.tr("Remove format"))

        self.dataformat_box = QComboBox()
        self.dataformat_box.setModel(self.dataformat_model)

        self.form_layout.addRow(self.tr("Type"), self.dataformat_box)

        self.dataformat_box.currentIndexChanged.connect(self.dataChanged)

    def load(self, name, type_):
        """Load this widget with the content of type_

        :param name str: name of the entry
        :param type_ str: type_ to load
        """

        self.setName(name)
        self.dataformat_box.setCurrentText(type_)

    def dump(self):
        """Returns the json representation of this type"""

        type_data = self.dataformat_box.currentText()

        if self.hasName():
            type_data = {self.name(): self.dataformat_box.currentText()}
        return type_data


class DataformatObjectWidget(DataformatBaseWidget):
    """Widget representing an object entry"""

    def __init__(self, dataformat_model, parent=None):
        """Constructor

        :param dataformat_model DataFormatModel: model containing the list of
               available dataformats
        :param parent QWidget: parent of this widget
        """

        super().__init__(parent)
        self.dataformat_model = dataformat_model

        self.name_widget.setDeleteToolTip(self.tr("Remove object"))

        self.dataformat_widgets = []

        self.dataformat_box = QGroupBox(self.tr("Content"))
        self.dataformat_box_layout = QVBoxLayout(self.dataformat_box)

        self.form_layout.addWidget(self.dataformat_box)
        (
            button_layout,
            self.add_type_action,
            self.add_object_action,
            self.add_type_array_action,
            self.add_object_array_action,
        ) = create_add_button_layout()

        self.form_layout.addRow(button_layout)

        self.add_type_action.triggered.connect(
            lambda: self.__add_entry(default_dataformat())
        )
        self.add_object_action.triggered.connect(
            lambda: self.__add_entry(default_object_dataformat())
        )
        self.add_type_array_action.triggered.connect(
            lambda: self.__add_entry([0, default_dataformat()])
        )
        self.add_object_array_action.triggered.connect(
            lambda: self.__add_entry([0, default_object_dataformat()])
        )

    @pyqtSlot()
    def __onRemoveRequested(self):
        """Removes the widget clicked"""

        self.__remove_widget(self.sender())

    def __remove_widget(self, widget):
        """Removes the widget from this editor

        :param widget QWidget: widget to remove
        """

        self.dataformat_box_layout.removeWidget(widget)
        self.dataformat_widgets.pop(self.dataformat_widgets.index(widget))
        widget.setParent(None)
        self.dataChanged.emit()

    def __add_entry(self, content):
        """Add an entry to the dictionary

        :param content dict: dictionary to load
        """

        format_names = [widgets.name() for widgets in self.dataformat_widgets]

        while True:
            name, ok_pressed = NameInputDialog.getText(self, self.tr("Field name"))
            if not ok_pressed:
                break

            if ok_pressed and name not in format_names:
                self.__load_dict({name: content})
                self.dataChanged.emit()
                break

    def __load_dict(self, type_dict):
        """Load this widget with the content of type_dict

        :param type_dict dict: dictionary to load
        """

        for name, type_ in type_dict.items():
            if isinstance(type_, list):
                dataformat_widget = DataformatArrayWidget(self.dataformat_model)
            elif isinstance(type_, dict):
                dataformat_widget = DataformatObjectWidget(self.dataformat_model)
            else:
                dataformat_widget = DataformatWidget(self.dataformat_model)

            dataformat_widget.load(name, type_)
            self.dataformat_box_layout.addWidget(dataformat_widget)
            self.dataformat_widgets.append(dataformat_widget)

            dataformat_widget.dataChanged.connect(self.dataChanged)
            dataformat_widget.deletionRequested.connect(self.__onRemoveRequested)

    def load(self, name, type_dict):
        """Load this widget with the content of type_dict

        :param name str: name of the entry
        :param type_dict dict: dictionary to load
        """

        if not isinstance(type_dict, dict):
            raise TypeError(
                "This widget only handles dict not {}".format(type(type_dict))
            )

        self.setName(name)
        for widget in self.dataformat_widgets:
            self.__remove_widget(widget)
        self.__load_dict(type_dict)

    def dump(self):
        """Returns the json representation of this dictionary"""

        type_dict = {}
        for widget in self.dataformat_widgets:
            type_dict.update(widget.dump())

        if self.hasName():
            type_dict = {self.name_widget.text: type_dict}
        return type_dict


class DimensionWidget(DataformatBaseWidget):
    """Widget representing an array dimension"""

    def __init__(self, parent=None):
        """Constructor

        :param parent QWidget: parent of this widget
        """

        super().__init__(parent)

        self.setHasName(False)
        self.name_widget.setDeleteToolTip(self.tr("Remove dimension"))

        self.dimension_spin_box = QSpinBox()
        self.form_layout.addRow(self.tr("Dimension"), self.dimension_spin_box)

        self.dimension_spin_box.valueChanged.connect(self.dataChanged)

    def value(self):
        """Returns the value of this array dimension"""

        return self.dimension_spin_box.value()

    def setValue(self, value):
        """Sets the value of this array dimension

        :param value int: value of the dimension
        """

        self.dimension_spin_box.setValue(value)

    def setDimension(self, dimension):
        """Set the dimension which this widget represents

        :param dimension int: which dimension this widget represents
        """

        label = self.form_layout.labelForField(self.dimension_spin_box)
        label.setText(self.tr("{}".format(dimension)))
        self.setObjectName("{} {}".format(__class__.__name__, dimension))


class DataformatArrayWidget(DataformatBaseWidget):
    """Widget representing the content of an array"""

    def __init__(self, dataformat_model, parent=None):
        """Constructor

        :param dataformat_model DataFormatModel: model containing the list of available dataformats
        :param parent QWidget: parent of this widget
        """

        super().__init__(parent)
        self.dataformat_model = dataformat_model

        self.name_widget.setDeleteToolTip(self.tr("Remove array"))

        self.dimension_widgets = []
        self.dataformat_widget = None

        self.dimension_box = QGroupBox(self.tr("Dimensions"))
        self.add_dimension_button = QPushButton(self.tr("+"))
        self.add_dimension_button.setToolTip(self.tr("Add dimension"))
        self.add_dimension_button.setFixedSize(30, 30)
        add_dimension_layout = create_button_layout(self.add_dimension_button)

        self.dimension_layout = QVBoxLayout(self.dimension_box)
        self.dimension_layout.addLayout(add_dimension_layout)

        self.widget_layout = QVBoxLayout()
        self.widget_layout.addWidget(self.dimension_box)

        self.form_layout.addRow(self.widget_layout)
        self.add_dimension_button.clicked.connect(lambda: self.__load_array([0]))

        self.__add_dimension(0, 0)

    def __onRemoveRequested(self):
        """Remove the widget clicked"""

        self.__remove_widget(self.sender())

    def __remove_widget(self, widget):
        """Removes the widget from this editor

        :param widget QWidget: widget to remove
        """

        if widget is None:
            return

        widget.hide()

        if isinstance(widget, DimensionWidget):
            index = self.dimension_layout.indexOf(widget)
            self.dimension_layout.takeAt(index)

            index = self.dimension_widgets.index(widget)
            self.dimension_widgets.pop(index)
            for dimension_widget in self.dimension_widgets:
                index = self.dimension_widgets.index(dimension_widget)
                dimension_widget.setDimension(index)
                dimension_widget.setRemovable(index != 0)

        else:
            self.layout().removeWidget(widget)
            self.dataformat_widget = None

        widget.setParent(None)

        self.dataChanged.emit()

    def __add_dimension(self, dimension, value):
        """Add a new dimension to the array with the given value

        :param dimension int: dimension of the array
        :param value int: value of the dimension
        """

        dimension_widget = DimensionWidget()
        dimension_widget.setValue(value)
        dimension_widget.setDimension(dimension)
        dimension_widget.setRemovable(dimension != 0)
        dimension_widget.dataChanged.connect(self.dataChanged)
        dimension_widget.deletionRequested.connect(self.__onRemoveRequested)

        self.dimension_widgets.append(dimension_widget)

        return dimension_widget

    def __load_array(self, type_array):
        """Loads this widget widget with content of type_array

        :param type_array list:  array to load
        """

        while type_array:
            item = type_array.pop(0)

            if isinstance(item, int):
                editor = self.__add_dimension(len(self.dimension_widgets), item)

            elif isinstance(item, dict):
                editor = DataformatObjectWidget(self.dataformat_model)

            elif isinstance(item, list):
                raise ValueError("Invalid array content")

            else:
                editor = DataformatWidget(self.dataformat_model)

            if isinstance(editor, DimensionWidget):
                self.dimension_layout.insertWidget(
                    self.dimension_layout.count() - 1, editor
                )
            else:
                self.dataformat_widget = editor
                self.dataformat_widget.setRemovable(False)
                self.dataformat_widget.load(None, item)
                self.widget_layout.addWidget(self.dataformat_widget)

            editor.dataChanged.connect(self.dataChanged)
            editor.deletionRequested.connect(self.__onRemoveRequested)
        self.dataChanged.emit()

    def load(self, name, type_array):
        """Load this widget with the content of type_array

        :param name str: name of the entry
        :param type_array list: array to load
        """

        if not isinstance(type_array, list):
            raise TypeError(
                "This widget only handles array not {}".format(type(type_array))
            )

        self.setName(name)
        for widget in self.dimension_widgets:
            self.__remove_widget(widget)
        self.__remove_widget(self.dataformat_widget)
        # load a copy because we modify it
        self.__load_array(type_array.copy())

    def dump(self):
        """Returns the json representation of this array"""

        type_data = []

        for widget in self.dimension_widgets:
            type_data.append(widget.value())

        type_data.append(self.dataformat_widget.dump())

        if self.hasName():
            type_data = {self.name(): type_data}

        return type_data


@frozen
class DataformatEditor(AbstractAssetEditor):
    """Editor for the Dataformat asset"""

    def __init__(self, parent=None):
        """Constructor

        :param parent QWidget: parent of this widget
        """

        super().__init__(AssetType.DATAFORMAT, parent)
        self.setObjectName(self.__class__.__name__)
        self.set_title(self.tr("Dataformat"))

        self.dataformat_model = DataFormatModel()
        self.dataformat_model.full_list_enabled = True

        self.extends_label = QLabel()
        self._add_information_widget(self.tr("Extends"), self.extends_label)
        self.schema_version_label = QLabel()
        self._add_information_widget(
            self.tr("Schema version"), self.schema_version_label
        )

        self.scroll_widget = ScrollWidget()

        (
            button_layout,
            self.add_type_action,
            self.add_object_action,
            self.add_type_array_action,
            self.add_object_array_action,
        ) = create_add_button_layout()

        self.layout().addWidget(self.scroll_widget, 1)
        self.layout().addLayout(button_layout)

        self.scroll_widget.dataChanged.connect(self.dataChanged)
        self.add_type_action.triggered.connect(
            lambda: self.__add_entry(default_dataformat())
        )
        self.add_object_action.triggered.connect(
            lambda: self.__add_entry(default_object_dataformat())
        )
        self.add_type_array_action.triggered.connect(
            lambda: self.__add_entry([0, default_dataformat()])
        )
        self.add_object_array_action.triggered.connect(
            lambda: self.__add_entry([0, default_object_dataformat()])
        )

        self.contextChanged.connect(
            lambda: self.dataformat_model.setPrefixPath(self.prefix_path)
        )

    @property
    def dataformat_widgets(self):
        return self.scroll_widget.widget_list

    def __add_entry(self, content):
        """Add a new dataformat entry to the editor

        :parameter content: default content to be set inside the new editor
        """

        format_names = [widgets.name() for widgets in self.dataformat_widgets]
        while True:
            name, ok_pressed = NameInputDialog.getText(self, self.tr("Field name"))
            if not ok_pressed:
                break

            if ok_pressed and name not in format_names:
                self._load_json({name: content})
                self.dataChanged.emit()
                break

    def __onRemoveRequested(self):
        self.__remove_widget(self.sender())

    def __remove_widget(self, widget):
        """Removes the widget that which signal triggered this slot"""

        self.scroll_widget.removeWidget(widget)

    def _asset_models(self):
        """Reimpl"""

        return [self.dataformat_model]

    def _load_json(self, json_object):
        """Re-impl Load the json object passed as parameter"""

        self.description_lineedit.setText(json_object.get("#description"))
        extends = json_object.get("#extends")
        if extends:
            self.extends_label.setText(extends)
        else:
            self.extends_label.setText("")
        self._set_information_widget_visible(
            self.extends_label, self.extends_label.text() != ""
        )

        schema_version = json_object.get("#schema_version")
        if schema_version:
            self.schema_version_label.setText(str(schema_version))
        else:
            self.schema_version_label.setText("")
        self._set_information_widget_visible(
            self.schema_version_label, self.schema_version_label.text() != ""
        )

        data_types = {
            key: value for key, value in json_object.items() if not key.startswith("#")
        }

        for name, type_ in data_types.items():
            if isinstance(type_, list):
                klass = DataformatArrayWidget
            elif isinstance(type_, dict):
                klass = DataformatObjectWidget
            else:
                klass = DataformatWidget

            dataformat_widget = klass(self.dataformat_model)
            dataformat_widget.load(name, type_)

            self.scroll_widget.addWidget(dataformat_widget)
            dataformat_widget.deletionRequested.connect(self.__onRemoveRequested)

    def _dump_json(self):
        """Returns the json representation of the asset"""

        json_data = {}

        if self.description_lineedit.text():
            json_data["#description"] = self.description_lineedit.text()

        if self.extends_label.text():
            json_data["#extends"] = self.extends_label.text()

        if self.schema_version_label.text():
            json_data["#schema_version"] = int(self.schema_version_label.text())

        for widget in self.dataformat_widgets:
            json_data.update(widget.dump())

        return json_data

    def load_json(self, json_object):
        """Load the json object passed as parameter"""

        self.blockSignals(True)

        self.scroll_widget.clear()

        self.blockSignals(False)

        self._load_json(json_object)

        self.clearDirty()

    def dump_json(self):
        """Returns the json representation of the asset"""

        return self._dump_json()
