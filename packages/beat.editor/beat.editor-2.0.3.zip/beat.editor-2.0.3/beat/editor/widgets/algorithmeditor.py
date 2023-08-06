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

import os
import re

from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QButtonGroup
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from beat.backend.python.algorithm import Algorithm

from ..backend.asset import Asset
from ..backend.asset import AssetType
from ..backend.assetmodel import AssetModel
from ..backend.assetmodel import DataFormatModel
from ..backend.delegates import AssetItemDelegate
from ..decorators import frozen
from .editor import AbstractAssetEditor
from .libraries import LibrariesWidget
from .parameterwidget import ParameterWidget
from .scrollwidget import EditorListWidget
from .scrollwidget import ScrollWidget
from .validatedhelpers import NameItemDelegate
from .validatedhelpers import NameLineEdit

ALGORITHM_TYPE = "algorithm_type"
DEFAULT_SCHEMA_VERSION = 2
DEFAULT_API_VERSION = 2

ALGORITHM_PROCESS_METHOD_MAP = {
    Algorithm.LEGACY: "def process(self, inputs, outputs):",
    Algorithm.SEQUENTIAL: "def process(self, inputs, data_loaders, outputs):",
    Algorithm.AUTONOMOUS: "def process(self, data_loaders, outputs):",
    Algorithm.SEQUENTIAL_LOOP_PROCESSOR: "def process(self, inputs, data_loaders, outputs, channel):",
    Algorithm.AUTONOMOUS_LOOP_PROCESSOR: "def process(self, data_loaders, outputs, channel):",
    Algorithm.SEQUENTIAL_LOOP_EVALUATOR: "def process(self, inputs, data_loaders, outputs, channel):",
    Algorithm.AUTONOMOUS_LOOP_EVALUATOR: "def process(self, data_loaders, outputs, channel):",
}

ANALYZER_PROCESS_METHOD_MAP = {
    "legacy": "def process(self, inputs, output):",
    "sequential": "def process(self, inputs, data_loaders, output):",
    "autonomous": "def process(self, data_loaders, output):",
}

LOOP_VALIDATE_METHOD = "def validate(self, result):"


def migrate_to_api_v2(asset):
    status = asset.type.create_new_version(asset.prefix, asset.name)
    new_asset = None

    if status:
        version_number = int(asset.storage().version) + 1
        name = os.sep.join(asset.name.split(os.sep)[:-1] + [""])
        name += str(version_number)
        new_asset = Asset(asset.prefix, asset.type, name)
        declaration = new_asset.declaration
        declaration["api_version"] = 2
        declaration["schema_version"] = 2
        declaration["type"] = "legacy"
        new_asset.declaration = declaration

    return status, new_asset


def update_code(asset):
    declaration = asset.declaration
    if declaration.get("language") == "python":
        alg_type = declaration.get("type")
        is_analyzer = "results" in declaration

        with open(asset.code_path, "rt") as code_file:
            lines = code_file.readlines()

        process_line = None
        validate_line = None
        for index, line in enumerate(lines):
            if "def process" in line:
                process_line = index

            if "def validate" in line:
                validate_line = index

        if process_line:
            if is_analyzer:
                lines[process_line] = re.sub(
                    r"^(\s*).*(\s*)$",
                    r"\g<1>{}\g<2>".format(ANALYZER_PROCESS_METHOD_MAP[alg_type]),
                    lines[process_line],
                )
            elif alg_type in ALGORITHM_PROCESS_METHOD_MAP:
                lines[process_line] = re.sub(
                    r"^(\s*).*(\s*)$",
                    r"\g<1>{}\g<2>".format(ALGORITHM_PROCESS_METHOD_MAP[alg_type]),
                    lines[process_line],
                )
        elif alg_type != "loop":
            lines.append("    {}\n".format(ALGORITHM_PROCESS_METHOD_MAP[alg_type]))
            lines.append("        pass\n")

        if alg_type == "loop" and not validate_line:
            lines.append("    {}\n".format(LOOP_VALIDATE_METHOD))
            lines.append("        pass\n")

        with open(asset.code_path, "wt") as code_file:
            code_file.write("".join(lines))


