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

import logging

import numpy as np

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from ..backend.asset import Asset
from ..backend.asset import AssetType
from ..backend.assetmodel import AssetModel
from ..decorators import frozen
from .dialogs import AssetCreationDialog
from .editor import AbstractAssetEditor
from .parameterwidget import InputType
from .scrollwidget import ScrollWidget
from .spinboxes import NumpySpinBox

logger = logging.getLogger(__name__)


class ParameterChoiceDialog(QDialog):
    """Dialog to retrieve a value to to add to the editable parameters"""

    def __init__(self, unused_parameters_list, parent=None):
        """Constructor

        :param unused_parameters_list: parameters that can still be edited
        :param parent QWidget: parent widget
        """

        super().__init__(parent)

        self.setWindowTitle(self.tr("Input"))
        self.label = QLabel(self.tr("Add Parameter:"))
        self.combobox = QComboBox()
        self.combobox.addItems(unused_parameters_list)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.combobox)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )
        layout.addWidget(self.buttons)

        # Signals/Slots connection
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def value(self):
        """Returns the value selected"""

        return self.combobox.currentText()

    @staticmethod
    def getParameterObject(unused_parameters_list, parent=None):
        """Static method to create the dialog and return qdialog accepted/combobox value

        :param unused_parameters_list: parameters that can still be edited
        :param parent QWidget: parent widget
        """

        dialog = ParameterChoiceDialog(unused_parameters_list, parent)
        result = dialog.exec_()
        value = None

        if result == QDialog.Accepted:
            value = dialog.value()

        return (value, result)


class RestrictedParameterWidget(QWidget):
    """Widget representing a parameter"""

    dataChanged = pyqtSignal()

    def __init__(self, data, parent=None):
        """Constructor

        :param data: single parameter data
        :param parent QWidget: parent widget
        """

        super().__init__(parent)

        self._type = data.get("type", None)
        default = data.get("default", "" if self._type == "string" else 0)
        # cast the default value to the required type
        cast_fn = np.cast[self._type] if self._type != "string" else str
        try:
            default = cast_fn(default)
        except ValueError:
            logger.exception(
                f"Failed to convert the default value: {default} to type {self._type}",
            )
            default = cast_fn("" if self._type == "string" else 0)
        self.default = default

        self.current_type = InputType[self._type.upper()]
        self.modality = "single"
        if "choice" in data:
            self.modality = "choice"
        elif "range" in data:
            self.modality = "range"

        layout = QHBoxLayout(self)

        if self._type == "string":
            if self.modality == "choice":
                self.choices_combobox = QComboBox()
                layout.addWidget(self.choices_combobox)
                self.choices_combobox.currentIndexChanged.connect(self.dataChanged)
                self.choices_combobox.addItems(data.get("choice", []))
                self.__set_choice_default_value(self.default)

            else:
                self.single_ledit = QLineEdit()
                layout.addWidget(self.single_ledit)
                self.single_ledit.textChanged.connect(self.dataChanged)

                self.single_ledit.setText(self.default)

        elif self._type == "bool":

            self.bool_checkbox = QCheckBox()
            layout.addWidget(self.bool_checkbox)
            self.bool_checkbox.stateChanged.connect(self.dataChanged)

            self.bool_checkbox.setChecked(self.default)

        else:
            # Numerical parameter type
            if self.modality == "choice":
                self.choices_combobox = QComboBox()
                layout.addWidget(self.choices_combobox)
                self.choices_combobox.currentIndexChanged.connect(self.dataChanged)

                choices = data.get("choice", [])
                str_choices = [str(item) for item in choices]
                self.choices_combobox.addItems(str_choices)

                self.__set_choice_default_value(str(self.default))

            else:

                min_value = self.current_type.numpy_info.min
                max_value = self.current_type.numpy_info.max

                if self.modality == "range":
                    min_value = data["range"][0]
                    max_value = data["range"][1]

                self.numerical_spinbox = NumpySpinBox(self.current_type.np_type)
                self.numerical_spinbox.setMinimum(min_value)
                self.numerical_spinbox.setMaximum(max_value)
                layout.addWidget(self.numerical_spinbox)
                self.numerical_spinbox.valueChanged.connect(self.dataChanged)

                self.numerical_spinbox.setValue(self.default)

    def dump(self):
        """Returns the json representation of this editor"""

        output = None

        if self._type == "string":
            if self.modality == "choice":
                output = self.choices_combobox.currentText()
            else:
                output = self.single_ledit.text()
        elif self._type == "bool":
            output = self.bool_checkbox.isChecked()
        else:
            # Numerical parameter type
            if self.modality == "choice":
                output = self.choices_combobox.currentText()
            else:
                output = self.numerical_spinbox.value

        return output

    def load(self, data):
        """Load the json object passed as parameter"""

        if self._type == "string":
            if self.modality == "choice":
                self.__set_choice_default_value(data)
            else:
                self.single_ledit.setText(data)
        elif self._type == "bool":
            self.bool_checkbox.setChecked(data)
        else:
            # Numerical parameter type
            if self.modality == "choice":
                self.__set_choice_default_value(str(data))
            else:
                self.numerical_spinbox.setValue(data)

    def __set_choice_default_value(self, default_value):
        index = self.choices_combobox.findText(default_value, Qt.MatchFixedString)
        self.choices_combobox.setCurrentIndex(index)


