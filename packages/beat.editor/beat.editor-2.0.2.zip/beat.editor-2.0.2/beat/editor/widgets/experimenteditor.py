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

import copy
import os

import numpy as np
import simplejson as json

from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from beat.backend.python.algorithm import Algorithm
from beat.core.experiment import EVALUATOR_PREFIX
from beat.core.experiment import PROCESSOR_PREFIX

from ..backend.asset import Asset
from ..backend.asset import AssetType
from ..backend.assetmodel import AssetModel
from ..backend.resourcemodels import AlgorithmResourceModel
from ..backend.resourcemodels import QueueResourceModel
from ..backend.resourcemodels import experiment_resources
from ..decorators import frozen
from ..utils import is_Qt_equal_or_higher
from .dialogs import AssetCreationDialog
from .editor import AbstractAssetEditor
from .scrollwidget import EditorListWidget
from .scrollwidget import ScrollWidget
from .spinboxes import NumpySpinBox

PARAMETER_TYPE_KEY = "parameter_type"
DEFAULT_VALUE_KEY = "default_value"
EDITED_KEY = "edited"


# ------------------------------------------------------------------------------
# Helper methods


def typed_user_property(widget):
    """Returns the user property value properly typed

    :param widget QWidget: widget from which the property value must be retrieved
    """

    user_property = widget.metaObject().userProperty()
    parameter_type = widget.property(PARAMETER_TYPE_KEY)
    return np.array([user_property.read(widget)]).astype(parameter_type)[0]


def write_user_property(widget, value):
    """Write the widget user property value

    :param widget QWidget: widget to which the property value must be written
    :param value: value to write to the user property
    """

    user_property = widget.metaObject().userProperty()
    user_property.write(widget, value)


# ------------------------------------------------------------------------------
# Helper classes


class EnvironmentModel(QStandardItemModel):
    """Model wrapping the processing environment available"""

    def __init__(self, parent=None):
        super().__init__(4, 0, parent)

        self.context = None

    @pyqtSlot()
    def refreshContent(self):
        self.clear()
        if self.context is not None:

            def add_row(type_, data):
                visual_name = "{name} ({version})".format(**data)
                icon = QIcon(f":/resources/{type_}")
                self.appendRow(
                    [
                        QStandardItem(icon, visual_name),
                        QStandardItem(data["name"]),
                        QStandardItem(data["version"]),
                        QStandardItem(type_),
                    ]
                )

            with open(self.context.meta["environments"], "rt") as file_:
                json_data = json.load(file_)
                remote_data = json_data.get("remote", {})
                for data in remote_data:
                    add_row("remote", data)

                docker_data = json_data.get("docker", {})
                for _, data in docker_data.items():
                    if "databases" not in data:
                        add_row("docker", data)

    def setContext(self, context):
        self.context = context
        self.refreshContent()

    def environment(self, index):
        """Returns the (name, version) tuple representing an environment

        :param index QModelIndex: index from the model
        """

        if is_Qt_equal_or_higher("5.11"):
            name = index.siblingAtColumn(1)
            version = index.siblingAtColumn(2)
        else:
            name = index.sibling(index.row(), 1)
            version = index.sibling(index.row(), 2)

        name = self.data(name)
        version = self.data(version)
        return {"name": name, "version": version}

    def environmentType(self, index):
        if is_Qt_equal_or_higher("5.11"):
            type_ = index.siblingAtColumn(3)
        else:
            type_ = index.sibling(index.row(), 3)

        return self.data(type_)


class ContainerWidget(ScrollWidget):
    """Container widget to show block editors"""

    def dump(self):
        return {widget.block_name: widget.dump() for widget in self.widget_list}


class AbstractBaseEditor(QWidget):

    dataChanged = pyqtSignal()
    prefixPathChanged = pyqtSignal(str)

    def __init__(self, prefix_path, parent=None):
        super().__init__(parent)

        self.prefix_path = prefix_path
        self.error_label = QLabel(self)
        icon = self.style().standardIcon(QStyle.SP_MessageBoxWarning)
        self.error_label.setPixmap(icon.pixmap(32, 32, QIcon.Normal, QIcon.On))
        layout = QVBoxLayout(self)
        layout.addWidget(self.error_label)
        self.setErrors([])

    def setErrors(self, errors):
        if errors:
            self.error_label.setVisible(True)
            self.error_label.setToolTip("\n".join(errors))
        else:
            self.error_label.setVisible(False)
            self.error_label.setToolTip("")

    @pyqtSlot(str)
    def setPrefixPath(self, prefix_path):
        if self.prefix_path == prefix_path:
            return

        self.prefix_path = prefix_path
        self.prefixPathChanged.emit(self.prefix_path)

    def load(self, json_object):
        raise NotImplementedError

    def dump(self):
        raise NotImplementedError


