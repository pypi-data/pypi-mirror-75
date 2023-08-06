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

import numpy as np

from PyQt5 import QtCore
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from beat.core.protocoltemplate import ProtocolTemplate

from ..backend.asset import AssetType
from ..backend.assetmodel import AssetModel
from ..decorators import frozen
from ..utils import is_Qt_equal_or_higher
from .editor import AbstractAssetEditor
from .scrollwidget import EditorListWidget
from .scrollwidget import ScrollWidget
from .utils import create_delete_button_and_layout

# ------------------------------------------------------------------------------
# V1 part


class SelectableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse | QtCore.Qt.TextSelectableByKeyboard
        )


class SetViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.name_label = SelectableLabel()
        self.template_label = SelectableLabel()
        self.view_label = SelectableLabel()
        self.outputs_tablewidget = QTableWidget()
        self.outputs_tablewidget.verticalHeader().setVisible(False)
        self.outputs_tablewidget.setColumnCount(2)
        self.outputs_tablewidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.outputs_tablewidget.setHorizontalHeaderLabels(
            [self.tr("Name"), self.tr("Type")]
        )
        self.outputs_tablewidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.outputs_tablewidget.setMinimumHeight(200)

        self.form_layout = QFormLayout(self)
        self.form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.form_layout.addRow(self.tr("Name"), self.name_label)
        self.form_layout.addRow(self.tr("Template"), self.template_label)
        self.form_layout.addRow(self.tr("View"), self.view_label)
        self.form_layout.addRow(self.tr("Outputs"), self.outputs_tablewidget)

    def load(self, json_data):
        self.name_label.setText(json_data["name"])
        self.template_label.setText(json_data["template"])
        self.view_label.setText(json_data["view"])
        outputs = json_data["outputs"]
        self.outputs_tablewidget.setRowCount(len(outputs))
        row = 0
        for name, type_ in outputs.items():
            name_item = QTableWidgetItem(name)
            type_item = QTableWidgetItem(type_)
            self.outputs_tablewidget.setItem(row, 0, name_item)
            self.outputs_tablewidget.setItem(row, 1, type_item)
            row += 1


class ProtocolViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.set_viewers = []

        self.name_label = SelectableLabel()
        self.template_label = SelectableLabel()

        self.sets_layout = QVBoxLayout()
        self.sets_layout.addStretch(1)

        self.form_layout = QFormLayout(self)
        self.form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.form_layout.addRow(self.tr("Name"), self.name_label)
        self.form_layout.addRow(self.tr("Template"), self.template_label)
        self.form_layout.addRow(self.tr("Sets"), self.sets_layout)

    def load(self, json_data):
        self.name_label.setText(json_data["name"])
        self.template_label.setText(json_data["template"])

        for set_ in json_data["sets"]:
            set_viewer = SetViewer()
            set_viewer.load(set_)
            index = self.sets_layout.count() - 1
            self.sets_layout.insertWidget(index, set_viewer, 2)
            self.set_viewers.append(set_viewer)


class DatabaseV1Viewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scroll_widget = ScrollWidget()

        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll_widget)

        self.json_object = None

    def load(self, json_object):
        self.scroll_widget.clear()

        for protocol in json_object.get("protocols", []):
            protocol_viewer = ProtocolViewer()
            protocol_viewer.load(protocol)
            self.scroll_widget.addWidget(protocol_viewer)

        self.json_object = json_object

    def dump(self):
        return self.json_object


# ------------------------------------------------------------------------------
# V2 and more part


class ParameterTypeDelegate(QStyledItemDelegate):
    """Delegate to edit parameter type entries"""

    def __init__(self, parameter_type_model, parent=None):
        super().__init__(parent)
        self.parameter_type_model = parameter_type_model

    def createEditor(self, parent, options, index):
        combobox = QComboBox(parent)
        combobox.setModel(self.parameter_type_model)
        return combobox

    def setModelData(self, editor, model, index):
        new_parameter_type = editor.currentText()
        old_parameter_type = index.data()

        if new_parameter_type != old_parameter_type:
            if is_Qt_equal_or_higher("5.11"):
                sibling = index.siblingAtColumn(2)
            else:
                sibling = index.sibling(index.row(), 2)

            if new_parameter_type == "boolean":
                data = "True"
            elif new_parameter_type == "number":
                data = 0
            else:
                if old_parameter_type == "boolean":
                    # For currently unknown reasons going from boolean to string
                    # doesn't change the model content although setData returns
                    # True. This workaround makes this case work
                    model.setData(sibling, None)
                data = self.tr("Change_me")

            model.setData(sibling, data)

        super().setModelData(editor, model, index)


