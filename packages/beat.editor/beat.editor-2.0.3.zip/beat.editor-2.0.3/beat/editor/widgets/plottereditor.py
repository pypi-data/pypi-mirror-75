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

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from ..backend.asset import AssetType
from ..backend.assetmodel import AssetModel
from ..decorators import frozen
from .dialogs import AssetCreationDialog
from .dialogs import NameInputDialog
from .editor import AbstractAssetEditor
from .libraries import LibrariesWidget
from .parameterwidget import ParameterWidget
from .scrollwidget import ScrollWidget
from .validatedhelpers import NameLineEdit


class ParameterViewer(QWidget):

    dataChanged = pyqtSignal()
    deletionRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.delete_button = QPushButton(self.tr("-"))
        self.delete_button.setToolTip(self.tr("Remove parameter"))
        self.delete_button.setFixedSize(30, 30)

        delete_layout = QHBoxLayout()
        delete_layout.addStretch(1)
        delete_layout.addWidget(self.delete_button)

        self.name_lineedit = NameLineEdit()
        self.parameter_widget = ParameterWidget()

        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        form_layout.addRow(self.tr("Name"), self.name_lineedit)

        layout = QVBoxLayout(self)
        layout.addLayout(delete_layout)
        layout.addLayout(form_layout)
        layout.addWidget(self.parameter_widget)

        self.name_lineedit.textChanged.connect(self.dataChanged)
        self.delete_button.clicked.connect(self.deletionRequested)
        self.parameter_widget.dataChanged.connect(self.dataChanged)

    def name(self):
        """Name of the parameter"""

        return self.name_lineedit.text()

    def load(self, name, data):
        """Load this widget with the content of json_data"""

        self.name_lineedit.setText(name)

        self.parameter_widget.load(data)

    def dump(self):
        """Returns the json representation of this set"""

        parameter_name = self.name_lineedit.text()
        parameter_data = self.parameter_widget.dump()

        return {parameter_name: parameter_data}


@frozen
class PlotterEditor(AbstractAssetEditor):
    def __init__(self, parent=None):
        super().__init__(AssetType.PLOTTER, parent)
        self.setObjectName(self.__class__.__name__)
        self.set_title(self.tr("Plotter"))

        self.plotter_model = AssetModel()
        self.plotter_model.asset_type = AssetType.PLOTTER

        self.dataformat_model = AssetModel()
        self.dataformat_model.asset_type = AssetType.DATAFORMAT

        self.library_model = AssetModel()
        self.library_model.asset_type = AssetType.LIBRARY

        self.libraries_widget = LibrariesWidget()

        self.scroll_widget = ScrollWidget()

        self.add_parameter_button = QPushButton(self.tr("+"))
        self.add_parameter_button.setToolTip(self.tr("Add parameter"))
        self.add_parameter_button.setFixedSize(30, 30)

        self.dataformat_combobox = QComboBox(parent)
        self.dataformat_combobox.setModel(self.dataformat_model)

        self.language = ""

        dataformat_label = QLabel(self.tr("Dataformat"))
        self.layout().addWidget(dataformat_label)
        self.layout().addWidget(self.dataformat_combobox)
        self.layout().addWidget(self.scroll_widget, 1)
        self.layout().addWidget(self.libraries_widget)
        self.layout().addWidget(self.add_parameter_button, 1)

        self.libraries_widget.dataChanged.connect(self.dataChanged)
        self.scroll_widget.dataChanged.connect(self.dataChanged)
        self.libraries_widget.dataChanged.connect(self.dataChanged)
        self.add_parameter_button.clicked.connect(self.__addParameter)
        self.contextChanged.connect(
            lambda: self.plotter_model.setPrefixPath(self.prefix_path)
        )
        self.contextChanged.connect(
            lambda: self.dataformat_model.setPrefixPath(self.prefix_path)
        )
        self.contextChanged.connect(
            lambda: self.library_model.setPrefixPath(self.prefix_path)
        )

    @property
    def parameter_viewers(self):
        return self.scroll_widget.widget_list

    @pyqtSlot()
    def __onRemoveRequested(self):
        """Remove the widget clicked"""

        self.__remove_widget(self.sender())

    def __remove_widget(self, widget):
        """Removes the widget that which signal triggered this slot"""

        self.scroll_widget.removeWidget(widget)

    @pyqtSlot()
    def __addParameter(self):
        """Add a new parameter"""

        parameter_names = [widget.name() for widget in self.parameter_viewers]

        while True:
            name, ok_pressed = NameInputDialog.getText(self, self.tr("Parameter name"))
            if not ok_pressed:
                break

            if ok_pressed and name not in parameter_names:
                new_parameter = {name: ParameterWidget().dump()}

                self.__load_parameter({"parameters": new_parameter})
                self.dataChanged.emit()
                break

    @pyqtSlot()
    def __showLatestParameter(self):
        """Ensure that the latest set is visible"""

        if self.parameter_viewers:
            self.scroll_widget.ensureWidgetVisible(self.parameter_viewers[-1], 10, 10)

    def __load_parameter(self, json_object):
        parameters = json_object.get("parameters", {})

        for name, data in parameters.items():
            parameter_viewer = ParameterViewer()
            parameter_viewer.load(name, data)
            self.scroll_widget.addWidget(parameter_viewer)
            parameter_viewer.deletionRequested.connect(self.__onRemoveRequested)

    def __load_json(self, json_object):
        """Load the json object passed as parameter"""

        self.blockSignals(True)

        self.language = json_object.get("language", "")

        selected_dataformat = json_object.get("dataformat", "")
        index = self.dataformat_combobox.findText(
            selected_dataformat, Qt.MatchFixedString
        )

        self.dataformat_combobox.setCurrentIndex(index)

        self.libraries_widget.set_available_libraries(self.library_model.stringList())
        self.libraries_widget.set_used_libraries(json_object.get("uses", {}))

        self.__load_parameter(json_object)

        self.blockSignals(False)

        if self.parameter_viewers:
            QTimer.singleShot(100, self.__showLatestParameter)

    def _asset_models(self):
        """Returns a list of all asset models used"""

        return [self.plotter_model, self.dataformat_model, self.library_model]

    def _createNewAsset(self, creation_type, asset_info):
        """Re-implement to ensure we"""

        plotter, data = super(PlotterEditor, self)._createNewAsset(
            creation_type, asset_info
        )

        if creation_type == AssetCreationDialog.NEW:
            declaration = plotter.declaration
            valid_dataformats = [
                df
                for df in self.dataformat_model.stringList()
                if df.startswith("plot/")
            ]
            declaration["dataformat"] = valid_dataformats[0]
            plotter.declaration = declaration

        return plotter, data

    def _load_json(self, json_object):
        """Load the json object passed as parameter"""

        self.scroll_widget.clear()

        while self.parameter_viewers:
            widget = self.parameter_viewers[0]
            self.__remove_widget(widget)

        self.__load_json(json_object)

    def _dump_json(self):
        """Returns the json representation of the asset"""

        parameters = {}
        for widget in self.parameter_viewers:
            parameters.update(widget.dump())

        used_libraries = self.libraries_widget.get_used_libraries()
        output = {
            "dataformat": self.dataformat_combobox.currentText(),
            "parameters": parameters,
            "language": self.language,
        }

        if len(used_libraries) != 0:
            output["uses"] = used_libraries

        return output