class DatasetModel(QStringListModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.outputs = []

    def reload(self):
        asset_model = AssetModel()
        asset_model.asset_type = AssetType.DATABASE
        asset_model.prefix_path = self.prefix_path
        asset_model.setLatestOnlyEnabled(False)

        available_databases = asset_model.stringList()
        available_set_names = []

        for database in available_databases:
            db = AssetType.DATABASE.klass(self.prefix_path, database)
            if not db.valid:
                continue
            for protocol in db.protocol_names:
                for set_name, set_data in db.sets(protocol).items():
                    if (
                        self.outputs
                        and list(set_data["outputs"].keys()) != self.outputs
                    ):
                        continue

                    available_set_names.append(
                        "{}/{}/{}".format(database, protocol, set_name)
                    )

        self.setStringList(available_set_names)

    def setPrefixPath(self, prefix_path):
        self.prefix_path = prefix_path
        self.reload()

    def setupOuputFilter(self, output_filter):
        self.outputs = output_filter
        self.reload()


# ------------------------------------------------------------------------------


# Editors


class IOMapperDialog(QDialog):
    """Dialog that allows to remap inputs and outputs of an algorithm to fit on
    a block of the toolchain
    """

    def __init__(self, algorithm, block_data, parent=None):
        super().__init__(parent)
        alg_inputs = []
        alg_outputs = []
        for group in algorithm["groups"]:
            alg_inputs += group["inputs"].keys()
            outputs = group.get("outputs")
            if outputs:
                alg_outputs += outputs.keys()

        self.inputs_layout = QFormLayout()
        for alg_input, input_ in block_data["inputs"].items():
            combobox = QComboBox()
            combobox.addItems(alg_inputs)
            combobox.setCurrentText(alg_input)
            self.inputs_layout.addRow(input_, combobox)

        inputs_groupbox = QGroupBox(self.tr("Inputs"))
        inputs_groupbox.setLayout(self.inputs_layout)
        groupboxes_layout = QHBoxLayout()
        groupboxes_layout.addWidget(inputs_groupbox)

        self.outputs_layout = QFormLayout()

        outputs = block_data.get("outputs")
        if outputs:
            for alg_output, output in outputs.items():
                combobox = QComboBox()
                combobox.addItems(alg_outputs)
                combobox.setCurrentText(alg_output)
                self.outputs_layout.addRow(output, combobox)

            outputs_groupbox = QGroupBox(self.tr("Outputs"))
            outputs_groupbox.setLayout(self.outputs_layout)
            groupboxes_layout.addWidget(outputs_groupbox)

        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        layout = QVBoxLayout(self)
        layout.addLayout(groupboxes_layout)
        layout.addWidget(buttonbox)

        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)

    def ioMapping(self):
        data = {"inputs": {}}

        for i in range(self.inputs_layout.rowCount()):
            label = self.inputs_layout.itemAt(i, QFormLayout.LabelRole).widget()
            combobox = self.inputs_layout.itemAt(i, QFormLayout.FieldRole).widget()
            data["inputs"][combobox.currentText()] = label.text()

        for i in range(self.outputs_layout.rowCount()):
            if "outputs" not in data:
                data["outputs"] = {}
            label = self.outputs_layout.itemAt(i, QFormLayout.LabelRole).widget()
            combobox = self.outputs_layout.itemAt(i, QFormLayout.FieldRole).widget()
            data["outputs"][combobox.currentText()] = label.text()

        return data

    @staticmethod
    def getIOMapping(prefix, block_data):
        algorithm = Asset(prefix, AssetType.ALGORITHM, block_data["algorithm"])

        dialog = IOMapperDialog(algorithm.declaration, block_data)
        status = dialog.exec_()
        if status == QDialog.Rejected:
            return False, None

        return True, dialog.ioMapping()


class DatasetEditor(AbstractBaseEditor):
    """Widget allowing the setup of the various datasets used"""

    datasetChanged = pyqtSignal(str)

    def __init__(self, block_name, prefix_path, parent=None):
        super().__init__(prefix_path, parent)

        self.json_object = {}
        self.block_name = block_name
        self.dataset_model = DatasetModel()
        self.dataset_model.setPrefixPath(prefix_path)
        self.dataset_combobox = QComboBox()
        self.dataset_combobox.setModel(self.dataset_model)
        self.reset_button = QPushButton(
            self.style().standardIcon(QStyle.SP_DialogResetButton), ""
        )
        self.reset_button.setToolTip(self.tr("Reset values"))

        row_layout = QHBoxLayout()
        row_layout.addWidget(self.dataset_combobox, 1)
        row_layout.addWidget(self.reset_button)

        layout = QFormLayout()
        layout.addRow(self.block_name, row_layout)
        self.layout().addLayout(layout)

        self.dataset_combobox.currentTextChanged.connect(self.dataChanged)
        self.dataset_combobox.currentTextChanged.connect(self.datasetChanged)
        self.reset_button.clicked.connect(self.reset)

    def reset(self):
        dataset_name = "{}/{}/{}".format(
            self.json_object["database"],
            self.json_object["protocol"],
            self.json_object["set"],
        )
        self.dataset_combobox.setCurrentText(dataset_name)

        if self.dataset_combobox.currentText() != dataset_name:
            self.dataset_combobox.setCurrentIndex(-1)

    def loadToolchainData(self, toolchain):
        asset = AssetType.TOOLCHAIN.klass(self.prefix_path, toolchain)
        outputs = []
        if asset.valid:
            outputs = asset.datasets[self.block_name]["outputs"]

        current_dataset = self.dataset_combobox.currentText()

        #  Avoid emitting signals while updating the filter as the current
        #  entry will be invalidated.
        self.dataset_combobox.blockSignals(True)
        self.dataset_model.setupOuputFilter(outputs)
        self.dataset_combobox.setCurrentText(current_dataset)
        self.dataset_combobox.blockSignals(False)

    def currentSet(self):
        _, _, _, set_ = self.dataset_combobox.currentText().split("/")
        return set_

    def load(self, json_object):
        self.json_object = copy.deepcopy(json_object)
        self.reset()

    def dump(self):
        current_dataset = self.dataset_combobox.currentText()
        try:
            database, db_version, protocol, set_ = current_dataset.split("/")
        except ValueError:
            database = None
            db_version = None
            protocol = None
            set_ = None

        return {
            "database": "{}/{}".format(database, db_version),
            "protocol": protocol,
            "set": set_,
        }