class ParameterValueDelegate(QStyledItemDelegate):
    """Delegate to edit parameter type entries"""

    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, options, index):
        if is_Qt_equal_or_higher("5.11"):
            parameter_type = index.siblingAtColumn(1).data()
        else:
            parameter_type = index.sibling(index.row(), 1).data()

        if parameter_type == "boolean":
            combobox = QComboBox(parent)
            boolean_model = QStringListModel(["True", "False"])
            combobox.setModel(boolean_model)
            return combobox
        elif parameter_type == "number":
            return QDoubleSpinBox(parent)
        else:
            return super().createEditor(parent, options, index)


class ViewEditor(QWidget):

    dataChanged = pyqtSignal()
    deletionRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.parameter_type_model = QStringListModel()
        self.parameter_type_model.setStringList(["string", "number", "boolean"])

        self.delete_button, delete_layout = create_delete_button_and_layout()

        self.dbset_name_label = QLabel()
        self.view_name_lineedit = QLineEdit()

        self.parameters_tablewidget = QTableWidget()
        self.parameters_tablewidget.verticalHeader().setVisible(False)
        self.parameters_tablewidget.setColumnCount(3)
        self.parameters_tablewidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.parameters_tablewidget.setHorizontalHeaderLabels(
            [self.tr("Name"), self.tr("Type"), self.tr("Value")]
        )
        self.parameters_tablewidget.setMinimumHeight(200)

        # parent is mandatory, otherwise, crash follows when adding a new item
        type_delegate = ParameterTypeDelegate(
            self.parameter_type_model, self.parameters_tablewidget
        )
        value_delegate = ParameterValueDelegate(self.parameters_tablewidget)
        self.parameters_tablewidget.setItemDelegateForColumn(1, type_delegate)
        self.parameters_tablewidget.setItemDelegateForColumn(2, value_delegate)

        self.add_button = QPushButton(self.tr("+"))
        self.add_button.setFixedSize(30, 30)
        self.remove_button = QPushButton(self.tr("-"))
        self.remove_button.setFixedSize(30, 30)
        self.remove_button.setEnabled(False)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)

        form_layout = QFormLayout()
        form_layout.addRow(self.tr("Set"), self.dbset_name_label)
        form_layout.addRow(self.tr("View"), self.view_name_lineedit)
        form_layout.addRow(self.tr("Parameters"), self.parameters_tablewidget)

        layout = QVBoxLayout(self)
        layout.addLayout(delete_layout)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.delete_button.clicked.connect(self.deletionRequested)
        self.add_button.clicked.connect(self.__addParameter)
        self.remove_button.clicked.connect(self.__removeParameters)
        self.view_name_lineedit.textChanged.connect(self.dataChanged)
        self.parameters_tablewidget.itemChanged.connect(self.dataChanged)
        self.parameters_tablewidget.itemSelectionChanged.connect(
            self.__onItemSelectionChanged
        )

    @pyqtSlot()
    def __addParameter(self):
        """Add a new parameter"""

        new_row = self.parameters_tablewidget.rowCount()
        self.parameters_tablewidget.setRowCount(new_row + 1)
        name_item = QTableWidgetItem(self.tr("Name_me"))
        type_item = QTableWidgetItem(self.parameter_type_model.index(0).data())
        value_item = QTableWidgetItem(self.tr("Change_me"))
        self.parameters_tablewidget.setItem(new_row, 0, name_item)
        self.parameters_tablewidget.setItem(new_row, 1, type_item)
        self.parameters_tablewidget.setItem(new_row, 2, value_item)
        self.parameters_tablewidget.scrollToItem(value_item)

    @pyqtSlot()
    def __removeParameters(self):
        """Remove the selected parameter(s)"""

        selected_items = self.parameters_tablewidget.selectedItems()

        rows = []
        while selected_items:
            item = selected_items.pop()
            rows.append(item.row())

        rows = set(sorted(rows))

        while rows:
            row = rows.pop()
            self.parameters_tablewidget.removeRow(row)
        self.dataChanged.emit()

    @pyqtSlot()
    def __onItemSelectionChanged(self):
        self.remove_button.setEnabled(bool(self.parameters_tablewidget.selectedItems()))

    @pyqtSlot(str)
    def setDbSetName(self, name):
        self.dbset_name_label.setText(name)

    def dBSetName(self):
        return self.dbset_name_label.text()

    dbset_name = pyqtProperty(str, fget=dBSetName, fset=setDbSetName)

    def load(self, json_object):
        """Load the json object passed as parameter"""

        self.view_name_lineedit.setText(json_object["view"])
        parameters = json_object.get("parameters", {})
        self.parameters_tablewidget.setRowCount(len(parameters))
        row = 0
        for name, value in parameters.items():
            name_item = QTableWidgetItem(name)
            value_item = QTableWidgetItem(str(value))
            type_item = QTableWidgetItem()

            if isinstance(value, str):
                type_item.setText("string")
            elif isinstance(value, bool):
                value_item.setText("True" if value else "False")
                type_item.setText("boolean")
            else:
                type_item.setText("number")

            self.parameters_tablewidget.setItem(row, 0, name_item)
            self.parameters_tablewidget.setItem(row, 1, type_item)
            self.parameters_tablewidget.setItem(row, 2, value_item)
            row += 1

    def dump(self):
        """Returns the json representation of the protocol"""

        parameters = {}
        for i in range(self.parameters_tablewidget.rowCount()):
            parameter_type = self.parameters_tablewidget.item(i, 1).text()
            value = self.parameters_tablewidget.item(i, 2).text()

            if parameter_type == "number":
                value_array = np.fromstring(value, sep=" ")
                if value_array:
                    value = value_array[0]
                else:
                    value = 0

            elif parameter_type == "boolean":
                value = value == "True"

            parameters[self.parameters_tablewidget.item(i, 0).text()] = value

        json_data = {"view": self.view_name_lineedit.text()}
        if parameters:
            json_data["parameters"] = parameters

        return json_data


