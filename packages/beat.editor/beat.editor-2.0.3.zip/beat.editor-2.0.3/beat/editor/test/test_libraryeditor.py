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
from ..widgets.libraryeditor import LibraryEditor
from .conftest import prefix
from .conftest import sync_prefix


def get_library_declaration(prefix_path, library_name):
    asset = Asset(prefix_path, AssetType.LIBRARY, library_name)
    return asset.declaration


def get_valid_library(test_prefix):
    sync_prefix()
    model = AssetModel()
    model.asset_type = AssetType.LIBRARY
    model.prefix_path = test_prefix
    model.setLatestOnlyEnabled(False)
    return [
        algorithm
        for algorithm in model.stringList()
        if all(invalid not in algorithm for invalid in ["errors", "invalid"])
    ]


class TestLibraryEditor:
    """Test that the mock editor works correctly"""

    def test_default_dump(self, qtbot):
        editor = LibraryEditor()
        qtbot.addWidget(editor)

        assert editor.dump_json() == {"language": None}
        assert editor.is_valid()

    @pytest.mark.parametrize("library", get_valid_library(prefix))
    def test_load_and_dump(self, qtbot, beat_context, test_prefix, library):
        reference_json = get_library_declaration(test_prefix, library)
        editor = LibraryEditor()
        qtbot.addWidget(editor)
        editor.set_context(beat_context)
        editor.load_json(reference_json)

        uses = reference_json.get("uses")
        if not uses:
            reference_json.pop("uses", None)

        assert editor.dump_json() == reference_json
        assert editor.is_valid()

    def test_load_and_dump_wrong(self, qtbot, beat_context):
        faulty_json = {"description": "test", "uses": {"alias": "test/dummy/1"}}
        reference_json = {"description": "test", "language": None}
        editor = LibraryEditor()
        qtbot.addWidget(editor)
        editor.set_context(beat_context)
        editor.load_json(faulty_json)

        assert editor.dump_json() == reference_json
        assert editor.is_valid()
