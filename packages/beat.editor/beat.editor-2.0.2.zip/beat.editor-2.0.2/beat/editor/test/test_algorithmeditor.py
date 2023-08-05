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

from beat.backend.python.algorithm import Algorithm

from ..backend.asset import Asset
from ..backend.asset import AssetType
from ..backend.assetmodel import AssetModel
from ..backend.assetmodel import DataFormatModel
from ..widgets.algorithmeditor import ALGORITHM_TYPE
from ..widgets.algorithmeditor import DEFAULT_API_VERSION
from ..widgets.algorithmeditor import DEFAULT_SCHEMA_VERSION
from ..widgets.algorithmeditor import AlgorithmEditor
from ..widgets.algorithmeditor import GroupEditor
from ..widgets.algorithmeditor import IOWidget
from ..widgets.algorithmeditor import ParameterEditor
from ..widgets.algorithmeditor import PropertyEditor
from ..widgets.algorithmeditor import ResultEditor
from ..widgets.algorithmeditor import migrate_to_api_v2
from ..widgets.algorithmeditor import update_code
from .conftest import prefix
from .conftest import sync_prefix


def get_algorithm_declaration(prefix_path, algorithm_name):
    asset = Asset(prefix_path, AssetType.ALGORITHM, algorithm_name)
    return asset.declaration


def get_valid_algorithm(test_prefix):
    sync_prefix()
    model = AssetModel()
    model.asset_type = AssetType.ALGORITHM
    model.prefix_path = test_prefix
    model.setLatestOnlyEnabled(False)
    return [
        algorithm
        for algorithm in model.stringList()
        if all(
            invalid not in algorithm
            for invalid in ["errors", "legacy", "invalid", "v1"]
        )
    ]


@pytest.fixture()
def dataformat_model(test_prefix):
    model = DataFormatModel()
    model.prefix_path = test_prefix
    return model


@pytest.fixture()
def full_dataformat_model(test_prefix):
    model = DataFormatModel()
    model.prefix_path = test_prefix
    model.full_list_enabled = True
    return model


@pytest.fixture(autouse=True)
def synced_prefix():
    """Re sync the prefix between test"""
    sync_prefix()


class TestHelperMethods:
    def test_migration(self, test_prefix):
        algorithm = "v1/sum/1"
        asset = Asset(test_prefix, AssetType.ALGORITHM, algorithm)
        result, new_asset = migrate_to_api_v2(asset)

        assert result
        assert new_asset.name != asset.name

        v1_declaration = asset.declaration
        v2_declaration = new_asset.declaration

        assert v1_declaration != v2_declaration
        assert v2_declaration["schema_version"] == 2
        assert v2_declaration["api_version"] == 2
        assert v2_declaration["type"] == "legacy"

    @pytest.mark.parametrize(
        ["algorithm_name", "new_type", "field_to_add"],
        [
            ("autonomous/add/1", Algorithm.LEGACY, None),
            ("autonomous/add/1", Algorithm.SEQUENTIAL, None),
            ("sequential/add/1", Algorithm.AUTONOMOUS, None),
            ("sequential/add/1", Algorithm.SEQUENTIAL_LOOP_PROCESSOR, None),
            ("sequential/add/1", Algorithm.SEQUENTIAL_LOOP_EVALUATOR, None),
            ("sequential/add/1", Algorithm.AUTONOMOUS_LOOP_PROCESSOR, None),
            ("sequential/add/1", Algorithm.AUTONOMOUS_LOOP_EVALUATOR, None),
            ("autonomous/loop_evaluator/1", Algorithm.SEQUENTIAL, None),
            ("autonomous/loop_evaluator/1", Algorithm.SEQUENTIAL, "results"),
            ("autonomous/add/1", Algorithm.SEQUENTIAL, "results"),
        ],
    )
    def test_code_update(self, test_prefix, algorithm_name, new_type, field_to_add):
        asset = Asset(test_prefix, AssetType.ALGORITHM, algorithm_name)

        with open(asset.code_path, "rt") as code_file:
            original_code = code_file.read()

        declaration = asset.declaration
        declaration["type"] = new_type
        if field_to_add:
            declaration[field_to_add] = None

        asset.declaration = declaration
        update_code(asset)

        with open(asset.code_path, "rt") as code_file:
            updated_code = code_file.read()

        assert updated_code != original_code


