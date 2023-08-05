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

from ..backend.asset import Asset
from ..backend.asset import AssetType
from ..backend.assetmodel import AssetModel
from ..widgets.plottereditor import ParameterViewer
from ..widgets.plottereditor import PlotterEditor


@pytest.fixture()
def dataformat_model(test_prefix):
    asset_model = AssetModel()
    asset_model.asset_type = AssetType.DATAFORMAT
    asset_model.prefix_path = test_prefix
    return asset_model


@pytest.fixture()
def reference_parameter_json():
    return {
        "axis-fontsize": {
            "default": 10,
            "description": "Controls the axis font size (labels and values)",
            "type": "uint16",
        }
    }


class TestParameterViewer:
    """Test that the viewer dedicated to the parameters work correctly"""

    def test_load_and_dump(self, qtbot, reference_parameter_json):
        parameter_viewer = ParameterViewer()

        key = next(iter(reference_parameter_json))
        value = reference_parameter_json.get(key, {})
        parameter_viewer.load(key, value)

        assert parameter_viewer.dump() == reference_parameter_json

    def test_get_name(self, qtbot, reference_parameter_json):
        parameter_viewer = ParameterViewer()

        key = next(iter(reference_parameter_json))
        value = reference_parameter_json.get(key, {})
        parameter_viewer.load(key, value)

        assert parameter_viewer.dump() == reference_parameter_json
        assert parameter_viewer.name() == key


class TestPlotterEditor:
    """Test that the plotter editor works correctly"""

    def test_load_and_dump(self, qtbot, dataformat_model, test_prefix, beat_context):
        asset_name = "user/scatter/1"
        asset = Asset(test_prefix, AssetType.PLOTTER, asset_name)
        json_data = asset.declaration
        editor = PlotterEditor()
        editor.set_context(beat_context)
        editor.load_json(json_data)

        qtbot.addWidget(editor)

        assert editor.dump_json() == json_data

    def test_change_dataformat(
        self, qtbot, dataformat_model, test_prefix, beat_context
    ):
        asset_name = "user/scatter/1"
        asset = Asset(test_prefix, AssetType.PLOTTER, asset_name)
        json_data = asset.declaration
        editor = PlotterEditor()
        editor.set_context(beat_context)
        editor.load_json(json_data)

        qtbot.addWidget(editor)

        assert editor.dump_json() == json_data

        asset_list = dataformat_model.stringList()
        qtbot.keyClicks(editor.dataformat_combobox, asset_list[1])

        assert editor.dump_json()["dataformat"] == asset_list[1]
