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

import pytest
import simplejson as json

from PyQt5 import QtCore

from ..backend.asset import Asset
from ..backend.asset import AssetType
from ..backend.assetmodel import DataFormatModel
from ..widgets.dialogs import NameInputDialog
from ..widgets.protocoltemplateeditor import ProtocolTemplateEditor
from ..widgets.protocoltemplateeditor import SetWidget


@pytest.fixture()
def dataformat_model(test_prefix):
    asset_model = DataFormatModel()
    asset_model.prefix_path = test_prefix
    asset_model.full_list_enabled = True
    return asset_model


@pytest.fixture()
def reference_set_json():
    return {"name": "test", "outputs": {"out1": "int8"}}


@pytest.fixture()
def reference_pt_json():
    return {"sets": [{"name": "original", "outputs": {"a": "int8"}}]}


class TestSetWidget:
    """Test that the editor dedicated to a set works correctly"""

    def test_load_and_dump(self, qtbot, dataformat_model, reference_set_json):
        set_widget = SetWidget(dataformat_model)
        set_widget.load(reference_set_json)

        qtbot.addWidget(set_widget)

        assert set_widget.dump() == reference_set_json

    def test_add_output(self, qtbot, dataformat_model, reference_set_json):
        edited_json = copy.deepcopy(reference_set_json)
        edited_json["outputs"]["Change_me"] = "int8"

        set_widget = SetWidget(dataformat_model)
        set_widget.load(reference_set_json)

        qtbot.addWidget(set_widget)

        qtbot.mouseClick(set_widget.add_button, QtCore.Qt.LeftButton)

        assert set_widget.dump() == edited_json

    def test_remove_output(self, qtbot, dataformat_model, reference_set_json):
        edited_json = copy.deepcopy(reference_set_json)
        edited_json["outputs"] = {}

        set_widget = SetWidget(dataformat_model)
        set_widget.load(reference_set_json)

        qtbot.addWidget(set_widget)

        qtbot.mouseClick(set_widget.remove_button, QtCore.Qt.LeftButton)

        assert set_widget.dump() == reference_set_json

        set_widget.outputs_tablewidget.setCurrentCell(0, 0)

        qtbot.mouseClick(set_widget.remove_button, QtCore.Qt.LeftButton)

        assert set_widget.dump() == edited_json


class TestProtocolTemplateEditor:
    """Test that the protocol template editor works correctly"""

    def test_load_and_dump(self, qtbot, test_prefix):
        asset_name = "double/1"
        asset = Asset(test_prefix, AssetType.PROTOCOLTEMPLATE, asset_name)
        with open(asset.declaration_path, "rt") as json_file:
            json_data = json.load(json_file)
            editor = ProtocolTemplateEditor()
            editor.load_json(json_data)

            qtbot.addWidget(editor)

            assert editor.dump_json() == json_data

    def test_add_set(self, qtbot, monkeypatch, beat_context, reference_pt_json):
        edited_json = copy.deepcopy(reference_pt_json)
        edited_json["schema_version"] = 1
        edited_json["sets"].append(
            {"name": "test_set", "outputs": {"Change_me": "int8"}}
        )

        monkeypatch.setattr(
            NameInputDialog, "getText", classmethod(lambda *args: ("test_set", True))
        )

        editor = ProtocolTemplateEditor()
        editor.set_context(beat_context)
        editor.load_json(reference_pt_json)

        qtbot.addWidget(editor)
        qtbot.mouseClick(editor.add_set_button, QtCore.Qt.LeftButton)

        assert editor.dump_json() == edited_json

    def test_remove_set(self, qtbot, beat_context, reference_pt_json):
        edited_json = copy.deepcopy(reference_pt_json)
        edited_json["schema_version"] = 1
        edited_json["sets"] = []

        editor = ProtocolTemplateEditor()
        editor.set_context(beat_context)
        editor.load_json(reference_pt_json)

        qtbot.addWidget(editor)
        qtbot.mouseClick(editor.set_widgets[0].delete_button, QtCore.Qt.LeftButton)

        assert editor.dump_json() == edited_json