class AlgorithmParametersEditor(AbstractBaseEditor):

    dataChanged = pyqtSignal()
    parameterCountChanged = pyqtSignal(int)

    def __init__(self, prefix_path, parent=None):
        super().__init__(prefix_path, parent)

        self.algorithm_name = None
        self.json_data = {}
        self.edited = {}
        self.dump_edited_only = True
        self.form_layout = QFormLayout()
        self.layout().addLayout(self.form_layout)

    def setDumpEditOnlyEnabled(self, enabled):
        """Sets whether the dump will contain all or only the modified fields"""

        self.dump_edited_only = enabled

    def isEmpty(self):
        """Returns whether this editor is empty"""

        return self.form_layout.rowCount() == 0

    def parameterCount(self):
        """Returns the number of parameters to edit"""

        return self.form_layout.rowCount()

    def editorForRow(self, row):
        """Returns the editor widget matching the give row"""

        if row < 0 or row >= self.form_layout.rowCount():
            return None

        return self.form_layout.itemAt(row, QFormLayout.FieldRole).widget()

    def labelForRow(self, row):
        """Returns the label widget matching the give row"""

        if row < 0 or row >= self.form_layout.rowCount():
            return None

        return self.form_layout.itemAt(row, QFormLayout.LabelRole).widget().text()

    def editorForLabel(self, label):
        """Returns the editor matching the given label"""

        for i in range(self.form_layout.rowCount()):
            if self.labelForRow(i) == label:
                return self.editorForRow(i)

    def setup(self, algorithm_name):
        """Setup the editor for the give algorithm"""

        if self.algorithm_name == algorithm_name:
            return

        self.algorithm_name = algorithm_name
        old_count = self.parameterCount()

        while self.form_layout.rowCount():
            self.form_layout.removeRow(0)

        if not algorithm_name:
            self.parameterCountChanged.emit(0)
            return

        algorithm = AssetType.ALGORITHM.klass(self.prefix_path, self.algorithm_name)
        parameters = algorithm.parameters
        if parameters is not None:
            for name, info in parameters.items():
                type_ = np.dtype(info["type"])
                default = info.get("default")

                if np.issubdtype(type_, np.number):
                    if "choice" in info:
                        editor = QComboBox()
                        signal = editor.currentTextChanged
                        editor.addItems([str(value) for value in info["choice"]])
                        editor.setCurrentText(str(default))
                    else:
                        editor = NumpySpinBox(type_.type)
                        signal = editor.valueChanged
                        if "range" in info:
                            range_ = info["range"]
                            editor.setRange(range_[0], range_[1])
                        editor.setValue(default)
                elif np.issubdtype(type_, np.dtype(str).type):
                    if "choice" in info:
                        editor = QComboBox()
                        signal = editor.currentTextChanged
                        editor.addItems(info["choice"])
                        editor.setCurrentText(str(default))
                    else:
                        editor = QLineEdit()
                        signal = editor.textChanged
                        editor.setText(default)

                elif np.issubdtype(type_, np.dtype(bool).type):
                    editor = QCheckBox()
                    signal = editor.toggled
                    editor.setChecked(bool(default))
                else:
                    raise RuntimeError("Unsupported type: {}".format(type_))

                signal.connect(self.dataChanged)
                signal.connect(lambda: self.sender().setProperty(EDITED_KEY, True))
                editor.setProperty(PARAMETER_TYPE_KEY, type_)
                editor.setProperty(DEFAULT_VALUE_KEY, default)
                editor.setProperty(EDITED_KEY, False)

                self.form_layout.addRow(name, editor)

        new_count = self.parameterCount()
        if new_count != old_count:
            self.parameterCountChanged.emit(new_count)

    def reset(self):
        """Reset the state of the editor all default values"""

        for i in range(self.form_layout.rowCount()):
            widget = self.form_layout.itemAt(i, QFormLayout.FieldRole).widget()
            widget.setProperty(EDITED_KEY, False)
            default = widget.property(DEFAULT_VALUE_KEY)
            write_user_property(widget, default)

    def load(self, json_data):
        """Setup the content of the editor with the given JSON data"""

        self.json_data = copy.deepcopy(json_data)

        for name, value in json_data.items():
            for i in range(self.form_layout.rowCount()):
                label = self.form_layout.itemAt(i, QFormLayout.LabelRole).widget()
                if label.text() == name:
                    widget = self.form_layout.itemAt(i, QFormLayout.FieldRole).widget()
                    write_user_property(widget, value)
                    break

    def dump(self):
        """Dump only the parameters that have changed unless dump edited only
        is set.
        """

        data = {}
        for i in range(0, self.form_layout.rowCount()):
            label = self.form_layout.itemAt(i, QFormLayout.LabelRole).widget()
            name = label.text()

            widget = self.form_layout.itemAt(i, QFormLayout.FieldRole).widget()
            value = typed_user_property(widget)
            if self.dump_edited_only:
                default_value = widget.property(DEFAULT_VALUE_KEY)
                if widget.property(EDITED_KEY) and value != default_value:
                    data[name] = value
            else:
                data[name] = value
        return data


