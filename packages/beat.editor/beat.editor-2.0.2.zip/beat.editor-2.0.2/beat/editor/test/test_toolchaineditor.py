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
import simplejson as json

from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsView

from ..backend.asset import Asset
from ..backend.asset import AssetType
from ..backend.assetmodel import AssetModel
from ..widgets.toolchaineditor import BlockType
from ..widgets.toolchaineditor import LoopWidget
from ..widgets.toolchaineditor import ToolchainEditor
from ..widgets.toolchaineditor import ToolchainView
from ..widgets.toolchainscene import ToolchainScene
from .conftest import prefix
from .conftest import sync_prefix


def toolchain_config():
    file_ = QFile(":/resources/toolchain_style_config")
    is_open = file_.open(QFile.ReadOnly | QFile.Text)
    assert is_open
    return json.loads(file_.readAll().data().decode("utf-8"))


@pytest.fixture()
def scene_config():
    return toolchain_config()["toolchainscene_config"]


def get_toolchain_declaration(prefix_path, asset_name):
    asset = Asset(prefix_path, AssetType.TOOLCHAIN, asset_name)
    return asset.declaration


def get_valid_toolchains(test_prefix):
    sync_prefix()
    model = AssetModel()
    model.asset_type = AssetType.TOOLCHAIN
    model.prefix_path = test_prefix
    model.setLatestOnlyEnabled(False)
    return [
        toolchain
        for toolchain in model.stringList()
        if all(invalid not in toolchain for invalid in ["errors"])
    ]


def get_valid_block_types():
    return ["datasets", "blocks", "analyzers", "loops"]


def get_invalid_block_types():
    return ["invalid_1", "invalid_2"]


class TestToolchainScene:
    def test_good_init(self, qtbot, scene_config):
        scene = ToolchainScene(scene_config)
        assert isinstance(scene, QGraphicsScene)
        assert scene.grid_size == scene_config["grid_size"]
        assert scene.grid_color == scene_config["grid_color"]

    def test_bad_init(self, qtbot, scene_config):
        configuration = {"bad": 1000}
        scene = ToolchainScene(configuration)
        assert isinstance(scene, QGraphicsScene)
        assert scene.grid_size == scene_config["grid_size"]
        assert scene.grid_color == scene_config["grid_color"]

    @pytest.mark.parametrize(
        ["input_parameter", "test_input", "expected_exception_message"],
        [
            ("grid_size", 1000.0, "Grid size configuration has to be of type integer"),
            ("grid_color", "blue", "Grid color configuration has to be of type list"),
            ("grid_color", [220, 220], "Invalid grid element types or unmatching size"),
            (
                "grid_color",
                [220, 220, 220.0],
                "Invalid grid element types or unmatching size",
            ),
        ],
    )
    def test_bad_grid_config(
        self, qtbot, input_parameter, test_input, expected_exception_message
    ):
        configuration = {input_parameter: test_input}
        with pytest.raises(TypeError) as excinfo:
            ToolchainScene(configuration)
        assert str(excinfo.value) == expected_exception_message

    @pytest.mark.parametrize("toolchain", get_valid_toolchains(prefix))
    def test_add_scene_to_view(self, qtbot, toolchain, scene_config):
        scene = ToolchainScene(scene_config)
        toolchainview = ToolchainView(toolchain)
        assert toolchainview.scene() is None

        toolchainview.setScene(scene)
        assert toolchainview.scene() == scene
        assert isinstance(toolchainview, QGraphicsView)
        assert isinstance(scene, QGraphicsScene)


class TestBlockType:
    """Test the BlockType enum class"""

    @pytest.mark.parametrize("block_type", get_valid_block_types())
    def test_valid_block_type(self, qtbot, block_type):
        block_type_name = block_type.upper()
        assert any([block_type_name == type_.name for type_ in BlockType])

    @pytest.mark.parametrize("block_type", get_invalid_block_types())
    def test_invalid_block_type(self, qtbot, block_type):
        block_type_name = block_type.upper()
        assert not any([block_type_name == type_.name for type_ in BlockType])

    @pytest.mark.parametrize("block_type", get_valid_block_types())
    def test_valid_block_type_from_name(self, qtbot, block_type):
        name = block_type.upper()
        created_block_type = BlockType.from_name(name)
        assert isinstance(created_block_type, BlockType)
        assert created_block_type.name == name

    @pytest.mark.parametrize("block_type", get_invalid_block_types())
    def test_invalid_block_type_from_name(self, qtbot, block_type):
        name = block_type.upper()
        with pytest.raises(KeyError) as excinfo:
            BlockType.from_name(name)
        assert "{} is not a valid block type".format(name) in str(excinfo.value)


class TestLoopWidget:
    """Test that the LoopWidget works correctly"""

    def test_empty_block_list(self, qtbot, beat_context):
        widget = LoopWidget()

        for listwidget in [
            widget.sequential_loop_processor_listwidget,
            widget.autonomous_loop_processor_listwidget,
            widget.sequential_loop_evaluator_listwidget,
            widget.sequential_loop_evaluator_listwidget,
        ]:
            assert listwidget.count() == 1
            assert listwidget.item(0).text() == "No valid algorithm found"


class TestToolchainEditor:
    """Test that the mock editor works correctly"""

    @pytest.mark.parametrize("toolchain", get_valid_toolchains(prefix))
    def test_load_and_dump(self, qtbot, test_prefix, toolchain):

        reference_json = get_toolchain_declaration(test_prefix, toolchain)
        editor = ToolchainEditor()

        editor.load_json(reference_json)

        assert editor.dump_json() == reference_json

    def test_empty_block_list(self, qtbot):
        editor = ToolchainEditor()

        actions = editor.toolchain.analyzer_edit_menu.actions()
        assert len(actions) == 1
        assert actions[0].text() == "No valid analyzers found"
        actions = editor.toolchain.block_edit_menu.actions()
        assert len(actions) == 1
        assert actions[0].text() == "No valid blocks found"
        actions = editor.toolchain.dataset_edit_menu.actions()
        assert len(actions) == 1
        assert actions[0].text() == "No valid datasets found"