class ViewsEditor(QWidget):

    dataChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.protocol = None
        self.prefix_path = None

        self.editor_list_widget = EditorListWidget()

        self.add_view_button = QPushButton(self.tr("+"))
        self.add_view_button.setFixedSize(30, 30)

        layout = QVBoxLayout(self)
        layout.addWidget(self.editor_list_widget, 1)
        layout.addWidget(self.add_view_button, 1)

        self.editor_list_widget.dataChanged.connect(self.dataChanged)
        self.add_view_button.clicked.connect(self.__addView)

    @property
    def view_editors(self):
        return self.editor_list_widget.widget_list

    def available_sets(self):
        protocol_template = ProtocolTemplate(self.prefix_path, self.protocol)
        used_sets = [editor.dbset_name for editor in self.view_editors]
        protocol_sets = [set_["name"] for set_ in protocol_template.sets()]
        return [set_ for set_ in protocol_sets if set_ not in used_sets]

    @pyqtSlot()
    def __addView(self):
        """Add a new view"""

        available_sets = self.available_sets()

        name, ok_pressed = QInputDialog.getItem(
            self,
            self.tr("DB set name"),
            self.tr("Name"),
            available_sets,
            editable=False,
        )

        if ok_pressed:
            view_editor = ViewEditor()
            view_editor.dbset_name = name
            self.__add_widget(view_editor)
            self.dataChanged.emit()
            available_sets.pop(available_sets.index(name))
            self.add_view_button.setDisabled(not available_sets)

    @pyqtSlot()
    def __removeView(self):
        """Execute deletion request"""

        self.__remove_widget(self.sender())

    def __remove_widget(self, widget):
        """Removes the widget that which signal triggered this slot"""

        self.editor_list_widget.removeWidget(widget)
        self.add_view_button.setEnabled(True)

    def __add_widget(self, view_editor):
        """Add a new editor widget"""
        self.editor_list_widget.addWidget(view_editor)
        view_editor.deletionRequested.connect(self.__removeView)

    def set_procotol(self, protocol):
        self.protocol = protocol

    def setPrefixPath(self, prefix):
        self.prefix_path = prefix

    def load(self, json_object):
        """Load the json object passed as parameter"""

        for dbset_name, content in json_object.items():
            view_editor = ViewEditor()
            view_editor.setDbSetName(dbset_name)
            view_editor.load(content)
            self.__add_widget(view_editor)

        self.add_view_button.setEnabled(len(self.available_sets()) > 0)

    def dump(self):
        """Returns the json representation of the protocol"""

        return {widget.dbset_name: widget.dump() for widget in self.view_editors}