class PlotterParameterViewer(QWidget):

    dataChanged = pyqtSignal()
    deletionRequested = pyqtSignal()

    def __init__(self, name, data, parent=None):
        """Constructor

        :param name: parameter name
        :param name: parameter data
        :param parent QWidget: parent widget
        """

        super().__init__(parent)

        self.delete_button = QPushButton(self.tr("-"))
        self.delete_button.setToolTip(self.tr("Remove parameter"))
        self.delete_button.setFixedSize(30, 30)

        delete_layout = QHBoxLayout()
        delete_layout.addStretch(1)
        delete_layout.addWidget(self.delete_button)

        self.name_label = QLabel()
        self.description_label = QLabel()

        self.parameter_widget = RestrictedParameterWidget(data)

        self.parameter_layout = QHBoxLayout()

        self.form_layout = QFormLayout()
        self.form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.form_layout.addRow(self.tr("Name"), self.name_label)
        self.form_layout.addRow(self.tr("Description"), self.description_label)
        self.form_layout.addRow(self.tr("Parameter"), self.parameter_layout)

        layout = QVBoxLayout(self)
        layout.addLayout(delete_layout)
        layout.addLayout(self.form_layout)

        self.name_label.setText(name)

        self.description_label.setText(data.get("description", ""))
        self.delete_button.clicked.connect(self.deletionRequested)
        self.parameter_layout.addWidget(self.parameter_widget)
        self.parameter_widget.dataChanged.connect(self.dataChanged)

    def name(self):
        """Name of the parameter"""

        return self.name_label.text()

    def load(self, data):
        """Load this widget with the content of json_data"""

        self.parameter_widget.load(data)
        # self.parameter_layout.addWidget(self.parameter_widget)

    def dump(self):
        """Returns the json representation of this set"""

        parameter_name = self.name_label.text()
        parameter_data = self.parameter_widget.dump()

        json_data = {parameter_name: parameter_data}

        return json_data


