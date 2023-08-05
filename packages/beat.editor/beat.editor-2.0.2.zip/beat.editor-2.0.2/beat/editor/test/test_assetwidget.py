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
import random

import pytest

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox

from ..backend.asset import Asset
from ..backend.asset import AssetType
from ..backend.assetmodel import AssetModel
from ..widgets.algorithmeditor import AlgorithmEditor
from ..widgets.assetwidget import AssetWidget
from ..widgets.assetwidget import widget_for_asset_type
from ..widgets.databaseeditor import DatabaseEditor
from ..widgets.dataformateditor import DataformatEditor
from ..widgets.dialogs import AssetCreationDialog
from ..widgets.editor import PlaceholderEditor
from ..widgets.experimenteditor import ExperimentEditor
from ..widgets.libraryeditor import LibraryEditor
from ..widgets.plottereditor import PlotterEditor
from ..widgets.plotterparameterseditor import PlotterParametersEditor
from ..widgets.protocoltemplateeditor import ProtocolTemplateEditor
from ..widgets.toolchaineditor import ToolchainEditor
from .conftest import sync_prefix


@pytest.fixture()
def asset_type_prefix_entry_map():
    return {
        AssetType.ALGORITHM: ("user/integers_add_v2/1", AlgorithmEditor),
        AssetType.DATABASE: ("integers_db/2", DatabaseEditor),
        AssetType.DATAFORMAT: ("user/single_string/1", DataformatEditor),
        AssetType.EXPERIMENT: ("user/user/triangle/1/triangle", ExperimentEditor),
        AssetType.LIBRARY: ("user/sum/1", LibraryEditor),
        AssetType.PLOTTER: ("user/scatter/1", PlotterEditor),
        AssetType.PLOTTERPARAMETER: ("plot/config/1", PlotterParametersEditor),
        AssetType.PROTOCOLTEMPLATE: ("double/1", ProtocolTemplateEditor),
        AssetType.TOOLCHAIN: ("user/double/1", ToolchainEditor),
    }


def test_widget_factory_error():
    with pytest.raises(RuntimeError):
        widget_for_asset_type("dummy")


