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

import random

import pytest

from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from ..backend.assetmodel import DataFormatModel
from ..widgets.dataformateditor import DataformatArrayWidget
from ..widgets.dataformateditor import DataformatBaseWidget
from ..widgets.dataformateditor import DataformatEditor
from ..widgets.dataformateditor import DataformatObjectWidget
from ..widgets.dataformateditor import DataformatWidget
from ..widgets.dataformateditor import default_dataformat
from ..widgets.dataformateditor import default_object_dataformat
from ..widgets.dialogs import NameInputDialog


@pytest.fixture()
def dataformat_model(test_prefix):
    asset_model = DataFormatModel()
    asset_model.full_list_enabled = True
    asset_model.prefix_path = test_prefix
    return asset_model


def get_random_dataformat(dataformat_model):
    index = random.randint(0, dataformat_model.rowCount() - 1)
    model_index = dataformat_model.index(index, 0)
    return model_index.data()


class TestDataformatBaseWidget:
    """Test the common functionality of the various editors base widget"""

    def test_folding(self, qtbot):
        widget = DataformatBaseWidget()
        qtbot.addWidget(widget)
        widget.show()

        with qtbot.waitSignal(widget.name_widget.foldToggled):
            widget.name_widget.fold_button.toggle()

        assert not widget.content_widget.isVisible()

        with qtbot.waitSignal(widget.name_widget.foldToggled):
            widget.name_widget.fold_button.toggle()

        assert widget.content_widget.isVisible()


class TestDataformatWidget:
    """Test that the mock editor works correctly"""

    def test_load_and_dump(self, qtbot, dataformat_model):
        name = "test"
        value = get_random_dataformat(dataformat_model)
        reference_json = {name: value}

        editor = DataformatWidget(dataformat_model)
        qtbot.addWidget(editor)

        editor.load(None, value)

        assert editor.dump() == value

        editor.load(name, value)

        assert editor.dump() == reference_json


class TestDataformatObjectWidget:
    """Test that the mock editor works correctly"""

    @pytest.fixture()
    def df_object_editor(self, qtbot, dataformat_model):
        editor = DataformatObjectWidget(dataformat_model)
        qtbot.addWidget(editor)
        return editor

    def test_load_and_dump(self, df_object_editor, dataformat_model):
        name = "test"
        dataformat = get_random_dataformat(dataformat_model)

        value = {"key": dataformat}
        reference_json = {name: value}

        df_object_editor.load(None, value)

        assert df_object_editor.dump() == value

        df_object_editor.load(name, value)

        assert df_object_editor.dump() == reference_json

    def test_canceled_add(self, df_object_editor, monkeypatch):
        reference_json = {}

        monkeypatch.setattr(
            NameInputDialog, "getText", classmethod(lambda *args: (None, False))
        )
        df_object_editor.add_type_action.trigger()

        assert df_object_editor.dump() == reference_json

    def test_add_and_remove(
        self, qtbot, df_object_editor, monkeypatch, dataformat_model
    ):
        model_index = dataformat_model.index(0, 0)
        value = model_index.data()
        reference_json = {"test_type": value}

        monkeypatch.setattr(
            NameInputDialog, "getText", classmethod(lambda *args: ("test_type", True))
        )
        df_object_editor.add_type_action.trigger()

        assert df_object_editor.dump() == reference_json

        monkeypatch.setattr(
            NameInputDialog, "getText", classmethod(lambda *args: ("test_object", True))
        )
        df_object_editor.add_object_action.trigger()
        reference_json["test_object"] = default_object_dataformat()

        assert df_object_editor.dump() == reference_json

        monkeypatch.setattr(
            NameInputDialog,
            "getText",
            classmethod(lambda *args: ("test_type_array", True)),
        )
        df_object_editor.add_type_array_action.trigger()
        reference_json["test_type_array"] = [0, DEFAULT_TYPE]

        assert df_object_editor.dump() == reference_json

        monkeypatch.setattr(
            NameInputDialog,
            "getText",
            classmethod(lambda *args: ("test_object_array", True)),
        )
        df_object_editor.add_object_array_action.trigger()
        reference_json["test_object_array"] = [0, default_object_dataformat()]

        assert df_object_editor.dump() == reference_json

        for item in ["test_object_array", "test_type_array", "test_type"]:
            reference_json.pop(item)

            sub_editor = None
            for widget in df_object_editor.dataformat_widgets:
                if widget.name() == item:
                    sub_editor = widget
                    break

            assert sub_editor is not None
            with qtbot.waitSignal(df_object_editor.dataChanged):
                delete_button = sub_editor.name_widget.delete_button
                qtbot.mouseClick(delete_button, Qt.LeftButton)

            assert df_object_editor.dump() == reference_json

    def test_invalid_load_parameter(self, df_object_editor):
        with pytest.raises(TypeError):
            df_object_editor.load("invalid", None)