class PropertyEditor(QWidget):

    dataChanged = pyqtSignal()
    analyzerStateChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.language = "unknown"
        self.schema_version = DEFAULT_SCHEMA_VERSION
        self.api_version = DEFAULT_API_VERSION

        self.analyzer_checkbox = QCheckBox()
        self.splittable_checkbox = QCheckBox(self.tr("Splittable"))
        self.sequential_radiobutton = QRadioButton(self.tr("Sequential"))
        self.sequential_radiobutton.setProperty(ALGORITHM_TYPE, Algorithm.SEQUENTIAL)
        self.autonomous_radiobutton = QRadioButton(self.tr("Autonomous"))
        self.autonomous_radiobutton.setProperty(ALGORITHM_TYPE, Algorithm.AUTONOMOUS)
        self.sequential_loop_processor_radiobutton = QRadioButton(
            self.tr("Sequential loop processor")
        )
        self.sequential_loop_processor_radiobutton.setProperty(
            ALGORITHM_TYPE, Algorithm.SEQUENTIAL_LOOP_PROCESSOR
        )
        self.autonomous_loop_processor_radiobutton = QRadioButton(
            self.tr("Autonomous loop processor")
        )
        self.autonomous_loop_processor_radiobutton.setProperty(
            ALGORITHM_TYPE, Algorithm.AUTONOMOUS_LOOP_PROCESSOR
        )

        self.sequential_loop_evaluator_radiobutton = QRadioButton(
            self.tr("Sequential loop evaluator")
        )
        self.sequential_loop_evaluator_radiobutton.setProperty(
            ALGORITHM_TYPE, Algorithm.SEQUENTIAL_LOOP_EVALUATOR
        )
        self.autonomous_loop_evaluator_radiobutton = QRadioButton(
            self.tr("Autonomous loop evaluator")
        )
        self.autonomous_loop_evaluator_radiobutton.setProperty(
            ALGORITHM_TYPE, Algorithm.AUTONOMOUS_LOOP_EVALUATOR
        )

        self.button_group = QButtonGroup()
        button_layout = QGridLayout()
        row = 0
        col = 0
        for button in [
            self.sequential_radiobutton,
            self.autonomous_radiobutton,
            self.sequential_loop_processor_radiobutton,
            self.autonomous_loop_processor_radiobutton,
            self.sequential_loop_evaluator_radiobutton,
            self.autonomous_loop_evaluator_radiobutton,
        ]:
            self.button_group.addButton(button)
            button_layout.addWidget(button, row, col)
            col += 1
            if col == 2:
                row += 1
                col = 0

        self.sequential_radiobutton.setChecked(True)

        # button_layout.addStretch(1)

        layout = QFormLayout(self)
        layout.addRow(self.tr("Analyzer:"), self.analyzer_checkbox)
        layout.addRow(self.tr("Type:"), button_layout)
        layout.addRow(self.tr(""), self.splittable_checkbox)

        for widget in [
            self.splittable_checkbox,
            self.sequential_loop_processor_radiobutton,
            self.autonomous_loop_processor_radiobutton,
            self.sequential_loop_evaluator_radiobutton,
            self.autonomous_loop_evaluator_radiobutton,
        ]:
            self.analyzer_checkbox.toggled.connect(
                # target is declared so because otherwise it wouldn't be local
                # to the lambda as it's defined in the outer scope. It will be
                # accessed only when the lambda is called and thus the last value
                # would be used
                #
                # See: https://docs.python.org/3/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result
                lambda checked, target=widget: target.setVisible(not checked)
            )

        self.analyzer_checkbox.toggled.connect(self.analyzerStateChanged)
        self.analyzer_checkbox.toggled.connect(self.__onAnalyzerToggled)

        for widget in self.button_group.buttons() + [
            self.analyzer_checkbox,
            self.splittable_checkbox,
        ]:
            widget.toggled.connect(self.dataChanged)

        self.sequential_loop_evaluator_radiobutton.toggled.connect(
            self.splittable_checkbox.setDisabled
        )
        self.autonomous_loop_evaluator_radiobutton.toggled.connect(
            self.splittable_checkbox.setDisabled
        )

    @pyqtSlot(bool)
    def __onAnalyzerToggled(self, checked):
        if checked:
            if self.button_group.checkedButton() not in [
                self.sequential_radiobutton,
                self.autonomous_radiobutton,
            ]:
                self.sequential_radiobutton.setChecked(True)
        self.splittable_checkbox.setDisabled(checked)

    def isAnalyzer(self):
        return self.analyzer_checkbox.isChecked()

    def hasOutputs(self):
        return not self.analyzer_checkbox.isChecked()

    def hasLoop(self):
        return self.button_group.checkedButton() in [
            self.sequential_loop_processor_radiobutton,
            self.autonomous_loop_processor_radiobutton,
            self.sequential_loop_evaluator_radiobutton,
            self.autonomous_loop_evaluator_radiobutton,
        ]

    def canBeSplitable(self):
        return (
            not self.analyzer_checkbox.isChecked()
            and self.splittable_checkbox.isEnabled()
        )

    def load(self, json_object):
        self.schema_version = json_object.get("schema_version")
        self.api_version = json_object.get("api_version")
        self.language = json_object.get("language")
        self.analyzer_checkbox.setChecked("results" in json_object)
        algorithm_type = json_object.get("type", "legacy")
        for button in self.button_group.buttons():
            if button.property(ALGORITHM_TYPE) == algorithm_type:
                button.setChecked(True)
                break
        self.splittable_checkbox.setChecked(json_object.get("splittable", False))

    def dump(self):
        data = {
            "language": self.language,
            "api_version": self.api_version,
            "type": self.button_group.checkedButton().property(ALGORITHM_TYPE),
        }

        schema_version = self.schema_version
        if self.button_group.checkedButton() in [
            self.sequential_loop_processor_radiobutton,
            self.autonomous_loop_processor_radiobutton,
            self.sequential_loop_evaluator_radiobutton,
            self.autonomous_loop_evaluator_radiobutton,
        ]:
            schema_version = 3

        data["schema_version"] = schema_version

        if self.canBeSplitable():
            data["splittable"] = self.splittable_checkbox.isChecked()

        return data