class ExecutionPropertiesEditor(AbstractBaseEditor):
    """Widget showing the execution parameters related to an execution unit"""

    algorithmChanged = pyqtSignal(str)

    def __init__(self, prefix_path, parent=None):
        super().__init__(prefix_path, parent)

        self.json_object = {}
        self.io_mapping = {}
        self.environment_changed = False
        self.queue_changed = False
        self._queue_enabled = True
        self.parameter_item = None
        self.algorithm_model = None
        self.queue_model = QueueResourceModel()
        self.algorithm_combobox = QComboBox()
        self.algorithm_combobox.setObjectName("algorithms")
        self.environment_combobox = QComboBox()
        self.environment_combobox.setObjectName("environments")
        self.queue_combobox = QComboBox()
        self.queue_combobox.setModel(self.queue_model)
        self.parameters_editor = AlgorithmParametersEditor(prefix_path)

        self.remap_button = QPushButton(QIcon(":/resources/remap"), "")
        self.remap_button.setObjectName("remap")
        self.remap_button.setToolTip(self.tr("Remap input and outputs"))
        reset_button = QPushButton(
            self.style().standardIcon(QStyle.SP_DialogResetButton), ""
        )
        reset_button.setToolTip(self.tr("Reset values"))
        self.parameters_button = QPushButton(self.tr("Parameters"))
        self.parameters_button.setCheckable(True)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.parameters_button)
        button_layout.addStretch(1)
        button_layout.addWidget(self.remap_button)
        button_layout.addWidget(reset_button)

        groupbox = QGroupBox()
        groupbox.setVisible(False)
        self.parameters_layout = QFormLayout(groupbox)
        self.parameters_layout.addRow(self.tr("Environment"), self.environment_combobox)
        self.parameters_layout.addRow(self.tr("Queue"), self.queue_combobox)
        self.parameters_layout.addRow(self.tr("Parameters"), self.parameters_editor)

        layout = self.layout()
        layout.addWidget(self.algorithm_combobox)
        layout.addLayout(button_layout)
        layout.addWidget(groupbox)

        self.algorithm_combobox.currentIndexChanged.connect(self.dataChanged)
        self.algorithm_combobox.currentTextChanged.connect(self.__onAlgorithmChanged)
        self.environment_combobox.currentIndexChanged.connect(self.dataChanged)
        self.environment_combobox.currentIndexChanged.connect(
            lambda *args: setattr(self, "environment_changed", True)
        )
        self.environment_combobox.currentIndexChanged.connect(
            self.__onEnvironmentChanged
        )
        self.queue_combobox.currentIndexChanged.connect(self.dataChanged)
        self.queue_combobox.currentIndexChanged.connect(
            lambda *args: setattr(self, "queue_changed", True)
        )
        self.parameters_editor.dataChanged.connect(self.dataChanged)
        self.parameters_editor.parameterCountChanged.connect(self.__updateUi)
        self.remap_button.clicked.connect(self.__remapIO)
        reset_button.clicked.connect(lambda: self.load(self.json_object))
        self.parameters_button.toggled.connect(self.__updateUi)
        self.parameters_button.toggled.connect(groupbox.setVisible)

        self.__updateUi()

    @pyqtSlot()
    def __remapIO(self):

        status, mapping = IOMapperDialog.getIOMapping(self.prefix_path, self.dump())

        if status and self.io_mapping != mapping:
            self.io_mapping = mapping
            self.dataChanged.emit()

    @pyqtSlot()
    def __updateUi(self):
        icon = (
            QStyle.SP_TitleBarShadeButton
            if self.parameters_button.isChecked()
            else QStyle.SP_TitleBarUnshadeButton
        )
        self.parameters_button.setIcon(self.style().standardIcon(icon))

        self.parameters_editor.setVisible(not self.parameters_editor.isEmpty())
        self.parameters_layout.labelForField(self.parameters_editor).setVisible(
            not self.parameters_editor.isEmpty()
        )

        self.queue_combobox.setVisible(self._queue_enabled)
        self.parameters_layout.labelForField(self.queue_combobox).setVisible(
            self._queue_enabled
        )

    @pyqtSlot(int)
    def __onEnvironmentChanged(self, row):
        model = self.environment_combobox.model()
        index = model.index(row, 0)

        self.queue_model.setEnvironment(**model.environment(index))
        self.queue_model.setType(model.environmentType(index))
        self.queue_combobox.setCurrentIndex(0)

    @pyqtSlot(str)
    def __onAlgorithmChanged(self, algorithm_name):

        if not algorithm_name or not self.json_object:
            return

        # redo the io mapping

        asset = Asset(self.prefix_path, AssetType.ALGORITHM, algorithm_name)
        declaration = asset.declaration

        inputs = []
        outputs = []
        for group in declaration["groups"]:
            inputs += group.get("inputs", [])
            outputs += group.get("outputs", [])

        #  The key is the algorithm IO name and the value is toolchain IO name
        io_mapping = {}
        if sorted(inputs) != sorted(self.io_mapping["inputs"].keys()):
            io_mapping = {"inputs": {}}
            for key, value in zip(inputs, self.io_mapping["inputs"].values()):
                io_mapping["inputs"][key] = value

        outputs_mapping = self.io_mapping.get("outputs", {})
        if outputs and sorted(outputs) != sorted(outputs_mapping.keys()):
            io_mapping["outputs"] = {}
            for key, value in zip(outputs, outputs_mapping.values()):
                io_mapping["outputs"][key] = value

        if io_mapping:
            self.io_mapping = io_mapping

        self.algorithmChanged.emit(algorithm_name)

    def algorithm(self):
        return self.algorithm_combobox.currentText()

    algorithm = pyqtProperty(str, fget=algorithm, notify=algorithmChanged)

    def setAlgorithmResourceModel(self, model):
        self.algorithm_model = model
        self.algorithm_combobox.setModel(self.algorithm_model)

    def setEnvironmentModel(self, model):
        self.environment_combobox.setModel(model)

    def environmentModel(self):
        return self.environment_combobox.model()

    def setQueueEnabled(self, enabled):
        self._queue_enabled = enabled
        self.__updateUi()

    def load(self, json_object):
        self.json_object = copy.deepcopy(json_object)
        inputs = json_object.get("inputs", {})

        self.io_mapping = {"inputs": inputs}

        outputs = json_object.get("outputs", {})
        if outputs:
            self.io_mapping["outputs"] = outputs

        self.algorithm_model.setInputCount(len(inputs))
        self.algorithm_model.setOutputCount(len(outputs))

        algorithm_name = json_object["algorithm"]
        environment = json_object.get("environment")
        parameters = json_object.get("parameters")

        if algorithm_name:
            self.algorithm_combobox.setCurrentText(algorithm_name)
            if self.algorithm_combobox.currentText() != algorithm_name:
                available_algorithms = "\n".join(
                    self.algorithm_model.index(i, 0).data()
                    for i in range(self.algorithm_model.rowCount())
                )
                raise RuntimeError(
                    "Algorithm {} not available in list:\n {}".format(
                        algorithm_name, available_algorithms
                    )
                )
            self.parameters_editor.setup(algorithm_name)

        if environment:
            env_text = "{} ({})".format(environment["name"], environment["version"])
            self.environment_combobox.setCurrentText(env_text)
        else:
            self.environment_combobox.setCurrentIndex(0)

        if parameters:
            self.parameters_editor.load(parameters)

        self.environment_changed = False
        self.queue_changed = False
        self.parameters_changed = False

    def dump(self):
        data = copy.deepcopy(self.json_object)
        data["algorithm"] = self.algorithm_combobox.currentText()

        if self.environment_changed:
            model = self.environment_combobox.model()
            index = model.index(self.environment_combobox.currentIndex(), 0)
            data["environment"] = model.environment(index)

        if self._queue_enabled and self.queue_changed:
            data["queue"] = self.queue_combobox.currentText()

        parameters = self.parameters_editor.dump()
        if parameters:
            data["parameters"] = parameters

        data.update(self.io_mapping)
        return data