class TestDataformatArrayWidget:
    """Test that the mock editor works correctly"""

    @pytest.fixture()
    def df_array_editor(self, qtbot, dataformat_model):
        editor = DataformatArrayWidget(dataformat_model)
        qtbot.addWidget(editor)
        return editor

    def test_load_and_dump(self, df_array_editor, dataformat_model):
        name = "test"
        dataformat = get_random_dataformat(dataformat_model)

        value = [0, {"key": dataformat}]
        reference_json = {name: value}

        df_array_editor.load(None, value)

        assert df_array_editor.dump() == value

        df_array_editor.load(name, value)

        assert df_array_editor.dump() == reference_json

    def test_dimension(self, qtbot, df_array_editor, dataformat_model):
        model_index = dataformat_model.index(0, 0)
        dataformat = model_index.data()
        value = [0, dataformat]

        df_array_editor.load(None, value)

        assert df_array_editor.dump() == value

        qtbot.mouseClick(df_array_editor.add_dimension_button, QtCore.Qt.LeftButton)

        assert df_array_editor.dump() == [0, 0, dataformat]

        with qtbot.waitSignal(df_array_editor.dataChanged):
            df_array_editor.dimension_widgets[0].setValue(12)

        with qtbot.waitSignal(df_array_editor.dataChanged):
            df_array_editor.dimension_widgets[1].setValue(13)

        assert df_array_editor.dump() == [12, 13, dataformat]

        qtbot.mouseClick(
            df_array_editor.dimension_widgets[-1].name_widget.delete_button,
            QtCore.Qt.LeftButton,
        )

        assert df_array_editor.dump() == [12, dataformat]

    def test_invalid_load_parameter(self, df_array_editor):
        with pytest.raises(TypeError):
            df_array_editor.load("invalid", None)

        with pytest.raises(ValueError):
            df_array_editor.load("invalid", [0, []])


DEFAULT_TYPE = default_dataformat()


class TestDataformatEditor:
    """Test that the mock editor works correctly"""

    @pytest.fixture()
    def df_editor(self, qtbot, beat_context):
        editor = DataformatEditor()
        qtbot.addWidget(editor)
        editor.set_context(beat_context)
        return editor

    @pytest.mark.parametrize(
        "reference_json",
        [
            {"#description": "test"},
            {"#extends": "test/test/1"},
            {"#schema_version": 1},
            {"#description": "test", "#extends": "test/test/1"},
            {"#description": "test", "#schema_version": 1},
            {"#extends": "test/test/1", "#schema_version": 1},
            {"#description": "test", "#extends": "test/test/1", "#schema_version": 1},
        ],
    )
    def test_load_and_dump_meta_data(self, df_editor, reference_json):
        df_editor.load_json(reference_json)

        assert df_editor.dump_json() == reference_json
        validated, errors = df_editor.is_valid()
        assert validated, errors

    @pytest.mark.parametrize(
        "reference_json",
        [
            {"type": DEFAULT_TYPE},
            {"object": {"test1": DEFAULT_TYPE}},
            {"list": [0, DEFAULT_TYPE]},
            {"array": [0, 0, DEFAULT_TYPE]},
            {"list_of_object": [0, {"test1": DEFAULT_TYPE}]},
            {"array_of_object": [0, 0, {"test1": DEFAULT_TYPE}]},
        ],
    )
    def test_load_and_dump_data(self, monkeypatch, df_editor, reference_json):
        df_editor.load_json(reference_json)

        assert df_editor.dump_json() == reference_json
        validated, errors = df_editor.is_valid()
        assert validated, errors

    def test_canceled_add(self, df_editor, monkeypatch):
        reference_json = {}

        monkeypatch.setattr(
            NameInputDialog, "getText", classmethod(lambda *args: (None, False))
        )
        df_editor.add_type_action.trigger()

        assert df_editor.dump_json() == reference_json

    def test_add_and_remove(self, qtbot, monkeypatch, df_editor, dataformat_model):
        model_index = dataformat_model.index(0, 0)
        value = model_index.data()

        monkeypatch.setattr(
            NameInputDialog, "getText", classmethod(lambda *args: ("test_type", True))
        )
        df_editor.add_type_action.trigger()
        reference_json = {"test_type": value}

        assert df_editor.dump_json() == reference_json
        validated, errors = df_editor.is_valid()
        assert validated, errors

        monkeypatch.setattr(
            NameInputDialog, "getText", classmethod(lambda *args: ("test_object", True))
        )
        df_editor.add_object_action.trigger()
        reference_json["test_object"] = default_object_dataformat()

        assert df_editor.dump_json() == reference_json
        validated, errors = df_editor.is_valid()
        assert validated, errors

        monkeypatch.setattr(
            NameInputDialog,
            "getText",
            classmethod(lambda *args: ("test_type_array", True)),
        )
        df_editor.add_type_array_action.trigger()
        reference_json["test_type_array"] = [0, DEFAULT_TYPE]

        assert df_editor.dump_json() == reference_json
        validated, errors = df_editor.is_valid()
        assert validated, errors

        monkeypatch.setattr(
            NameInputDialog,
            "getText",
            classmethod(lambda *args: ("test_object_array", True)),
        )
        df_editor.add_object_array_action.trigger()
        reference_json["test_object_array"] = [0, default_object_dataformat()]

        assert df_editor.dump_json() == reference_json
        validated, errors = df_editor.is_valid()
        assert validated, errors

        for item in ["test_object_array", "test_type_array", "test_type"]:
            reference_json.pop(item)

            type_editor = None
            for subeditor in df_editor.scroll_widget.widget_list:
                if subeditor.name() == item:
                    type_editor = subeditor
                    break

            assert type_editor is not None
            with qtbot.waitSignal(df_editor.dataChanged):
                delete_button = type_editor.name_widget.delete_button
                qtbot.mouseClick(delete_button, Qt.LeftButton)

            assert df_editor.dump_json() == reference_json
            validated, errors = df_editor.is_valid()
            assert validated, errors