class ProtocolEditor(QWidget):

    dataChanged = pyqtSignal()
    deletionRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.delete_button, delete_layout = create_delete_button_and_layout()

        self.name_lineedit = QLineEdit()
        self.templateprotocol_label = QLabel()
        self.views_editor = ViewsEditor()

        form_layout = QFormLayout()
        form_layout.addRow(self.tr("Name"), self.name_lineedit)
        form_layout.addRow(self.tr("Template"), self.templateprotocol_label)
        form_layout.addRow(self.tr("Views"), self.views_editor)

        layout = QVBoxLayout(self)
        layout.addLayout(delete_layout)
        layout.addLayout(form_layout)

        self.delete_button.clicked.connect(self.deletionRequested)
        self.name_lineedit.textChanged.connect(self.dataChanged)
        self.views_editor.dataChanged.connect(self.dataChanged)

    @pyqtSlot(str)
    def setName(self, name):
        self.name_lineedit.setText(name)

    def name(self):
        return self.name_lineedit.text()

    name = pyqtProperty(str, fget=name, fset=setName)

    @pyqtSlot(str)
    def setProtocol(self, protocol):
        self.templateprotocol_label.setText(protocol)
        self.views_editor.set_procotol(protocol)

    def protocol(self):
        return self.templateprotocol_label.text()

    protocol = pyqtProperty(str, fget=protocol, fset=setProtocol)

    def setPrefixPath(self, prefix):
        self.views_editor.setPrefixPath(prefix)

    def load(self, json_object):
        """Load the json object passed as parameter"""

        self.name = json_object["name"]
        self.protocol = json_object["template"]
        self.views_editor.load(json_object["views"])

    def dump(self):
        """Returns the json representation of the protocol"""

        return {
            "name": self.name,
            "template": self.protocol,
            "views": self.views_editor.dump(),
        }


class ProtocolDialog(QDialog):
    """Dialog to get necessary info for a new protocol entry"""

    def __init__(self, used_names, protocoltemplate_model, parent=None):
        super().__init__(parent)

        self.used_names = used_names

        self.protocoltemplate_combobox = QComboBox()
        self.protocoltemplate_combobox.setModel(protocoltemplate_model)

        self.name_lineedit = QLineEdit()

        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonbox.button(QDialogButtonBox.Ok).setEnabled(False)

        form_layout = QFormLayout()
        form_layout.addRow(self.tr("Protocol"), self.protocoltemplate_combobox)
        form_layout.addRow(self.tr("Name"), self.name_lineedit)

        layout = QVBoxLayout(self)
        layout.addLayout(form_layout)
        layout.addWidget(self.buttonbox)

        self.name_lineedit.textChanged.connect(self.__validateName)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)

    @pyqtSlot(str)
    def __validateName(self, text):
        """Ensure the name is not empty or already used"""

        self.buttonbox.button(QDialogButtonBox.Ok).setDisabled(
            text == "" or text in self.used_names
        )

    def name(self):
        """Returns the name to use for the protocol"""

        return self.name_lineedit.text()

    def protocol(self):
        """Returns the protocol template to use"""

        return self.protocoltemplate_combobox.currentText()

    @staticmethod
    def getProtocol(parent, used_names, protocoltemplate_model):
        dialog = ProtocolDialog(used_names, protocoltemplate_model, parent)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            return (dialog.name(), dialog.protocol(), True)
        else:
            return (None, None, False)


