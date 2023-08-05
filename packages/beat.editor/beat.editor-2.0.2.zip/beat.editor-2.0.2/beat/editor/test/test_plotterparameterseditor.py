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

import pytest

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QMessageBox

from ..backend.asset import Asset
from ..backend.asset import AssetType
from ..backend.assetmodel import AssetModel
from ..widgets.plotterparameterseditor import ParameterChoiceDialog
from ..widgets.plotterparameterseditor import PlotterParametersEditor
from ..widgets.plotterparameterseditor import PlotterParameterViewer
from ..widgets.plotterparameterseditor import RestrictedParameterWidget
from .conftest import prefix
from .conftest import sync_prefix


@pytest.fixture()
def plotter_model(test_prefix):
    asset_model = AssetModel()
    asset_model.asset_type = AssetType.PLOTTER
    asset_model.setLatestOnlyEnabled(False)
    asset_model.prefix_path = test_prefix
    return asset_model


def get_plotterparameter(test_prefix):
    sync_prefix()
    model = AssetModel()
    model.asset_type = AssetType.PLOTTERPARAMETER
    model.prefix_path = test_prefix
    model.setLatestOnlyEnabled(False)
    return [
        plotterparameter
        for plotterparameter in model.stringList()
        if all(invalid not in plotterparameter for invalid in ["invalid"])
    ]


@pytest.fixture()
def reference_parameter_json():
    return {
        "axis-fontsize": {
            "default": 10,
            "description": "Controls the axis font size (labels and values)",
            "type": "uint16",
        }
    }


@pytest.fixture()
def modified_parameter_json():
    return {"axis-fontsize": 25}


@pytest.fixture()
def reference_input_string_list():
    return ["some_text_1", "some_text_2", "some_text_3"]


class TestParameterChoiceDialog:
    """Test the addition of parameters from the plotter works correctly"""

    def test_dialog(self, qtbot, reference_input_string_list):
        dialog = ParameterChoiceDialog(reference_input_string_list)
        qtbot.addWidget(dialog)
        qtbot.mouseClick(
            dialog.buttons.button(QDialogButtonBox.Ok), QtCore.Qt.LeftButton
        )
        assert dialog.value() == reference_input_string_list[0]


class TestRestrictedParameterWidget:
    """Test that the restricted parameter editor works correctly"""

    def test_load_and_dump(
        self, qtbot, reference_parameter_json, modified_parameter_json
    ):
        name = next(iter(reference_parameter_json))
        data = reference_parameter_json.get(name, {})
        restricted_parameter_widget = RestrictedParameterWidget(data)
        modified_data = modified_parameter_json.get(name, 0)

        assert restricted_parameter_widget.dump() == data["default"]

        restricted_parameter_widget.load(modified_data)

        assert restricted_parameter_widget.dump() == modified_data


class TestPlotterParameterViewer:
    """Test that the viewer dedicated to the parameters work correctly"""

    def test_load_and_dump(
        self, qtbot, reference_parameter_json, modified_parameter_json
    ):
        name = next(iter(reference_parameter_json))
        data = reference_parameter_json.get(name, {})
        parameter_viewer = PlotterParameterViewer(name, data)
        modified_data = modified_parameter_json.get(name, 0)
        parameter_viewer.load(modified_data)

        assert parameter_viewer.dump() == modified_parameter_json

    def test_get_name(self, qtbot, reference_parameter_json, modified_parameter_json):
        name = next(iter(reference_parameter_json))
        data = reference_parameter_json.get(name, {})
        parameter_viewer = PlotterParameterViewer(name, data)
        modified_data = modified_parameter_json.get(name, 0)

        assert parameter_viewer.dump() == {
            name: reference_parameter_json[name]["default"]
        }

        parameter_viewer.load(modified_data)

        assert parameter_viewer.dump() == modified_parameter_json
        assert parameter_viewer.name() == name