class AbstractBlockEditor(AbstractBaseEditor):
    """Common elements for editing a block"""

    algorithmChanged = pyqtSignal(str)

    def __init__(self, block_name, prefix_path, parent=None):
        super().__init__(prefix_path, parent)

        self.block_name = block_name

    def setAlgorithmResourceModel(self, model):
        """Set algorithm model"""

        raise NotImplementedError

    def setEnvironmentModel(self, model):
        """Set environment model"""

        raise NotImplementedError


class BlockEditor(AbstractBlockEditor):
    def __init__(self, block_name, prefix_path, parent=None):
        super().__init__(block_name, prefix_path, parent)

        self.algorithm_model = AlgorithmResourceModel()
        self.algorithm_model.setAnalyzerEnabled(False)
        self.algorithm_model.setTypes(
            [Algorithm.LEGACY, Algorithm.SEQUENTIAL, Algorithm.AUTONOMOUS]
        )

        self.properties_editor = ExecutionPropertiesEditor(prefix_path)
        self.properties_editor.setAlgorithmResourceModel(self.algorithm_model)

        layout = self.layout()
        layout.addWidget(QLabel(self.block_name))
        layout.addWidget(self.properties_editor)

        self.properties_editor.algorithmChanged.connect(self.algorithmChanged)
        self.properties_editor.dataChanged.connect(self.dataChanged)

        self.prefixPathChanged.connect(self.algorithm_model.update)

    def selectedAlgorithm(self):
        return self.properties_editor.algorithm

    def setEnvironmentModel(self, model):
        self.properties_editor.setEnvironmentModel(model)

    def environmentModel(self):
        return self.properties_editor.environmentModel()

    def load(self, json_object):
        self.properties_editor.load(json_object)

    def dump(self):
        return self.properties_editor.dump()


class AnalyzerBlockEditor(BlockEditor):
    def __init__(self, block_name, prefix_path, parent=None):
        super().__init__(block_name, prefix_path, parent)

        self.algorithm_model.setAnalyzerEnabled(True)


class LoopBlockEditor(AbstractBlockEditor):
    def __init__(self, block_name, prefix_path, parent=None):
        super().__init__(block_name, prefix_path, parent)

        self.processor_model = AlgorithmResourceModel()
        self.processor_model.setAnalyzerEnabled(False)
        self.processor_model.setTypes(
            [Algorithm.AUTONOMOUS_LOOP_PROCESSOR, Algorithm.SEQUENTIAL_LOOP_PROCESSOR]
        )

        self.evaluator_model = AlgorithmResourceModel()
        self.evaluator_model.setAnalyzerEnabled(False)
        self.evaluator_model.setTypes(
            [Algorithm.AUTONOMOUS_LOOP_EVALUATOR, Algorithm.SEQUENTIAL_LOOP_EVALUATOR]
        )

        self.processor_properties_editor = ExecutionPropertiesEditor(prefix_path)
        self.processor_properties_editor.setAlgorithmResourceModel(self.processor_model)
        self.evaluator_properties_editor = ExecutionPropertiesEditor(prefix_path)
        self.evaluator_properties_editor.setAlgorithmResourceModel(self.evaluator_model)
        self.evaluator_properties_editor.setQueueEnabled(False)

        processor_groupbox = QGroupBox(self.tr("Processor"))
        evaluator_groupbox = QGroupBox(self.tr("Evaluator"))

        processor_layout = QVBoxLayout(processor_groupbox)
        processor_layout.addWidget(self.processor_properties_editor)

        evaluator_layout = QVBoxLayout(evaluator_groupbox)
        evaluator_layout.addWidget(self.evaluator_properties_editor)

        layout = self.layout()
        layout.addWidget(QLabel(self.block_name))
        layout.addWidget(processor_groupbox)
        layout.addWidget(evaluator_groupbox)

        self.processor_properties_editor.algorithmChanged.connect(self.algorithmChanged)
        self.processor_properties_editor.dataChanged.connect(self.dataChanged)
        self.evaluator_properties_editor.algorithmChanged.connect(self.algorithmChanged)
        self.evaluator_properties_editor.dataChanged.connect(self.dataChanged)

        self.prefixPathChanged.connect(self.processor_model.update)
        self.prefixPathChanged.connect(self.evaluator_model.update)

    def selectedAlgorithms(self):
        return {
            self.processor_properties_editor.algorithm,
            self.evaluator_properties_editor.algorithm,
        }

    def setEnvironmentModel(self, model):
        for editor in [
            self.processor_properties_editor,
            self.evaluator_properties_editor,
        ]:
            editor.setEnvironmentModel(model)

    def environmentModel(self):
        return self.processor_properties_editor.environmentModel()

    def load(self, json_object):
        processor_data = {
            key[len(PROCESSOR_PREFIX) :]: value
            for key, value in json_object.items()
            if key.startswith(PROCESSOR_PREFIX)
        }
        evaluator_data = {
            key[len(EVALUATOR_PREFIX) :]: value
            for key, value in json_object.items()
            if key.startswith(EVALUATOR_PREFIX)
        }

        self.processor_properties_editor.load(processor_data)
        self.evaluator_properties_editor.load(evaluator_data)

    def dump(self):
        data = {}
        processor_data = self.processor_properties_editor.dump()
        data.update(
            {f"{PROCESSOR_PREFIX}{key}": value for key, value in processor_data.items()}
        )
        evaluator_data = self.evaluator_properties_editor.dump()
        data.update(
            {f"{EVALUATOR_PREFIX}{key}": value for key, value in evaluator_data.items()}
        )
        return data


