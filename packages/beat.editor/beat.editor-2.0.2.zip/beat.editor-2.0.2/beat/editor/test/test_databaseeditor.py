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

from PyQt5 import QtCore
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QInputDialog

from ..backend.asset import Asset
from ..backend.asset import AssetType
from ..widgets.databaseeditor import DatabaseEditor
from ..widgets.databaseeditor import DatabaseWidget
from ..widgets.databaseeditor import ParameterTypeDelegate
from ..widgets.databaseeditor import ProtocolDialog
from ..widgets.databaseeditor import ProtocolEditor
from ..widgets.databaseeditor import ViewEditor
from ..widgets.databaseeditor import ViewsEditor


@pytest.yield_fixture(params=[i for i in range(1, 3)])
def test_database(request):
    yield "simple/{}".format(request.param)


@pytest.yield_fixture(
    params=[
        {},
        {"test_string": "test string", "test_number": 12.0, "test_boolean": True},
    ]
)
def reference_view_json(request):
    parameters = request.param

    reference_json = {"view": "testing_view"}

    if parameters:
        reference_json["parameters"] = parameters

    yield reference_json


@pytest.fixture()
def reference_database_json(test_prefix):
    asset = Asset(test_prefix, AssetType.DATABASE, "simple/2")
    return asset.declaration


@pytest.fixture()
def reference_viewseditor_data(request, reference_database_json):
    protocol = reference_database_json["protocols"][0]
    return protocol["template"], protocol["views"]


@pytest.fixture()
def reference_protocols(request, reference_database_json):
    return reference_database_json["protocols"]


TYPE_VALUES_DICT = {"boolean": True, "number": 0, "string": "Change_me"}


# ------------------------------------------------------------------------------


class ParameterTypeTestDelegate(ParameterTypeDelegate):
    def createEditor(self, parent, options, index):
        """Force commit to model on index change, otherwise testing won't work"""

        combobox = super().createEditor(parent, options, index)
        combobox.currentIndexChanged.connect(lambda: self.commitData.emit(combobox))
        return combobox


@pytest.fixture()
def view_editor(qtbot, reference_view_json):
    editor = ViewEditor()
    qtbot.addWidget(editor)
    editor.load(reference_view_json)
    return editor


class TestViewEditor:
    """Test that the view editor works correctly"""

    def test_load_and_dump(self, qtbot, view_editor, reference_view_json):
        assert view_editor.dump() == reference_view_json

    def test_add_parameter(self, qtbot, view_editor, reference_view_json):
        with qtbot.waitSignal(view_editor.dataChanged):
            qtbot.mouseClick(view_editor.add_button, QtCore.Qt.LeftButton)

        if "parameters" not in reference_view_json:
            reference_view_json["parameters"] = {}
        reference_view_json["parameters"]["Name_me"] = "Change_me"

        assert view_editor.dump() == reference_view_json

    def test_remove_parameter(self, qtbot, view_editor, reference_view_json):
        assert not view_editor.remove_button.isEnabled()

        if "parameters" in reference_view_json:

            view_editor.parameters_tablewidget.setCurrentCell(0, 0)

            assert view_editor.remove_button.isEnabled()

            with qtbot.waitSignal(view_editor.dataChanged):
                qtbot.mouseClick(view_editor.remove_button, QtCore.Qt.LeftButton)

    def test_modify_name(self, qtbot, view_editor, reference_view_json):
        new_name = "new_name"

        with qtbot.waitSignal(view_editor.dataChanged):
            qtbot.keyClicks(view_editor.view_name_lineedit, new_name)

        reference_view_json["view"] += new_name

        assert view_editor.dump() == reference_view_json

    @pytest.mark.parametrize("value", TYPE_VALUES_DICT.values())
    @pytest.mark.parametrize("new_type, new_value", TYPE_VALUES_DICT.items())
    def test_modify_parameter_type(
        self, qtbot, view_editor, value, new_type, new_value
    ):
        reference_json = {"view": "test", "parameters": {"test_param": value}}
        new_json = copy.deepcopy(reference_json)
        new_json["parameters"] = {"test_param": new_value}

        view_editor.load(reference_json)
        type_delegate = ParameterTypeTestDelegate(
            view_editor.parameter_type_model, view_editor
        )
        view_editor.parameters_tablewidget.setItemDelegateForColumn(1, type_delegate)
        type_item = view_editor.parameters_tablewidget.item(0, 1)

        def __do_edit():
            view_editor.parameters_tablewidget.openPersistentEditor(type_item)
            combobox = view_editor.findChildren(QComboBox)[0]
            combobox.setCurrentText(new_type)
            view_editor.parameters_tablewidget.closePersistentEditor(type_item)

        if type_item.text() != new_type:
            with qtbot.waitSignal(view_editor.parameters_tablewidget.itemChanged):
                __do_edit()
        else:
            __do_edit()

        assert view_editor.dump() == new_json