class TestPlotterParametersEditor:
    """Test that the mock editor works correctly"""

    @pytest.mark.parametrize("plotterparameter", get_plotterparameter(prefix))
    def test_load_and_dump(
        self, qtbot, beat_context, plotter_model, test_prefix, plotterparameter
    ):
        asset_name = plotterparameter
        asset = Asset(test_prefix, AssetType.PLOTTERPARAMETER, asset_name)

        editor = PlotterParametersEditor()
        editor.set_context(beat_context)
        editor.set_plotter_model_to_combobox(plotter_model)

        editor.load_json(asset.declaration)

        qtbot.addWidget(editor)

        assert editor.dump_json() == asset.declaration

    def test_change_plotter(self, qtbot, beat_context, plotter_model, test_prefix):
        asset_name = "plot/config/1"
        asset = Asset(test_prefix, AssetType.PLOTTERPARAMETER, asset_name)

        editor = PlotterParametersEditor()
        editor.set_context(beat_context)
        editor.set_plotter_model_to_combobox(plotter_model)

        editor.load_json(asset.declaration)

        qtbot.addWidget(editor)

        assert editor.dump_json() == asset.declaration

        asset_list = plotter_model.stringList()
        qtbot.keyClicks(editor.plotter_combobox, asset_list[1])
        assert editor.dump_json()["plotter"] == asset_list[1]

    def test_add_plotter_parameter(
        self, qtbot, monkeypatch, beat_context, plotter_model, test_prefix
    ):
        asset_name = "plot/config/1"
        asset = Asset(test_prefix, AssetType.PLOTTERPARAMETER, asset_name)

        editor = PlotterParametersEditor()
        editor.set_context(beat_context)
        editor.set_plotter_model_to_combobox(plotter_model)

        plotter_name = asset.declaration.get("plotter", None)
        asset_plotter = Asset(test_prefix, AssetType.PLOTTER, plotter_name)

        editor.load_json(asset.declaration)

        qtbot.addWidget(editor)

        parameters_used = editor.dump_json()["data"]
        reference_plotter_parameters = asset_plotter.declaration.get("parameters", {})
        unused_plotterparameters = []

        for name, data in reference_plotter_parameters.items():
            if name not in parameters_used:
                unused_plotterparameters.append(name)

        assert editor.dump_json() == asset.declaration

        monkeypatch.setattr(
            ParameterChoiceDialog,
            "getParameterObject",
            classmethod(lambda *args: (unused_plotterparameters[0], True)),
        )

        qtbot.mouseClick(editor.add_parameter_button, QtCore.Qt.LeftButton)

        updated_plotterparameter = asset.declaration
        updated_plotterparameter["data"][
            unused_plotterparameters[0]
        ] = reference_plotter_parameters[unused_plotterparameters[0]]["default"]

        assert editor.dump_json() == updated_plotterparameter

    def test_remove_plotter_parameter(
        self, qtbot, monkeypatch, beat_context, plotter_model, test_prefix
    ):

        asset_name = "plot/config/1"
        asset = Asset(test_prefix, AssetType.PLOTTERPARAMETER, asset_name)

        editor = PlotterParametersEditor()
        editor.set_context(beat_context)
        editor.set_plotter_model_to_combobox(plotter_model)

        plotter_name = asset.declaration.get("plotter", None)
        asset_plotter = Asset(test_prefix, AssetType.PLOTTER, plotter_name)

        editor.load_json(asset.declaration)

        qtbot.addWidget(editor)

        parameters_used = editor.dump_json()["data"]
        reference_plotter_parameters = asset_plotter.declaration.get("parameters", {})
        unused_plotterparameters = []

        for name, data in reference_plotter_parameters.items():
            if name not in parameters_used:
                unused_plotterparameters.append(name)

        assert editor.dump_json() == asset.declaration

        parameters_length_before_deletion = len(editor.scroll_widget.widget_list)

        qtbot.mouseClick(
            editor.scroll_widget.widget_list[0].delete_button, QtCore.Qt.LeftButton
        )

        assert len(editor.scroll_widget.widget_list) == (
            parameters_length_before_deletion - 1
        )

    def test_disabled_enabled_add_plotter_parameter_button(
        self, qtbot, monkeypatch, beat_context, plotter_model, test_prefix
    ):
        asset_name = "plot/config/1"
        asset = Asset(test_prefix, AssetType.PLOTTERPARAMETER, asset_name)

        editor = PlotterParametersEditor()
        editor.set_context(beat_context)
        editor.set_plotter_model_to_combobox(plotter_model)

        plotter_name = asset.declaration.get("plotter", None)
        asset_plotter = Asset(test_prefix, AssetType.PLOTTER, plotter_name)

        editor.load_json(asset.declaration)

        qtbot.addWidget(editor)

        parameters_used = editor.dump_json()["data"]
        reference_plotter_parameters = asset_plotter.declaration.get("parameters", {})
        unused_plotterparameters = []

        for name, data in reference_plotter_parameters.items():
            if name not in parameters_used:
                unused_plotterparameters.append(name)

        assert editor.dump_json() == asset.declaration

        updated_plotterparameter = asset.declaration

        # Add all possible parameters
        for parameter in unused_plotterparameters:
            monkeypatch.setattr(
                ParameterChoiceDialog,
                "getParameterObject",
                classmethod(lambda *args: (parameter, True)),
            )

            monkeypatch.setattr(
                QMessageBox, "information", lambda *args: QMessageBox.Ok
            )
            # Check enabled button
            assert editor.add_parameter_button.isEnabled() is True

            qtbot.mouseClick(editor.add_parameter_button, QtCore.Qt.LeftButton)

            updated_plotterparameter["data"][parameter] = reference_plotter_parameters[
                parameter
            ]["default"]

            assert editor.dump_json() == updated_plotterparameter

            if (
                unused_plotterparameters.index(parameter)
                == len(unused_plotterparameters) - 1
            ):
                # Check disabled button change
                assert editor.add_parameter_button.isEnabled() is False

        # Check button gets re-enabled on parameter deletion
        qtbot.mouseClick(
            editor.scroll_widget.widget_list[0].delete_button, QtCore.Qt.LeftButton
        )

        assert editor.add_parameter_button.isEnabled() is True