class EditorGroupBox(QGroupBox):
    """Container widget for the GlobalParametersEditor"""

    def __init__(self, name, editor, parent=None):
        super().__init__(parent)

        self.editor = editor

        name_label = QLabel(name)
        reset_button = QPushButton(
            self.style().standardIcon(QStyle.SP_DialogResetButton), ""
        )
        reset_button.setToolTip(self.tr("Reset values"))

        title_layout = QHBoxLayout()
        title_layout.addWidget(name_label)
        title_layout.addWidget(reset_button)
        title_layout.addStretch(1)

        layout = QVBoxLayout(self)
        layout.addLayout(title_layout)
        layout.addWidget(editor)

        reset_button.clicked.connect(editor.reset)


class GlobalParametersEditor(AbstractBaseEditor):
    """Widget showing all the parameters that can be set"""

    dataChanged = pyqtSignal()

    def __init__(self, prefix_path, parent=None):
        super().__init__(prefix_path, parent)

        self.json_object = {}
        self.environment_changed = False
        self.queue_changed = False
        self.queue_model = QueueResourceModel()

        self.environment_combobox = QComboBox()
        self.queue_combobox = QComboBox()
        self.queue_combobox.setModel(self.queue_model)
        self.parameters_editor_listwidget = EditorListWidget()

        form_layout = QFormLayout()
        form_layout.addRow(self.tr("Environment"), self.environment_combobox)
        form_layout.addRow(self.tr("Queue"), self.queue_combobox)

        layout = self.layout()
        layout.addLayout(form_layout)
        layout.addWidget(self.parameters_editor_listwidget)
        layout.addStretch(1)

        self.environment_combobox.currentIndexChanged.connect(self.dataChanged)
        self.environment_combobox.currentIndexChanged.connect(
            lambda *args: setattr(self, "environment_changed", True)
        )
        self.environment_combobox.currentIndexChanged.connect(
            self.__onEnvironmentChanged
        )
        self.queue_combobox.currentIndexChanged.connect(self.dataChanged)
        self.queue_combobox.currentIndexChanged.connect(
            lambda *args: setattr(self, "queue_changed", True)
        )

        self.parameters_editor_listwidget.dataChanged.connect(self.dataChanged)
        self.prefixPathChanged.connect(self.queue_model.select)

    @pyqtSlot(int)
    def __onEnvironmentChanged(self, row):
        model = self.environment_combobox.model()
        index = model.index(row, 0)

        self.queue_model.setEnvironment(**model.environment(index))
        self.queue_model.setType(model.environmentType(index))
        self.queue_combobox.setCurrentIndex(0)

    def setEnvironmentModel(self, model):
        self.environment_combobox.setModel(model)

    def clear(self):
        self.environment_combobox.setCurrentIndex(0)
        self.parameters_editor_listwidget.clear()

    def setup(self, algorithms):
        current_algorithm_widgets = {
            widget.editor.algorithm_name: widget
            for widget in self.parameters_editor_listwidget.widget_list
        }
        current_algorithms = set(current_algorithm_widgets.keys())

        to_add = algorithms.difference(current_algorithms)
        to_remove = current_algorithms.difference(algorithms)

        for algorithm_name in to_remove:
            self.parameters_editor_listwidget.removeWidget(
                current_algorithm_widgets[algorithm_name]
            )
            self.json_object.pop(algorithm_name, None)

        for algorithm_name in to_add:
            if not algorithm_name:
                continue
            algorithm = AssetType.ALGORITHM.klass(self.prefix_path, algorithm_name)
            if algorithm.valid and algorithm.parameters:
                editor = AlgorithmParametersEditor(self.prefix_path)
                editor.setDumpEditOnlyEnabled(False)
                editor.setup(algorithm_name)
                editor.dataChanged.connect(self.dataChanged)

                global_parameter_editor = EditorGroupBox(algorithm_name, editor)

                self.parameters_editor_listwidget.addWidget(global_parameter_editor)

    def load(self, json_object):
        self.json_object = copy.deepcopy(json_object)

        environment = self.json_object.get("environment")
        if environment:
            env_text = "{} ({})".format(environment["name"], environment["version"])
            self.environment_combobox.setCurrentText(env_text)

        parameters = [
            item
            for item in self.json_object.items()
            if item[0] not in ["queue", "environment"]
        ]

        for data in parameters:
            name, data = data
            editor = None
            for widget in self.parameters_editor_listwidget.widget_list:
                if widget.editor.algorithm_name == name:
                    editor = widget.editor
                    break
            if editor is None:
                raise RuntimeError("Mismatch between globals data and block data")
            editor.load(data)

        self.environment_changed = False
        self.queue_changed = False
        self.parameters_changed = False

    def dump(self):
        data = copy.deepcopy(self.json_object)

        if self.environment_changed or "environment" not in data:
            model = self.environment_combobox.model()
            index = model.index(self.environment_combobox.currentIndex(), 0)
            data["environment"] = model.environment(index)
        if self.queue_changed or "queue" not in data:
            data["queue"] = self.queue_combobox.currentText()

        for widget in self.parameters_editor_listwidget.widget_list:
            editor = widget.editor
            data[editor.algorithm_name] = editor.dump()

        return data