class DeletableEditor(QWidget):
    """Editor with remove button base class"""

    dataChanged = pyqtSignal()
    deletionRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=None)

        self.delete_button = QPushButton(self.tr("-"))
        self.delete_button.setFixedSize(30, 30)

        delete_layout = QHBoxLayout()
        delete_layout.addStretch(1)
        delete_layout.addWidget(self.delete_button)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(delete_layout)

        self.delete_button.clicked.connect(self.deletionRequested)


class ParameterEditor(DeletableEditor):
    """Editor for a parameter"""

    def __init__(self, parent=None):
        super().__init__(parent=None)

        self.delete_button.setToolTip(self.tr("Remove parameter"))

        self.name_lineedit = NameLineEdit()
        self.parameter_widget = ParameterWidget()

        form_layout = QFormLayout()
        form_layout.addRow(self.tr("Name:"), self.name_lineedit)
        self.layout().addLayout(form_layout)
        self.layout().addWidget(self.parameter_widget)

        self.name_lineedit.textChanged.connect(self.dataChanged)
        self.parameter_widget.dataChanged.connect(self.dataChanged)

    def setName(self, name):
        self.name_lineedit.setText(name)

    def name(self):
        return self.name_lineedit.text()

    def load(self, json_object):
        self.parameter_widget.load(json_object)

    def dump(self):
        return self.parameter_widget.dump()