# ------------------------------------------------------------------------------


@pytest.fixture()
def views_editor(qtbot, test_prefix):
    editor = ViewsEditor()
    qtbot.addWidget(editor)
    editor.setPrefixPath(test_prefix)
    return editor


class TestViewsEditor:
    """Test that the views editor works correctly"""

    @staticmethod
    def setup_editor(editor, protocol, views):
        editor.protocol = protocol
        editor.load(views)
        return editor

    def test_load_and_dump(self, views_editor, reference_viewseditor_data):
        protocol, views_json = reference_viewseditor_data
        self.setup_editor(views_editor, protocol, views_json)

        assert views_editor.dump() == views_json

    def test_add_view(
        self, qtbot, monkeypatch, views_editor, reference_viewseditor_data
    ):
        protocol, views_json = reference_viewseditor_data
        views_json.pop(next(iter(views_json)))
        self.setup_editor(views_editor, protocol, views_json)

        available_sets = views_editor.available_sets()
        monkeypatch.setattr(
            QInputDialog,
            "getItem",
            classmethod(lambda *args, **kwargs: (available_sets[0], True)),
        )

        with qtbot.waitSignal(views_editor.dataChanged):
            qtbot.mouseClick(views_editor.add_view_button, QtCore.Qt.LeftButton)

        assert len(views_editor.view_editors) == len(views_json) + 1

    def test_remove_view(self, qtbot, views_editor, reference_viewseditor_data):
        protocol, views_json = reference_viewseditor_data
        self.setup_editor(views_editor, protocol, views_json)

        view_editor = views_editor.view_editors[-1]

        with qtbot.waitSignal(views_editor.dataChanged):
            qtbot.mouseClick(view_editor.delete_button, QtCore.Qt.LeftButton)

        assert len(views_editor.view_editors) == len(views_json) - 1


# ------------------------------------------------------------------------------


class TestProtocolEditor:
    """Test that the protocol editor works correctly"""

    def test_load_and_dump(self, qtbot, test_prefix, reference_database_json):
        protocol_editor = ProtocolEditor()
        qtbot.addWidget(protocol_editor)
        protocol_editor.setPrefixPath(test_prefix)

        for protocol in reference_database_json["protocols"]:
            protocol_editor.load(protocol)
            assert protocol_editor.dump() == protocol


# ------------------------------------------------------------------------------


@pytest.fixture()
def database_widget(qtbot, test_prefix):
    editor = DatabaseWidget()
    qtbot.addWidget(editor)
    editor.setPrefixPath(test_prefix)
    return editor


class TestDatabaseWidget:
    """Test that the database widget works correctly"""

    def test_load_and_dump(self, database_widget, reference_database_json):
        database_widget.load(reference_database_json)
        reference_database_json.pop("schema_version")
        assert database_widget.dump() == reference_database_json

    def test_add_protocol(
        self, qtbot, monkeypatch, database_widget, reference_database_json
    ):
        database_widget.load(reference_database_json)
        name = "test_protocol"
        protocol = database_widget.protocoltemplate_model.stringList()[0]

        monkeypatch.setattr(
            ProtocolDialog,
            "getProtocol",
            classmethod(lambda *args, **kwargs: (name, protocol, True)),
        )

        with qtbot.waitSignal(database_widget.dataChanged):
            qtbot.mouseClick(database_widget.add_protocol_button, QtCore.Qt.LeftButton)

        assert (
            len(database_widget.protocol_editors)
            == len(reference_database_json["protocols"]) + 1
        )

        reference_database_json.pop("schema_version")
        new_protocol = {"name": name, "template": protocol, "views": {}}
        reference_database_json["protocols"].append(new_protocol)
        assert database_widget.dump() == reference_database_json

    def test_remove_protocol(self, qtbot, database_widget, reference_database_json):
        database_widget.load(reference_database_json)

        protocol_editor = database_widget.protocol_editors[-1]

        with qtbot.waitSignal(database_widget.dataChanged):
            qtbot.mouseClick(protocol_editor.delete_button, QtCore.Qt.LeftButton)

        assert (
            len(database_widget.protocol_editors)
            == len(reference_database_json["protocols"]) - 1
        )

        reference_database_json.pop("schema_version")
        reference_database_json["protocols"].pop(-1)
        assert database_widget.dump() == reference_database_json


# ------------------------------------------------------------------------------


class TestDatabaseEditor:
    """Test that the database editor works correctly"""

    def test_load_and_dump(self, qtbot, beat_context, test_prefix, test_database):
        asset = Asset(test_prefix, AssetType.DATABASE, test_database)
        json_data = asset.declaration
        editor = DatabaseEditor()
        editor.set_context(beat_context)
        editor.load_json(json_data)

        assert editor.dump_json() == json_data