class TestPropertyEditor:
    """Test that the algorithm properties editor works as expected"""

    @pytest.mark.parametrize("algorithm", get_valid_algorithm(prefix))
    def test_load_and_dump(self, qtbot, test_prefix, algorithm):
        reference_json = get_algorithm_declaration(test_prefix, algorithm)

        editor = PropertyEditor()
        qtbot.addWidget(editor)
        editor.load(reference_json)

        reference_json.pop("groups", None)
        reference_json.pop("parameters", None)
        reference_json.pop("results", None)
        reference_json.pop("uses", None)

        assert editor.dump() == reference_json

    def test_default_dump(self, qtbot):
        editor = PropertyEditor()
        qtbot.addWidget(editor)

        assert editor.dump() == {
            "language": "unknown",
            "api_version": DEFAULT_API_VERSION,
            "type": Algorithm.SEQUENTIAL,
            "schema_version": DEFAULT_SCHEMA_VERSION,
            "splittable": False,
        }

    def test_splittable(self, qtbot):
        editor = PropertyEditor()
        qtbot.addWidget(editor)
        assert editor.canBeSplitable()
        assert editor.splittable_checkbox.isEnabled()

        # Make the list in an order different than the one they were put in the
        # group otherwise, dataChanged won't be emitted
        for button in [
            editor.sequential_loop_processor_radiobutton,
            editor.autonomous_loop_processor_radiobutton,
            editor.autonomous_radiobutton,
            editor.sequential_radiobutton,
        ]:
            with qtbot.waitSignal(editor.dataChanged):
                button.toggle()
                assert editor.canBeSplitable()

        for radiobutton in [
            editor.sequential_loop_evaluator_radiobutton,
            editor.autonomous_loop_evaluator_radiobutton,
        ]:
            with qtbot.waitSignal(editor.dataChanged):
                radiobutton.toggle()

            assert not editor.canBeSplitable()
            assert not editor.splittable_checkbox.isEnabled()

        with qtbot.waitSignal(editor.dataChanged):
            editor.analyzer_checkbox.toggle()

        assert not editor.canBeSplitable()

    def test_has_outputs(self, qtbot):
        editor = PropertyEditor()
        qtbot.addWidget(editor)
        assert editor.hasOutputs()

        with qtbot.waitSignal(editor.dataChanged):
            editor.analyzer_checkbox.toggle()
        assert not editor.hasOutputs()

        with qtbot.waitSignal(editor.dataChanged):
            editor.analyzer_checkbox.toggle()
        assert editor.hasOutputs()

        buttons = editor.button_group.buttons()
        buttons.append(buttons.pop(buttons.index(editor.button_group.checkedButton())))
        for button in buttons:
            with qtbot.waitSignal(editor.dataChanged):
                button.toggle()
            assert editor.hasOutputs()

    @pytest.mark.parametrize(
        ["algorithm_type", "has_loop"],
        [
            (Algorithm.SEQUENTIAL, False),
            (Algorithm.AUTONOMOUS, False),
            (Algorithm.AUTONOMOUS_LOOP_PROCESSOR, True),
            (Algorithm.SEQUENTIAL_LOOP_PROCESSOR, True),
            (Algorithm.AUTONOMOUS_LOOP_EVALUATOR, True),
            (Algorithm.SEQUENTIAL_LOOP_EVALUATOR, True),
        ],
    )
    def test_has_loop(self, qtbot, algorithm_type, has_loop):
        editor = PropertyEditor()
        qtbot.addWidget(editor)
        assert not editor.hasLoop()

        for button in editor.button_group.buttons():
            if button.property(ALGORITHM_TYPE) == algorithm_type:
                button.setChecked(True)
                break

        assert editor.hasLoop() == has_loop

    @pytest.mark.parametrize(
        ["algorithm_type", "schema_version"],
        [
            (Algorithm.SEQUENTIAL, DEFAULT_SCHEMA_VERSION),
            (Algorithm.AUTONOMOUS, DEFAULT_SCHEMA_VERSION),
            (Algorithm.SEQUENTIAL_LOOP_PROCESSOR, 3),
            (Algorithm.AUTONOMOUS_LOOP_PROCESSOR, 3),
            (Algorithm.SEQUENTIAL_LOOP_EVALUATOR, 3),
            (Algorithm.AUTONOMOUS_LOOP_EVALUATOR, 3),
        ],
    )
    def test_schema_version(self, qtbot, algorithm_type, schema_version):
        editor = PropertyEditor()
        qtbot.addWidget(editor)

        for button in editor.button_group.buttons():
            if button.property(ALGORITHM_TYPE) == algorithm_type:
                button.setChecked(True)
                break

        assert editor.dump().get("schema_version") == schema_version


class TestParameterEditor:
    """Test that the algorithm parameter editor works as expected"""

    @pytest.mark.parametrize("algorithm", get_valid_algorithm(prefix))
    def test_load_and_dump(self, qtbot, test_prefix, algorithm):
        reference_json = get_algorithm_declaration(test_prefix, algorithm)

        parameters = reference_json.pop("parameters", {})
        editor = ParameterEditor()
        qtbot.addWidget(editor)

        for _, parameter in parameters.items():
            editor.load(parameter)
            assert editor.dump() == parameter

    def test_name(self, qtbot):
        editor = ParameterEditor()
        qtbot.addWidget(editor)
        new_name = "test"
        with qtbot.waitSignal(editor.dataChanged):
            editor.setName(new_name)

        assert editor.name() == new_name