class ResultEditor(DeletableEditor):
    """Editor for results"""

    def __init__(self, dataformat_model, parent=None):
        super().__init__(parent)

        self.delete_button.setToolTip(self.tr("Remove result"))

        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(dataformat_model)
        proxy_model.setFilterRegExp(
            "(^int32$|^float32$|^bool$|^string$|^system/[a-zA-Z0-9_-]+/[0-9]+$|^plot/[a-zA-Z0-9_-]+/[0-9]+$)"
        )
        self.name_lineedit = NameLineEdit()
        self.type_combobox = QComboBox()
        self.type_combobox.setModel(proxy_model)
        self.display_checkbox = QCheckBox()

        form_layout = QFormLayout()
        form_layout.addRow(self.tr("Name:"), self.name_lineedit)
        form_layout.addRow(self.tr("Type:"), self.type_combobox)
        form_layout.addRow(self.tr("Display by default"), self.display_checkbox)
        self.layout().addLayout(form_layout)

        self.name_lineedit.textChanged.connect(self.dataChanged)
        self.type_combobox.currentTextChanged.connect(self.dataChanged)
        self.display_checkbox.toggled.connect(self.dataChanged)

    def setName(self, name):
        self.name_lineedit.setText(name)

    def name(self):
        return self.name_lineedit.text()

    def load(self, json_object):
        self.type_combobox.setCurrentText(json_object["type"])
        self.display_checkbox.setChecked(json_object["display"])

    def dump(self):
        return {
            "type": self.type_combobox.currentText(),
            "display": self.display_checkbox.isChecked(),
        }


class IOWidget(QGroupBox):
    """Input/Ouput editor"""

    dataChanged = pyqtSignal()

    def __init__(self, title, dataformat_model, parent=None):
        super().__init__(title, parent)

        self.dataformat_model = dataformat_model

        name_delegate = NameItemDelegate(self)
        asset_delegate = AssetItemDelegate(self.dataformat_model, self)

        self.tablewidget = QTableWidget(0, 2)
        self.tablewidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tablewidget.setHorizontalHeaderLabels([self.tr("Name"), self.tr("Type")])
        self.tablewidget.setItemDelegateForColumn(0, name_delegate)
        self.tablewidget.setItemDelegateForColumn(1, asset_delegate)
        self.tablewidget.setMinimumHeight(250)
        self.add_button = QPushButton(self.tr("+"))
        self.add_button.setFixedSize(30, 30)
        self.remove_button = QPushButton(self.tr("-"))
        self.remove_button.setFixedSize(30, 30)
        self.remove_button.setEnabled(False)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        layout = QVBoxLayout(self)
        layout.addWidget(self.tablewidget)
        layout.addLayout(button_layout)

        self.tablewidget.itemChanged.connect(self.dataChanged)
        self.tablewidget.itemSelectionChanged.connect(self.__onSelectionChanged)
        self.add_button.clicked.connect(self.__addRow)
        self.remove_button.clicked.connect(self.__removeRow)

    def __onSelectionChanged(self):
        self.remove_button.setEnabled(bool(self.tablewidget.selectedItems()))

    @pyqtSlot()
    def __addRow(self):
        new_row = self.tablewidget.rowCount()
        self.tablewidget.setRowCount(new_row + 1)
        name_item = QTableWidgetItem(self.tr("Name_me"))
        type_item = QTableWidgetItem(self.dataformat_model.index(0).data())
        self.tablewidget.setItem(new_row, 0, name_item)
        self.tablewidget.setItem(new_row, 1, type_item)
        self.tablewidget.scrollToItem(name_item)

    @pyqtSlot()
    def __removeRow(self):
        selected_items = self.tablewidget.selectedItems()

        rows = []
        while selected_items:
            item = selected_items.pop()
            rows.append(item.row())

        rows = set(sorted(rows))

        while rows:
            row = rows.pop()
            self.tablewidget.removeRow(row)
        self.dataChanged.emit()

    def load(self, json_data):
        self.tablewidget.clearContents()
        self.tablewidget.setRowCount(len(json_data))

        row = 0
        for name, data in json_data.items():
            name_item = QTableWidgetItem(name)
            type_item = QTableWidgetItem(data["type"])
            self.tablewidget.setItem(row, 0, name_item)
            self.tablewidget.setItem(row, 1, type_item)
            row += 1

    def dump(self):
        entries = {
            self.tablewidget.item(i, 0).text(): {
                "type": self.tablewidget.item(i, 1).text()
            }
            for i in range(0, self.tablewidget.rowCount())
        }
        return entries