class DatabaseWidget(QWidget):
    """Widget to edit a database object from at least v2"""

    dataChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.protocoltemplate_model = AssetModel()
        self.protocoltemplate_model.asset_type = AssetType.PROTOCOLTEMPLATE

        self.root_folder = None
        self.prefix_path = None

        self.scroll_widget = ScrollWidget()

        self.add_protocol_button = QPushButton(self.tr("+"))
        self.add_protocol_button.setFixedSize(30, 30)

        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll_widget, 1)
        layout.addWidget(self.add_protocol_button, 1)

        self.scroll_widget.dataChanged.connect(self.dataChanged)
        self.add_protocol_button.clicked.connect(self.__addProtocol)

    @property
    def protocol_editors(self):
        return self.scroll_widget.widget_list

    @pyqtSlot()
    def __onRemoveRequested(self):
        """Remove the widget clicked"""

        self.__remove_widget(self.sender())

    def __remove_widget(self, widget):
        """Removes the widget that which signal triggered this slot"""

        self.scroll_widget.removeWidget(widget)

    def __add_widget(self, protocol_editor):
        """Add the editor to this widget"""

        self.scroll_widget.addWidget(protocol_editor)
        protocol_editor.deletionRequested.connect(self.__onRemoveRequested)

    @pyqtSlot()
    def __addProtocol(self):
        """Add a new protocol to edit"""

        protocol_names = [widgets.name for widgets in self.protocol_editors]

        name, protocol, ok_pressed = ProtocolDialog.getProtocol(
            self, protocol_names, self.protocoltemplate_model
        )

        if ok_pressed:
            protocol_editor = ProtocolEditor()
            protocol_editor.setPrefixPath(self.prefix_path)
            protocol_editor.name = name
            protocol_editor.protocol = protocol

            self.__add_widget(protocol_editor)

    def setPrefixPath(self, prefix):
        """Re-impl"""

        self.prefix_path = prefix
        self.protocoltemplate_model.prefix_path = prefix

    def load(self, json_object):
        """Load the json object passed as parameter"""

        self.blockSignals(True)

        self.scroll_widget.clear()

        self.blockSignals(False)

        self.root_folder = json_object["root_folder"]

        for protocol in json_object["protocols"]:
            protocol_editor = ProtocolEditor()
            protocol_editor.setPrefixPath(self.prefix_path)
            protocol_editor.load(protocol)
            self.__add_widget(protocol_editor)

    def dump(self):
        """Returns the json representation of this database"""

        return {
            "root_folder": self.root_folder,
            "protocols": [widget.dump() for widget in self.scroll_widget.widget_list],
        }

    def asset_models(self):
        """Returns the models used"""

        return [self.protocoltemplate_model]


@frozen
class DatabaseEditor(AbstractAssetEditor):
    def __init__(self, parent=None):
        super().__init__(AssetType.DATABASE, parent)
        self.setObjectName(self.__class__.__name__)
        self.set_title(self.tr("Database"))

        self.database_v1_viewer = DatabaseV1Viewer()
        self.database_widget = DatabaseWidget()

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.database_v1_viewer)
        self.stacked_widget.addWidget(self.database_widget)

        self.layout().addWidget(self.stacked_widget, 1)

        self.database_widget.dataChanged.connect(self.dataChanged)
        self.contextChanged.connect(
            lambda: self.database_widget.setPrefixPath(self.prefix_path)
        )

    def _asset_models(self):
        """Reimpl"""

        return self.database_widget.asset_models()

    def _load_json(self, json_object):
        """Load the json object passed as parameter"""

        self.description_lineedit.setReadOnly(self.schema_version in [1, None])

        if self.schema_version in [1, None]:
            self.set_title(self.tr("Database V1 Read Only"))
            self.database_v1_viewer.load(json_object)
            self.stacked_widget.setCurrentWidget(self.database_v1_viewer)
        else:
            self.set_title(self.tr("Database"))
            self.database_widget.load(json_object)
            self.stacked_widget.setCurrentWidget(self.database_widget)

    def _dump_json(self):
        """Returns the json representation of the asset"""

        return self.stacked_widget.currentWidget().dump()