class TestResultEditor:
    """Test that the algorithm result editor works as expected"""

    @pytest.fixture()
    def editor(self, qtbot, full_dataformat_model):
        editor = ResultEditor(full_dataformat_model)
        qtbot.addWidget(editor)
        return editor

    @pytest.mark.parametrize("algorithm", get_valid_algorithm(prefix))
    def test_load_and_dump(self, qtbot, test_prefix, editor, algorithm):
        reference_json = get_algorithm_declaration(test_prefix, algorithm)

        results = reference_json.pop("results", {})

        for _, result in results.items():
            editor.load(result)
            assert editor.dump() == result

    def test_name(self, qtbot, editor):
        new_name = "test"
        with qtbot.waitSignal(editor.dataChanged):
            editor.setName(new_name)

        assert editor.name() == new_name

    def test_type_change(self, qtbot, editor):
        model = editor.type_combobox.model()
        dataformat = model.index(1, 0).data()
        with qtbot.waitSignal(editor.dataChanged):
            editor.type_combobox.setCurrentIndex(1)
        assert editor.dump()["type"] == dataformat

    def test_display_change(self, qtbot, editor):
        assert not editor.dump()["display"]

        with qtbot.waitSignal(editor.dataChanged):
            editor.display_checkbox.toggle()

        assert editor.dump()["display"]

        with qtbot.waitSignal(editor.dataChanged):
            editor.display_checkbox.toggle()

        assert not editor.dump()["display"]


class TestIOWidget(object):
    """Tests for the widget for input output handling"""

    @pytest.fixture()
    def editor(self, qtbot, dataformat_model):
        editor = IOWidget("Test", dataformat_model)
        qtbot.addWidget(editor)
        return editor

    @pytest.mark.parametrize("algorithm", get_valid_algorithm(prefix))
    def test_load_and_dump(self, qtbot, test_prefix, dataformat_model, algorithm):
        reference_json = get_algorithm_declaration(test_prefix, algorithm)

        groups = reference_json.pop("groups", {})

        for group in groups:
            inputs = group.get("inputs", {})
            outputs = group.get("outputs", {})

            editor = IOWidget("Test", dataformat_model)
            qtbot.addWidget(editor)
            editor.load(inputs)
            assert editor.dump() == inputs
            editor.load(outputs)
            assert editor.dump() == outputs

    def test_add_entry(self, qtbot, test_prefix, editor):
        assert len(editor.dump()) == 0

        with qtbot.waitSignal(editor.dataChanged):
            qtbot.mouseClick(editor.add_button, QtCore.Qt.LeftButton)

        assert len(editor.dump()) == 1

    def test_remove_entry(self, qtbot, test_prefix, editor, dataformat_model):
        assert not editor.remove_button.isEnabled()

        editor.load({"Test": {"type": dataformat_model.stringList()[0]}})

        assert not editor.remove_button.isEnabled()

        with qtbot.waitSignal(editor.tablewidget.itemSelectionChanged):
            editor.tablewidget.selectRow(0)

        assert editor.remove_button.isEnabled()

        qtbot.mouseClick(editor.remove_button, QtCore.Qt.LeftButton)

        assert len(editor.dump()) == 0

        assert not editor.remove_button.isEnabled()


class TestGroupEditor:
    """Test that the algorithm group editor works as expected"""

    @pytest.mark.parametrize("algorithm", get_valid_algorithm(prefix))
    def test_load_and_dump(self, qtbot, test_prefix, algorithm):
        reference_json = get_algorithm_declaration(test_prefix, algorithm)

        model = AssetModel()
        model.asset_type = AssetType.DATAFORMAT
        model.prefix_path = test_prefix

        groups = reference_json.pop("groups", {})
        editor = GroupEditor(model)
        qtbot.addWidget(editor)
        is_loop = reference_json.get("type") in [
            Algorithm.SEQUENTIAL_LOOP_PROCESSOR,
            Algorithm.AUTONOMOUS_LOOP_PROCESSOR,
            Algorithm.SEQUENTIAL_LOOP_EVALUATOR,
            Algorithm.AUTONOMOUS_LOOP_EVALUATOR,
        ]
        has_no_output = "results" in reference_json
        for index, group in enumerate(groups):
            editor.load(group)
            if not has_no_output:
                editor.setOutputsEnabled(index == 0)
            else:
                editor.setOutputsEnabled(False)

            editor.setLoopEnabled(is_loop)
            assert editor.dump() == group


class TestAlgorithmEditor:
    """Test that the mock editor works correctly"""

    @pytest.mark.parametrize("algorithm", get_valid_algorithm(prefix))
    def test_load_and_dump(self, qtbot, beat_context, test_prefix, algorithm):
        reference_json = get_algorithm_declaration(test_prefix, algorithm)
        editor = AlgorithmEditor()
        qtbot.addWidget(editor)
        editor.set_context(beat_context)
        editor.load_json(reference_json)

        dump = editor.dump_json()

        if editor.property_editor.isAnalyzer():
            assert "results" in dump
            assert "splittable" not in dump

        assert dump == reference_json