class GroupEditor(DeletableEditor):
    """Editor for input/output group"""

    def __init__(self, dataformat_model, parent=None):
        super().__init__(parent)

        self.dataformat_model = dataformat_model

        self.delete_button.setToolTip(self.tr("Remove group"))

        self.name_lineedit = QLineEdit()
        self.inputs_widget = IOWidget(self.tr("Inputs"), self.dataformat_model)
        self.inputs_widget.add_button.setToolTip(self.tr("Add input"))
        self.inputs_widget.remove_button.setToolTip(self.tr("Remove input"))
        self.outputs_widget = IOWidget(self.tr("Outputs"), self.dataformat_model)
        self.outputs_widget.add_button.setToolTip(self.tr("Add output"))
        self.outputs_widget.remove_button.setToolTip(self.tr("Remove output"))
        self.unsynchronized_checkbox = QCheckBox(self.tr("Unsynchronized"))
        self.groupbox = QGroupBox()
        self.loop_groupbox = QGroupBox(self.tr("Loop"))
        self.request_combobox = QComboBox()
        self.request_combobox.setModel(dataformat_model)
        self.answer_combobox = QComboBox()
        self.answer_combobox.setModel(dataformat_model)

        groupbox_layout = QHBoxLayout(self.groupbox)
        groupbox_layout.addWidget(self.inputs_widget)
        groupbox_layout.addWidget(self.outputs_widget)
        loop_layout = QFormLayout(self.loop_groupbox)
        loop_layout.addRow(self.tr("Request"), self.request_combobox)
        loop_layout.addRow(self.tr("Answer"), self.answer_combobox)
        self.layout().addWidget(self.name_lineedit)
        self.layout().addWidget(self.groupbox)
        self.layout().addWidget(self.loop_groupbox)
        self.layout().addWidget(self.unsynchronized_checkbox)

        # Only the first group can have outputs
        # and only if not an analyzer
        self.outputs_enabled = True
        # Only the last group can be unsynchronized
        self.unsynchronized_enabled = False
        # If the edited algorithm is of loop or loop_user type
        self.loop_enabled = False

        self.inputs_widget.dataChanged.connect(self.dataChanged)
        self.outputs_widget.dataChanged.connect(self.dataChanged)
        self.unsynchronized_checkbox.toggled.connect(self.dataChanged)
        self.unsynchronized_checkbox.toggled.connect(
            lambda checked: self.name_lineedit.setVisible(not checked)
        )
        self.request_combobox.currentTextChanged.connect(self.dataChanged)
        self.answer_combobox.currentTextChanged.connect(self.dataChanged)

    def setOutputsEnabled(self, enabled):
        self.outputs_enabled = enabled
        self.outputs_widget.setVisible(enabled)

    def setLoopEnabled(self, enabled):
        self.loop_enabled = enabled
        self.loop_groupbox.setVisible(enabled)

    def setUnsynchronizedEnabled(self, enabled):
        self.unsynchronized_enabled = enabled
        self.unsynchronized_checkbox.setChecked(False)
        self.unsynchronized_checkbox.setVisible(enabled)

    def name(self):
        return self.name_lineedit.text()

    def load(self, json_object):
        self.unsynchronized_checkbox.setChecked(False)
        self.name_lineedit.setText(json_object.get("name"))

        inputs = json_object.get("inputs", {})
        self.inputs_widget.load(inputs)
        outputs = json_object.get("outputs", {})
        self.outputs_widget.load(outputs)
        loop = json_object.get("loop")
        if loop:
            self.request_combobox.setCurrentText(loop["request"]["type"])
            self.answer_combobox.setCurrentText(loop["answer"]["type"])

    def dump(self):
        data = {"inputs": self.inputs_widget.dump()}

        name = self.name()
        if name:
            data["name"] = name

        if self.outputs_enabled:
            data["outputs"] = self.outputs_widget.dump()

        if self.loop_enabled:
            data["loop"] = {
                "request": {"type": self.request_combobox.currentText()},
                "answer": {"type": self.answer_combobox.currentText()},
            }

        return data