@frozen
class PlotterParametersEditor(AbstractAssetEditor):
    def __init__(self, parent=None):
        """Constructor

        :param parent QWidget: parent widget
        """

        super().__init__(AssetType.PLOTTERPARAMETER, parent)
        self.setObjectName(self.__class__.__name__)
        self.set_title(self.tr("Plotter Parameters"))

        self.plotterparameter_model = AssetModel()
        self.plotterparameter_model.asset_type = AssetType.PLOTTERPARAMETER

        self.plotter_model = AssetModel()
        self.plotter_model.asset_type = AssetType.PLOTTER
        self.plotter_model.setLatestOnlyEnabled(False)
        self.plotter_json_data = None

        self.scroll_widget = ScrollWidget()

        self.add_parameter_button = QPushButton(self.tr("+"))
        self.add_parameter_button.setToolTip(self.tr("Add parameter"))
        self.add_parameter_button.setFixedSize(30, 30)

        plotter_label = QLabel(self.tr("Plotter"))
        self.plotter_combobox = QComboBox(parent)
        self.plotter_combobox.setModel(self.plotter_model)

        self.layout().addWidget(plotter_label)
        self.layout().addWidget(self.plotter_combobox)
        self.layout().addWidget(self.scroll_widget, 1)
        self.layout().addWidget(self.add_parameter_button, 1)

        self.scroll_widget.dataChanged.connect(self.dataChanged)
        self.add_parameter_button.clicked.connect(self.__addParameter)
        self.contextChanged.connect(
            lambda: self.plotterparameter_model.setPrefixPath(self.prefix_path)
        )
        self.contextChanged.connect(
            lambda: self.plotter_model.setPrefixPath(self.prefix_path)
        )

        self.plotter_combobox.currentIndexChanged.connect(
            self.__onPlotterReferenceChanged
        )

    def set_plotter_model_to_combobox(self, plotter_model):
        self.plotter_combobox.setModel(plotter_model)

    @pyqtSlot()
    def __onPlotterReferenceChanged(self):
        """Update reference if plotter type changes"""

        selected_plotter = self.plotter_combobox.currentText()
        self.__fetch_load_plotter_data(selected_plotter)
        self.__load_parameter({})

    @property
    def parameter_viewers(self):
        return self.scroll_widget.widget_list

    def __remove_widget(self, widget):
        """Removes the widget that which signal triggered this slot"""

        self.scroll_widget.removeWidget(widget)

    @pyqtSlot()
    def __onRemoveRequested(self):
        """Remove the widget clicked"""

        self.add_parameter_button.setEnabled(True)
        self.__remove_widget(self.sender())

    @pyqtSlot()
    def __addParameter(self):
        """Add a new parameter"""

        name = None
        ok = False

        parameters_used = self._dump_json()["data"]
        reference_plotter_parameters = self.plotter_json_data.get("parameters", {})
        unused_plotterparameters = []

        for name, data in reference_plotter_parameters.items():
            if name not in parameters_used:
                unused_plotterparameters.append(name)

        if len(unused_plotterparameters) > 0:
            name, ok = ParameterChoiceDialog.getParameterObject(
                unused_plotterparameters
            )

            if ok:
                data = reference_plotter_parameters[name]
                parameter_viewer = PlotterParameterViewer(name, data)
                self.scroll_widget.addWidget(parameter_viewer)
                parameter_viewer.deletionRequested.connect(self.__onRemoveRequested)

                # Disable add button when last parameter is added
                if len(unused_plotterparameters) == 1:
                    QMessageBox.information(
                        self,
                        self.tr("Plotter Parameters"),
                        self.tr("All possible parameters have already been added"),
                    )

                    self.add_parameter_button.setEnabled(False)

    @pyqtSlot()
    def __showLatestParameter(self):
        """Ensure that the latest set is visible"""

        if self.parameter_viewers:
            self.scroll_widget.ensureWidgetVisible(self.parameter_viewers[-1], 10, 10)

    def __fetch_load_plotter_data(self, selected_plotter):
        """Load json data from the asset"""

        # Fetch plotter json data

        if selected_plotter:

            asset = Asset(
                self.plotter_model.prefix_path,
                self.plotter_model.asset_type,
                selected_plotter,
            )

            self.plotter_json_data = asset.declaration
        else:
            self.plotter_json_data = {}

        while self.parameter_viewers:
            widget = self.parameter_viewers[0]
            self.__remove_widget(widget)

    def __load_parameter(self, json_object):
        """Load parameters from the json data"""

        parameters = json_object.get("data", {})
        reference_plotter_parameters = self.plotter_json_data.get("parameters", {})

        for name, data in reference_plotter_parameters.items():

            if name in parameters:
                parameter_viewer = PlotterParameterViewer(name, data)
                parameter_viewer.load(parameters[name])

                self.scroll_widget.addWidget(parameter_viewer)
                parameter_viewer.deletionRequested.connect(self.__onRemoveRequested)

    def __load_json(self, json_object):
        """Load the json object passed as parameter"""

        self.blockSignals(True)

        selected_plotter = json_object.get("plotter")
        index = self.plotter_combobox.findText(selected_plotter, Qt.MatchFixedString)
        self.plotter_combobox.setCurrentIndex(index)

        self.__load_parameter(json_object)

        self.blockSignals(False)

        if self.parameter_viewers:
            QTimer.singleShot(100, self.__showLatestParameter)

    def _asset_models(self):
        """Returns a list of all asset models used"""

        return [self.plotter_model, self.plotterparameter_model]

    def _createNewAsset(self, creation_type, asset_info):
        """Re-implement to ensure we"""

        plotterparameters, data = super(PlotterParametersEditor, self)._createNewAsset(
            creation_type, asset_info
        )

        if creation_type == AssetCreationDialog.NEW:
            declaration = plotterparameters.declaration
            declaration["plotter"] = self.plotter_model.index(0, 0).data()
            plotterparameters.declaration = declaration

        return plotterparameters, data

    def _load_json(self, json_object):
        """Load the json object passed as parameter"""

        self.scroll_widget.clear()

        selected_plotter = json_object.get("plotter")

        self.__fetch_load_plotter_data(selected_plotter)

        self.__load_json(json_object)

    def _dump_json(self):
        """Returns the json representation of the asset"""

        parameters = {}

        for widget in self.parameter_viewers:
            parameters.update(widget.dump())

        output = {"data": parameters, "plotter": self.plotter_combobox.currentText()}

        return output