@frozen
class ExperimentEditor(AbstractAssetEditor):
    """Editor for experiment configuration"""

    blockChanged = pyqtSignal(str, dict)

    def __init__(self, parent=None):
        super().__init__(AssetType.EXPERIMENT, parent)
        self.setObjectName(self.__class__.__name__)
        self.set_title(self.tr("Experiment"))

        self.processing_env_model = EnvironmentModel()

        self.algorithm_model = AssetModel()
        self.algorithm_model.setLatestOnlyEnabled(False)
        self.algorithm_model.asset_type = AssetType.ALGORITHM

        self.datasets_widget = ContainerWidget()
        self.blocks_widget = ContainerWidget()
        self.loops_widget = ContainerWidget()
        self.analyzers_widget = ContainerWidget()
        self.globalparameters_widget = GlobalParametersEditor(self.prefixPath())
        self.globalparameters_widget.setEnvironmentModel(self.processing_env_model)

        self.tabwidget = QTabWidget()
        self.tabwidget.addTab(self.datasets_widget, self.tr("Datasets"))
        self.tabwidget.addTab(self.blocks_widget, self.tr("Blocks"))
        self.loops_widget_index = self.tabwidget.addTab(
            self.loops_widget, self.tr("Loops")
        )
        self.tabwidget.addTab(self.analyzers_widget, self.tr("Analyzers"))
        self.tabwidget.addTab(
            self.globalparameters_widget, self.tr("Global parameters")
        )

        self.layout().addWidget(self.tabwidget)

        self.contextChanged.connect(self.__update)

        for widget in [
            self.datasets_widget,
            self.blocks_widget,
            self.loops_widget,
            self.analyzers_widget,
            self.globalparameters_widget,
        ]:
            widget.dataChanged.connect(self.dataChanged)

    @pyqtSlot()
    def __update(self):
        for object_ in [
            self.algorithm_model,
            self.datasets_widget,
            self.blocks_widget,
            self.loops_widget,
            self.analyzers_widget,
            self.globalparameters_widget,
        ]:
            object_.setPrefixPath(self.prefix_path)

        self.processing_env_model.setContext(self.context)

    @pyqtSlot()
    def __onAlgorithmChanged(self):
        algorithms = {
            editor.properties_editor.algorithm
            for editor in self.blocks_widget.widget_list
            + self.analyzers_widget.widget_list
        }

        for editor in self.loops_widget.widget_list:
            algorithms.add(editor.processor_properties_editor.algorithm)
            algorithms.add(editor.evaluator_properties_editor.algorithm)
        self.globalparameters_widget.setup(algorithms)

    def __onBlockChanged(self, asset_name):
        sender = self.sender()
        self.blockChanged.emit(sender.block_name, sender.dump())

    def _asset_models(self):
        """Reimpl"""

        #  Here we use the fact that Python is weakly typed and reload
        #  the dataset model as well
        return [self.algorithm_model]

    def _createNewAsset(self, creation_type, asset_info):
        """Re-implement"""

        if creation_type == AssetCreationDialog.NEW:
            toolchain_name, experiment_name = asset_info
            toolchain = Asset(self.prefix_path, AssetType.TOOLCHAIN, toolchain_name)
            toolchain_declaration = toolchain.declaration
            experiment_declaration = {
                "schema_version": 1,
                "datasets": {},
                "blocks": {},
                "analyzers": {},
                "globals": {
                    "environment": {"name": "dummy", "version": "0.0.0"},
                    "queue": "queue",
                },
            }

            # databases

            database_model = AssetModel()
            database_model.asset_type = AssetType.DATABASE
            database_model.prefix_path = self.prefix_path

            for dataset in toolchain_declaration["datasets"]:
                dataset_data = {"database": None, "protocol": None, "set": None}
                name = dataset["name"]
                experiment_declaration["datasets"][name] = dataset_data

            # blocks

            def build_block_data(block):
                block_data = {"algorithm": None}
                block_data["inputs"] = {
                    f"{input_}_tbr": input_ for input_ in block["inputs"]
                }
                outputs = block.get("outputs", [])
                if outputs:
                    block_data["outputs"] = {
                        f"{output}_tbr": output for output in outputs
                    }

                return block_data

            for block in toolchain_declaration["blocks"]:
                name = block["name"]
                experiment_declaration["blocks"][name] = build_block_data(block)

            # analyzers
            for analyzer in toolchain_declaration["analyzers"]:
                name = analyzer["name"]
                experiment_declaration["analyzers"][name] = build_block_data(analyzer)

            # loops
            if "loops" in toolchain_declaration:
                experiment_declaration["schema_version"] = 2
                experiment_declaration["loops"] = {}

                for loop in toolchain_declaration["loops"]:
                    loop_data = {}

                    processor_block = {
                        key[len(PROCESSOR_PREFIX) :]: value
                        for key, value in loop.items()
                        if key
                        in [
                            f"{PROCESSOR_PREFIX}inputs",
                            f"{PROCESSOR_PREFIX}outputs",
                            f"{PROCESSOR_PREFIX}algorithm",
                        ]
                    }
                    loop_block = {
                        key[len(EVALUATOR_PREFIX) :]: value
                        for key, value in loop.items()
                        if key
                        in [
                            f"{EVALUATOR_PREFIX}inputs",
                            f"{EVALUATOR_PREFIX}outputs",
                            f"{EVALUATOR_PREFIX}algorithm",
                        ]
                    }

                    processor_data = build_block_data(processor_block)
                    evaluator_data = build_block_data(loop_block)
                    loop_data.update(
                        {
                            f"{PROCESSOR_PREFIX}{key}": value
                            for key, value in processor_data.items()
                        }
                    )
                    loop_data.update(
                        {
                            f"{EVALUATOR_PREFIX}{key}": value
                            for key, value in evaluator_data.items()
                        }
                    )

                    name = loop["name"]
                    experiment_declaration["loops"][name] = loop_data

            user = self.context.meta["config"].user
            asset = Asset(
                self.prefix_path,
                AssetType.EXPERIMENT,
                os.path.join(user, toolchain_name, experiment_name),
            )
            os.makedirs(os.path.dirname(asset.declaration_path), exist_ok=True)
            asset.declaration = experiment_declaration
            return asset, experiment_declaration

        else:
            return super(ExperimentEditor, self)._createNewAsset(
                creation_type, asset_info
            )

    def _load_json(self, json_object):
        """Load the json object passed as parameter"""

        experiment_resources.refresh()

        for widget in [
            self.datasets_widget,
            self.blocks_widget,
            self.loops_widget,
            self.analyzers_widget,
            self.globalparameters_widget,
        ]:
            widget.clear()

        datasets = json_object.get("datasets")
        if datasets:
            for name, dataset in datasets.items():
                editor = DatasetEditor(name, self.prefix_path)
                editor.load(dataset)
                editor.datasetChanged.connect(self.__onBlockChanged)
                self.datasets_widget.addWidget(editor)

        used_algorithms = set()

        for type_, container, editor_klass in [
            ("blocks", self.blocks_widget, BlockEditor),
            ("loops", self.loops_widget, LoopBlockEditor),
            ("analyzers", self.analyzers_widget, AnalyzerBlockEditor),
        ]:
            items = json_object.get(type_)
            if items:
                for name, data in items.items():
                    editor = editor_klass(name, self.prefix_path)
                    editor.setEnvironmentModel(self.processing_env_model)
                    editor.load(data)
                    editor.algorithmChanged.connect(self.__onAlgorithmChanged)
                    editor.algorithmChanged.connect(self.__onBlockChanged)
                    container.addWidget(editor)

                    if type_ == "loops":
                        used_algorithms |= editor.selectedAlgorithms()
                    else:
                        used_algorithms.add(editor.selectedAlgorithm())

        self.globalparameters_widget.setup(used_algorithms)
        self.tabwidget.tabBar().setTabEnabled(
            self.loops_widget_index, "loops" in json_object
        )

        globals_ = json_object.get("globals", {})
        self.globalparameters_widget.load(globals_)

    def _dump_json(self):
        """Returns the json representation of the asset"""

        def __filter_parameters(blocks, globals_):
            """If algorithm parameters matches globals keep only the globals version"""

            algorithms = [
                key for key in globals_.keys() if key not in ["environment", "queue"]
            ]
            for block_name, block_data in blocks.items():
                for prefix in ["", PROCESSOR_PREFIX, EVALUATOR_PREFIX]:
                    algorithm_field = f"{prefix}algorithm"
                    parameter_field = f"{prefix}parameters"
                    if algorithm_field in block_data:
                        algorithm_name = block_data[algorithm_field]

                        if algorithm_name in algorithms:
                            block_parameters = block_data.get(parameter_field)
                            if block_parameters:
                                global_parameters = globals_[algorithm_name]
                                for (
                                    parameter_name,
                                    parameter_value,
                                ) in global_parameters.items():
                                    if (
                                        block_parameters.get(parameter_name)
                                        == parameter_value
                                    ):
                                        block_parameters.pop(parameter_name)
                                if not block_parameters:
                                    block_data.pop(parameter_field)

        def __filter_environment(blocks, globals_):
            globals_environment = globals_["environment"]

            for block_name, block_data in blocks.items():
                for prefix in ["", PROCESSOR_PREFIX, EVALUATOR_PREFIX]:
                    environment_key = f"{prefix}environment"

                    block_environment = block_data.get(environment_key)
                    if block_environment and block_environment == globals_environment:
                        block_data.pop(environment_key)

        analyzers = self.analyzers_widget.dump()
        blocks = self.blocks_widget.dump()
        loops = self.loops_widget.dump()
        globals_ = self.globalparameters_widget.dump()

        for item in [analyzers, blocks, loops]:
            __filter_parameters(item, globals_)
            __filter_environment(item, globals_)

        data = {
            "analyzers": analyzers,
            "blocks": blocks,
            "datasets": self.datasets_widget.dump(),
            "globals": globals_,
        }

        if loops:
            data["loops"] = loops

        return data

    def findEditor(self, block_name):
        """Find the editor corresponding to the block_name"""

        editor = None
        widgets = (
            self.datasets_widget.widget_list
            + self.blocks_widget.widget_list
            + self.loops_widget.widget_list
            + self.analyzers_widget.widget_list
        )
        for widget in widgets:
            if widget.block_name == block_name:
                editor = widget
                break
        return editor

    def loadToolchainData(self, toolchain):
        """Load the data from the toolchain where needed"""

        for widget in self.datasets_widget.widget_list:
            widget.loadToolchainData(toolchain)

    def clearBlockErrors(self):
        """Clear error hinting"""

        for widget in [
            self.datasets_widget,
            self.blocks_widget,
            self.loops_widget,
            self.analyzers_widget,
        ]:
            for editor in widget.widget_list:
                editor.setErrors([])

    def setBlockErrors(self, errors_map):
        """Set error hinting on editors

        errors_maps provides a dictionary of block name / error string list
        """

        for widget in [
            self.datasets_widget,
            self.blocks_widget,
            self.loops_widget,
            self.analyzers_widget,
        ]:
            for editor in widget.widget_list:
                errors = errors_map.get(editor.block_name, [])
                editor.setErrors(errors)