class TestAssetWidget:
    """Test that the AssetWidget works correctly"""

    @pytest.fixture(autouse=True)
    def synced_prefix(self):
        """Re sync the prefix between test"""
        sync_prefix()

    def test_matching_editor(
        self, qtbot, test_prefix, beat_context, asset_type_prefix_entry_map
    ):
        asset_widget = AssetWidget()
        qtbot.addWidget(asset_widget)
        asset_widget.set_context(beat_context)

        assert isinstance(asset_widget.current_editor, PlaceholderEditor)

        for (
            asset_type,
            (asset_name, editor_type),
        ) in asset_type_prefix_entry_map.items():
            asset = Asset(test_prefix, asset_type, asset_name)
            with qtbot.waitSignal(asset_widget.currentAssetChanged):
                asset_widget.loadAsset(asset)

            assert isinstance(asset_widget.current_editor, editor_type)

    def test_prefix_root_path(self, qtbot, test_prefix, beat_context):
        asset_widget = AssetWidget()
        qtbot.addWidget(asset_widget)
        asset_widget.set_context(beat_context)

        assert asset_widget.prefix_root_path == test_prefix

    def test_dirty(
        self, qtbot, monkeypatch, test_prefix, beat_context, asset_type_prefix_entry_map
    ):
        asset_widget = AssetWidget()
        qtbot.addWidget(asset_widget)
        asset_widget.set_context(beat_context)

        description = "dummy description"

        # Question about saving editor content after modification before a new json is loaded
        monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.No)

        for (
            asset_type,
            (asset_name, editor_type),
        ) in asset_type_prefix_entry_map.items():
            asset = Asset(test_prefix, asset_type, asset_name)
            with qtbot.waitSignal(asset_widget.currentAssetChanged):
                asset_widget.loadAsset(asset)
            assert not asset_widget.current_editor.isDirty()

            with qtbot.waitSignal(asset_widget.json_widget.textChanged):
                asset_widget.current_editor.description_lineedit.selectAll()
                qtbot.keyClicks(
                    asset_widget.current_editor.description_lineedit, description
                )

            assert asset_widget.save_button.isEnabled()
            assert asset_widget.current_editor.isDirty()

            dumped_json = asset_widget.current_editor.dump_json()
            description_key = "description"
            if asset_type == AssetType.DATAFORMAT:
                description_key = "#" + description_key
            assert dumped_json[description_key] == description

    def test_save(
        self, qtbot, monkeypatch, test_prefix, beat_context, asset_type_prefix_entry_map
    ):
        asset_widget = AssetWidget()
        qtbot.addWidget(asset_widget)
        asset_widget.set_context(beat_context)

        description = "dummy description"

        for (
            asset_type,
            (asset_name, editor_type),
        ) in asset_type_prefix_entry_map.items():
            asset = Asset(test_prefix, asset_type, asset_name)
            with qtbot.waitSignal(asset_widget.currentAssetChanged):
                asset_widget.loadAsset(asset)

            with qtbot.waitSignal(asset_widget.json_widget.textChanged):
                asset_widget.current_editor.description_lineedit.selectAll()
                qtbot.keyClicks(
                    asset_widget.current_editor.description_lineedit, description
                )

            assert asset_widget.save_button.isEnabled()
            qtbot.mouseClick(asset_widget.save_button, QtCore.Qt.LeftButton)
            assert not asset_widget.save_button.isEnabled()

            description_key = "description"
            if asset_type == AssetType.DATAFORMAT:
                description_key = "#" + description_key

            json_data = asset.declaration
            assert json_data[description_key] == description

    def test_new(self, qtbot, monkeypatch, test_prefix, beat_context, asset_type):
        asset_widget = AssetWidget()
        qtbot.addWidget(asset_widget)
        asset_widget.set_context(beat_context)
        asset_name = "test_name"
        user = beat_context.meta["config"].user

        if asset_type.can_create():
            monkeypatch.setattr(
                AssetCreationDialog,
                "getAssetInfo",
                classmethod(
                    lambda *args, **kwargs: (True, AssetCreationDialog.NEW, asset_name)
                ),
            )

            asset_widget.type_editor_map[asset_type].create_action.trigger()

            asset_model = AssetModel()
            asset_model.asset_type = asset_type
            asset_model.prefix_path = test_prefix

            if asset_type.split_count() == 2:
                target_name = f"{user}/{asset_name}/1"
            else:
                target_name = f"{asset_name}/1"
            assert target_name in asset_model.stringList()
            assert os.path.exists(asset_model.json_path(target_name))
        elif asset_type == AssetType.EXPERIMENT:
            toolchain_name = "user/two_loops/1"
            monkeypatch.setattr(
                AssetCreationDialog,
                "getAssetInfo",
                classmethod(
                    lambda *args, **kwargs: (
                        True,
                        AssetCreationDialog.NEW,
                        (toolchain_name, asset_name),
                    )
                ),
            )

            asset_widget.type_editor_map[asset_type].create_action.trigger()

            asset_model = AssetModel()
            asset_model.asset_type = asset_type
            asset_model.prefix_path = test_prefix
            target_name = f"{user}/{toolchain_name}/{asset_name}"

            assert target_name in asset_model.stringList()
            assert asset_widget.save_button.isEnabled()
            qtbot.mouseClick(asset_widget.save_button, QtCore.Qt.LeftButton)

            asset_model.reload()
            assert target_name in asset_model.stringList()
            assert os.path.exists(asset_model.json_path(target_name))

    def test_new_version(
        self,
        qtbot,
        monkeypatch,
        test_prefix,
        beat_context,
        asset_type,
        asset_type_prefix_entry_map,
    ):
        if asset_type.can_create():
            asset_widget = AssetWidget()
            qtbot.addWidget(asset_widget)
            asset_widget.set_context(beat_context)
            asset_name = asset_type_prefix_entry_map[asset_type][0]

            monkeypatch.setattr(
                AssetCreationDialog,
                "getAssetInfo",
                classmethod(
                    lambda *args, **kwargs: (
                        True,
                        AssetCreationDialog.NEW_VERSION,
                        asset_name,
                    )
                ),
            )

            asset_widget.type_editor_map[asset_type].create_action.trigger()

            asset_model = AssetModel()
            asset_model.asset_type = asset_type
            asset_model.prefix_path = test_prefix

            if asset_type.split_count() == 2:
                user_name, name, version = asset_name.split("/")
                target_name = f"{user_name}/{name}/{int(version) + 1}"
            else:
                name, version = asset_name.split("/")
                target_name = f"{name}/{int(version) + 1}"

            assert target_name in asset_model.stringList()
            assert os.path.exists(asset_model.json_path(target_name))

    def test_fork(
        self,
        qtbot,
        monkeypatch,
        test_prefix,
        beat_context,
        asset_type,
        asset_type_prefix_entry_map,
    ):
        if asset_type.can_fork():
            asset_widget = AssetWidget()
            qtbot.addWidget(asset_widget)
            asset_widget.set_context(beat_context)
            asset_name = asset_type_prefix_entry_map[asset_type][0]
            target_name = "forked"
            user = beat_context.meta["config"].user

            monkeypatch.setattr(
                AssetCreationDialog,
                "getAssetInfo",
                classmethod(
                    lambda *args, **kwargs: (
                        True,
                        AssetCreationDialog.FORK,
                        (asset_name, target_name),
                    )
                ),
            )

            asset_widget.type_editor_map[asset_type].create_action.trigger()

            asset_model = AssetModel()
            asset_model.asset_type = asset_type
            asset_model.prefix_path = test_prefix

            if asset_type.split_count() == 2:
                user_name, name, version = asset_name.split("/")
                target_name = f"{user}/{target_name}/{version}"
            elif asset_type.split_count() == 1:
                name, version = asset_name.split("/")
                target_name = f"{target_name}/{version}"
            else:
                items = asset_name.split("/")
                items[0] = user
                items[4] = target_name
                target_name = "/".join(items)

            assert target_name in asset_model.stringList()
            assert os.path.exists(asset_model.json_path(target_name))

    @pytest.mark.parametrize(
        "messagebox_answer", [QMessageBox.Yes, QMessageBox.No], ids=["Yes", "No"]
    )
    def test_delete_asset_in_edition(
        self,
        qtbot,
        monkeypatch,
        test_prefix,
        beat_context,
        asset_type,
        asset_type_prefix_entry_map,
        messagebox_answer,
    ):
        asset_widget = AssetWidget()
        qtbot.addWidget(asset_widget)
        asset_widget.set_context(beat_context)
        asset_name = asset_type_prefix_entry_map[asset_type][0]

        monkeypatch.setattr(QMessageBox, "question", lambda *args: messagebox_answer)

        asset = Asset(test_prefix, asset_type, asset_name)
        with qtbot.waitSignal(asset_widget.currentAssetChanged):
            asset_widget.loadAsset(asset)
        assert asset_widget.current_editor.asset_type != AssetType.UNKNOWN

        asset_widget.deleteAsset(asset.declaration_path)
        if messagebox_answer == QMessageBox.Yes:
            assert asset_widget.current_editor.asset_type == AssetType.UNKNOWN
            assert not os.path.exists(asset.declaration_path)
        else:
            assert asset_widget.current_editor.asset_type != AssetType.UNKNOWN
            assert asset_widget.current_asset == asset
            assert os.path.exists(asset.declaration_path)

    def __check_deletion(
        self, qtbot, beat_context, asset_to_edit, asset_to_delete, messagebox_answer
    ):
        asset_widget = AssetWidget()
        qtbot.addWidget(asset_widget)
        asset_widget.set_context(beat_context)

        with qtbot.waitSignal(asset_widget.currentAssetChanged):
            asset_widget.loadAsset(asset_to_edit)
        assert asset_widget.current_editor.asset_type != AssetType.UNKNOWN

        asset_widget.deleteAsset(asset_to_delete.declaration_path)
        if messagebox_answer == QMessageBox.Yes:
            assert asset_widget.current_editor.asset_type != AssetType.UNKNOWN
            assert os.path.exists(asset_to_edit.declaration_path)
            assert not os.path.exists(asset_to_delete.declaration_path)
        else:
            assert asset_widget.current_editor.asset_type != AssetType.UNKNOWN
            assert asset_widget.current_asset == asset_to_edit
            assert os.path.exists(asset_to_edit.declaration_path)
            assert os.path.exists(asset_to_delete.declaration_path)

    def __get_asset_name_list(self, test_prefix, asset_type):
        asset_model = AssetModel()
        asset_model.setLatestOnlyEnabled(False)
        asset_model.asset_type = asset_type
        asset_model.prefix_path = test_prefix
        asset_list = [
            asset_name
            for asset_name in asset_model.stringList()
            if "error" not in asset_name
        ]

        assert len(asset_list) >= 2

        return asset_list

    @pytest.mark.parametrize(
        "messagebox_answer", [QMessageBox.Yes, QMessageBox.No], ids=["Yes", "No"]
    )
    def test_delete_same_asset_type(
        self,
        qtbot,
        monkeypatch,
        test_prefix,
        beat_context,
        asset_type,
        asset_type_prefix_entry_map,
        messagebox_answer,
    ):
        monkeypatch.setattr(QMessageBox, "question", lambda *args: messagebox_answer)

        asset_name_list = self.__get_asset_name_list(test_prefix, asset_type)

        if asset_type == AssetType.DATAFORMAT:
            # Using lasts assets in the list because of dataformats basetypes
            asset_name_to_edit = asset_name_list[-1]
            asset_name_to_delete = asset_name_list[-2]
        else:
            asset_name_to_edit = asset_name_list[0]
            asset_name_to_delete = asset_name_list[1]

        asset_to_edit = Asset(test_prefix, asset_type, asset_name_to_edit)
        asset_to_delete = Asset(test_prefix, asset_type, asset_name_to_delete)

        self.__check_deletion(
            qtbot, beat_context, asset_to_edit, asset_to_delete, messagebox_answer
        )

    @pytest.mark.parametrize(
        "messagebox_answer", [QMessageBox.Yes, QMessageBox.No], ids=["Yes", "No"]
    )
    def test_delete_other_asset_type(
        self,
        qtbot,
        monkeypatch,
        test_prefix,
        beat_context,
        asset_type,
        asset_type_prefix_entry_map,
        messagebox_answer,
    ):
        monkeypatch.setattr(QMessageBox, "question", lambda *args: messagebox_answer)

        asset_name_list = self.__get_asset_name_list(test_prefix, asset_type)

        index = 0
        if asset_type == AssetType.DATAFORMAT:
            # Using lasts assets in the list because of dataformats basetypes
            index = -1

        asset_name_to_edit = asset_name_list[index]

        asset_to_delete_type = random.choice(
            [
                asset
                for asset in AssetType
                if asset not in [asset_type, AssetType.UNKNOWN]
            ]
        )
        asset_to_delete_name_list = self.__get_asset_name_list(
            test_prefix, asset_to_delete_type
        )
        index = 0
        if asset_to_delete_type == AssetType.DATAFORMAT:
            # Using lasts assets in the list because of dataformats basetypes
            index = -1

        asset_name_to_delete = asset_to_delete_name_list[index]

        asset_to_edit = Asset(test_prefix, asset_type, asset_name_to_edit)
        asset_to_delete = Asset(test_prefix, asset_to_delete_type, asset_name_to_delete)

        self.__check_deletion(
            qtbot, beat_context, asset_to_edit, asset_to_delete, messagebox_answer
        )

    def test_cancel_load_empty_json(
        self,
        qtbot,
        monkeypatch,
        test_prefix,
        beat_context,
        asset_type,
        asset_type_prefix_entry_map,
    ):
        asset_widget = AssetWidget()
        qtbot.addWidget(asset_widget)
        asset_widget.set_context(beat_context)
        asset_name = asset_type_prefix_entry_map[asset_type][0]

        monkeypatch.setattr(
            AssetWidget, "confirm_loading", lambda *args: QMessageBox.Cancel
        )

        asset = Asset(test_prefix, asset_type, asset_name)
        with open(asset.declaration_path, "wt") as declaration_file:
            declaration_file.write("")

        with qtbot.assertNotEmitted(asset_widget.currentAssetChanged):
            asset_widget.loadAsset(asset)

    def test_allow_load_invalid_json(
        self,
        qtbot,
        monkeypatch,
        test_prefix,
        beat_context,
        asset_type,
        asset_type_prefix_entry_map,
    ):
        asset_widget = AssetWidget()
        qtbot.addWidget(asset_widget)
        asset_widget.set_context(beat_context)
        asset_name = asset_type_prefix_entry_map[asset_type][0]

        monkeypatch.setattr(
            AssetWidget, "confirm_loading", lambda *args: QMessageBox.Ignore
        )
        monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.Ok)

        asset = Asset(test_prefix, asset_type, asset_name)
        with open(asset.declaration_path, "wt") as declaration_file:
            json_data = (
                '{"api_version": 2}' if asset_type == AssetType.ALGORITHM else "{}"
            )
            declaration_file.write(json_data)

        with qtbot.waitSignal(asset_widget.currentAssetChanged):
            # import ipdb; ipdb.set_trace()
            asset_widget.loadAsset(asset)

    def test_change_on_disk(
        self,
        qtbot,
        monkeypatch,
        test_prefix,
        beat_context,
        asset_type,
        asset_type_prefix_entry_map,
    ):
        asset_widget = AssetWidget()
        qtbot.addWidget(asset_widget)
        asset_widget.set_context(beat_context)

        asset_name = asset_type_prefix_entry_map[asset_type][0]

        monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.Yes)

        asset = Asset(test_prefix, asset_type, asset_name)
        with qtbot.waitSignal(asset_widget.currentAssetChanged):
            asset_widget.loadAsset(asset)

        asset_widget.save_button.setEnabled(True)
        declaration = asset.declaration
        declaration["description"] = "modified"

        with qtbot.waitSignal(asset_widget.watcher.fileChanged):
            asset.declaration = declaration

        assert not asset_widget.save_button.isEnabled()

    def test_loading_v1_algorithm_refuse_update(
        self, qtbot, monkeypatch, test_prefix, beat_context
    ):
        asset_widget = AssetWidget()
        qtbot.addWidget(asset_widget)
        asset_widget.set_context(beat_context)

        asset_name = "v1/sum/1"

        monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.No)

        asset = Asset(test_prefix, AssetType.ALGORITHM, asset_name)
        with qtbot.assertNotEmitted(asset_widget.currentAssetChanged):
            asset_widget.loadAsset(asset)

    def test_loading_v1_algorithm_accept_update(
        self, qtbot, monkeypatch, test_prefix, beat_context
    ):
        asset_widget = AssetWidget()
        qtbot.addWidget(asset_widget)
        asset_widget.set_context(beat_context)

        asset_name = "v1/sum/1"

        monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.Yes)

        asset = Asset(test_prefix, AssetType.ALGORITHM, asset_name)
        with qtbot.waitSignal(asset_widget.currentAssetChanged):
            asset_widget.loadAsset(asset)

        assert asset_widget.current_asset.name == "v1/sum/2"

    def test_experiment_error_hinting(self, qtbot, test_prefix, beat_context):
        asset_widget = AssetWidget()
        qtbot.addWidget(asset_widget)
        asset_widget.set_context(beat_context)
        asset_name = "user/user/two_loops/1/two_loops"
        asset = Asset(test_prefix, AssetType.EXPERIMENT, asset_name)
        with qtbot.waitSignal(asset_widget.currentAssetChanged):
            asset_widget.loadAsset(asset)

        BLOCK_TO_CHANGE = "offsetter_for_loop_evaluator"
        ALGORITHM_TO_SELECT = "user/string_offsetter/1"

        editor = asset_widget.current_editor.findEditor(BLOCK_TO_CHANGE)

        with qtbot.waitSignal(editor.dataChanged):
            editor.properties_editor.algorithm_combobox.setCurrentText(
                ALGORITHM_TO_SELECT
            )

        assert editor.error_label.toolTip() != ""