@frozen
class AlgorithmEditor(AbstractAssetEditor):
    def __init__(self, parent=None):
        super().__init__(AssetType.ALGORITHM, parent)
        self.setObjectName(self.__class__.__name__)
        self.set_title(self.tr("Algorithm"))

        self.property_editor = PropertyEditor()

        self.group_list_widget = EditorListWidget()
        self.add_group_button = QPushButton(self.tr("+"))
        self.add_group_button.setToolTip(self.tr("Add group"))
        self.add_group_button.setFixedSize(30, 30)

        self.parameter_list_widget = EditorListWidget()
        self.add_parameter_button = QPushButton(self.tr("+"))
        self.add_parameter_button.setToolTip(self.tr("Add parameter"))
        self.add_parameter_button.setFixedSize(30, 30)

        self.result_list_widget = EditorListWidget()
        self.add_result_button = QPushButton(self.tr("+"))
        self.add_result_button.setToolTip(self.tr("Add result"))
        self.add_result_button.setFixedSize(30, 30)

        self.dataformat_model = DataFormatModel()

        self.full_dataformat_model = DataFormatModel()
        self.full_dataformat_model.setFullListEnabled(True)

        self.library_model = AssetModel()
        self.library_model.asset_type = AssetType.LIBRARY
        self.libraries_widget = LibrariesWidget()

        # Grouping
        # Groups
        groups_groupbox = QGroupBox(self.tr("Endpoints"))
        groups_layout = QVBoxLayout(groups_groupbox)
        groups_layout.addWidget(self.group_list_widget)
        groups_layout.addWidget(self.add_group_button)

        # Parameters
        self.parameters_groupbox = QGroupBox(self.tr("Parameters"))
        parameters_layout = QVBoxLayout(self.parameters_groupbox)
        parameters_layout.addWidget(self.parameter_list_widget)
        parameters_layout.addWidget(self.add_parameter_button)
        self.parameters_groupbox.setVisible(not self.property_editor.isAnalyzer())

        # Results
        self.results_groupbox = QGroupBox(self.tr("Results"))
        results_layout = QVBoxLayout(self.results_groupbox)
        results_layout.addWidget(self.result_list_widget)
        results_layout.addWidget(self.add_result_button)
        self.results_groupbox.setVisible(self.property_editor.isAnalyzer())

        # Libraries
        libraries_groupbox = QGroupBox(self.tr("Libraries"))
        libraries_layout = QVBoxLayout(libraries_groupbox)
        libraries_layout.addWidget(self.libraries_widget)

        editors_scrollwidget = ScrollWidget()
        editors_scrollwidget.addWidget(groups_groupbox)
        editors_scrollwidget.addWidget(self.parameters_groupbox)
        editors_scrollwidget.addWidget(self.results_groupbox)
        editors_scrollwidget.addWidget(libraries_groupbox)

        self.layout().addWidget(self.property_editor)
        self.layout().addWidget(editors_scrollwidget)

        self.property_editor.dataChanged.connect(self.__updateUI)
        self.property_editor.analyzerStateChanged.connect(self.__updateUI)
        self.group_list_widget.dataChanged.connect(self.dataChanged)
        self.parameter_list_widget.dataChanged.connect(self.dataChanged)
        self.result_list_widget.dataChanged.connect(self.dataChanged)
        self.libraries_widget.dataChanged.connect(self.dataChanged)
        self.contextChanged.connect(self.__onContextChanged)
        self.add_group_button.clicked.connect(self.__onAddGroup)
        self.add_parameter_button.clicked.connect(self.__onAddParameter)
        self.add_result_button.clicked.connect(self.__onAddResult)

    def __get_free_name(self, widget_list):
        name = "Change_Me"
        i = 1
        restart = True
        while restart:
            for widget in widget_list:
                if widget.name() == name:
                    name = f"Change_Me_{i}"
                    i += 1
                    break
            else:
                restart = False
        return name

    def __updateUI(self):
        group_count = len(self.group_list_widget.widget_list)
        for widget in self.group_list_widget.widget_list:
            widget.setOutputsEnabled(False)
            widget.setUnsynchronizedEnabled(False)

        if group_count >= 1:
            first_widget = self.group_list_widget.widget_list[0]
            first_widget.setOutputsEnabled(self.property_editor.hasOutputs())
            first_widget.setLoopEnabled(self.property_editor.hasLoop())

        if group_count > 1:
            last_widget = self.group_list_widget.widget_list[-1]
            last_widget.setUnsynchronizedEnabled(True)

        is_analyzer = self.property_editor.isAnalyzer()
        self.results_groupbox.setVisible(is_analyzer)
        self.parameters_groupbox.setVisible(not is_analyzer)

        if is_analyzer:
            if not self.result_list_widget.widget_list:
                self.__onAddResult()

        self.dataChanged.emit()

    @pyqtSlot()
    def __onContextChanged(self):
        self.dataformat_model.setPrefixPath(self.prefix_path)
        self.full_dataformat_model.setPrefixPath(self.prefix_path)
        self.library_model.setPrefixPath(self.prefix_path)

    @pyqtSlot()
    def __onAddGroup(self):
        name = self.__get_free_name(self.group_list_widget.widget_list)
        self.__addGroup({"name": name})

    @pyqtSlot()
    def __onAddParameter(self):
        name = self.__get_free_name(self.parameter_list_widget.widget_list)
        self.__addParameter(name)

    @pyqtSlot()
    def __onAddResult(self):
        name = self.__get_free_name(self.result_list_widget.widget_list)
        self.__addResult(name)

    @pyqtSlot()
    def __onRemoveGroup(self):
        self.group_list_widget.removeWidget(self.sender())
        self.__updateUI()

    @pyqtSlot()
    def __onRemoveParameter(self):
        self.parameter_list_widget.removeWidget(self.sender())

    @pyqtSlot()
    def __onRemoveResult(self):
        self.result_list_widget.removeWidget(self.sender())

    def __addGroup(self, configuration={}):
        editor = GroupEditor(self.dataformat_model)
        if configuration:
            editor.load(configuration)
        editor.deletionRequested.connect(self.__onRemoveGroup)
        self.group_list_widget.addWidget(editor)
        self.__updateUI()

    def __addParameter(self, name, configuration={}):
        editor = ParameterEditor()
        editor.setName(name)
        if configuration:
            editor.load(configuration)
        editor.deletionRequested.connect(self.__onRemoveParameter)
        self.parameter_list_widget.addWidget(editor)

    def __addResult(self, name, configuration={}):
        editor = ResultEditor(self.full_dataformat_model)
        editor.setName(name)
        if configuration:
            editor.load(configuration)
        editor.deletionRequested.connect(self.__onRemoveResult)
        self.result_list_widget.addWidget(editor)

    def _asset_models(self):
        """Reimpl"""

        return [self.dataformat_model, self.full_dataformat_model, self.library_model]

    def _load_json(self, json_object):
        """Load the json object passed as parameter"""

        self.property_editor.load(json_object)
        for widget in [
            self.group_list_widget,
            self.parameter_list_widget,
            self.result_list_widget,
        ]:
            widget.clear()

        results = json_object.get("results", {})
        for name, configuration in results.items():
            self.__addResult(name, configuration)

        groups = json_object.get("groups", [])
        for group in groups:
            self.__addGroup(group)

        parameters = json_object.get("parameters", {})
        for name, configuration in parameters.items():
            self.__addParameter(name, configuration)

        self.libraries_widget.set_available_libraries(self.library_model.stringList())
        self.libraries_widget.set_used_libraries(json_object.get("uses", {}))

    def _dump_json(self):
        """Returns the json representation of the asset"""

        data = {}
        data.update(self.property_editor.dump())

        data["groups"] = [
            widget.dump() for widget in self.group_list_widget.widget_list
        ]

        if (
            not self.property_editor.isAnalyzer()
            and self.parameter_list_widget.widget_list
        ):
            data["parameters"] = {}
            for widget in self.parameter_list_widget.widget_list:
                data["parameters"][widget.name()] = widget.dump()

        if self.property_editor.isAnalyzer() and self.result_list_widget.widget_list:
            data["results"] = {}
            for widget in self.result_list_widget.widget_list:
                data["results"][widget.name()] = widget.dump()

        libraries = self.libraries_widget.get_used_libraries()
        if libraries:
            data["uses"] = libraries

        return data
