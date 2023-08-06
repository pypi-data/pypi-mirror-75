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
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QPushButton

from ..backend.asset import AssetType
from ..widgets.editor import AbstractAssetEditor
from ..widgets.field import FieldWidget


class MockAssetEditor(AbstractAssetEditor):
    """
    Mock editor to show how to test an editor
    """

    def __init__(self, parent=None):
        super().__init__(AssetType.UNKNOWN, parent)
        self.dataformat_model = None
        self.add_field_button = QPushButton(self.tr("Add"))
        self.layout().addWidget(self.add_field_button)

        self.add_field_button.clicked.connect(self.__addField)

    @pyqtSlot()
    def __addField(self):
        self.layout().addWidget(FieldWidget(self.dataformat_model))

    def set_dataformat_model(self, model):
        self.dataformat_model = model

    def _load_json(self, json_object):
        """Load the json object passed as parameter"""

        for name, type_ in json_object["field"].items():
            field = FieldWidget(self.dataformat_model)
            field.format_name = name
            field.format_type = type_
            self.layout().addWidget(field)

    def _dump_json(self):
        """Returns the json representation of the asset"""

        json_data = {}

        field_list = self.findChildren(FieldWidget)
        json_data["field"] = {}
        for field in field_list:
            json_data["field"][field.format_name] = field.format_type

        return json_data


@pytest.fixture()
def dataformat_model():
    return QStringListModel(["float32", "float64", "int32", "int64"])


class TestMockEditor:
    """Test that the mock editor works correctly"""

    def test_json_load_and_dump_field_widget(self, qtbot, dataformat_model):
        json_reference = {
            "field": {"value32": "float32", "value64": "float64"},
            "description": "Short description test",
        }

        widget = MockAssetEditor()
        widget.set_dataformat_model(dataformat_model)
        widget.load_json(json_reference)

        assert widget.dump_json() == json_reference

    def test_json_load_and_dump_long_description_field_widget(
        self, qtbot, dataformat_model
    ):
        json_reference = {
            "field": {"value32": "float32", "value64": "float64"},
            "description": "This is a very long description to test if the limitation works properly as expected by the editor or not.",
        }

        json_expected_output = {
            "field": {"value32": "float32", "value64": "float64"},
            "description": "This is a very long description to test if the limitation works properly as expected by the editor o",
        }

        widget = MockAssetEditor()
        widget.set_dataformat_model(dataformat_model)
        widget.load_json(json_reference)

        assert widget.dump_json() == json_expected_output

    def test_dataformat_creation_field_widget(self, qtbot, dataformat_model):
        widget = MockAssetEditor()
        widget.set_dataformat_model(dataformat_model)

        qtbot.mouseClick(widget.add_field_button, QtCore.Qt.LeftButton)
        fields = widget.findChildren(FieldWidget)

        assert len(fields) == 1

        field = fields[0]

        field.format_name = "value32"
        field.format_type = "float32"

        assert widget.dump_json() == {"field": {"value32": "float32"}}

        qtbot.mouseClick(widget.add_field_button, QtCore.Qt.LeftButton)
        fields = widget.findChildren(FieldWidget)

        assert len(fields) == 2

        field = fields[1]

        field.format_name = "value64"
        field.format_type = "float64"

        assert widget.dump_json() == {
            "field": {"value32": "float32", "value64": "float64"}
        }
