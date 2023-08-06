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
import shutil
import tempfile

import pytest
import simplejson as json

from ..backend.asset import Asset
from ..backend.asset import AssetType


@pytest.fixture(params=[item for item in AssetType if item.can_create()])
def creatable_asset_type(request):
    return request.param


@pytest.fixture(params=[item for item in AssetType if not item.can_create()])
def uncreatable_asset_type(request):
    return request.param


@pytest.fixture(params=[item for item in AssetType if item.can_fork()])
def forkable_asset_type(request):
    return request.param


@pytest.fixture(params=[item for item in AssetType if not item.can_fork()])
def unforkable_asset_type(request):
    return request.param


existing_asset_name_map = {
    AssetType.ALGORITHM: "autonomous/add/1",
    AssetType.DATABASE: "simple/1",
    AssetType.DATAFORMAT: "user/complexes/1",
    AssetType.EXPERIMENT: "user/user/double/1/double",
    AssetType.LIBRARY: "user/sum/1",
    AssetType.PLOTTER: "user/scatter/1",
    AssetType.PLOTTERPARAMETER: "plot/config/1",
    AssetType.PROTOCOLTEMPLATE: "double/1",
    AssetType.TOOLCHAIN: "user/double/1",
    AssetType.UNKNOWN: None,
}


class TestAssetType:
    """Test the asset type enum"""

    asset_name_map = {
        AssetType.ALGORITHM: "user/foo/1",
        AssetType.DATABASE: "foo/1",
        AssetType.DATAFORMAT: "user/foo/1",
        AssetType.EXPERIMENT: "user/foo/bar/1/baz",
        AssetType.LIBRARY: "user/foo/1",
        AssetType.PLOTTER: "user/foo/1",
        AssetType.PLOTTERPARAMETER: "user/foo/1",
        AssetType.PROTOCOLTEMPLATE: "foo/1",
        AssetType.TOOLCHAIN: "user/foo/1",
        AssetType.UNKNOWN: None,
    }

    def test_invalid_from_path(self):
        with pytest.raises(RuntimeError):
            AssetType.from_path("dummy")

    def test_unknown_validation(self):
        with pytest.raises(RuntimeError):
            AssetType.UNKNOWN.validate({})

    def test_unknown_creation(self):
        with pytest.raises(RuntimeError):
            AssetType.UNKNOWN.create_new("foo", "bar")

    def test_unknown_new_version(self):
        with pytest.raises(RuntimeError):
            AssetType.UNKNOWN.create_new_version("foo", "bar")

    def test_unknown_fork(self):
        with pytest.raises(RuntimeError):
            AssetType.UNKNOWN.fork("foo", "bar", "baz")

    def test_unknown_delete(self):
        with pytest.raises(RuntimeError):
            AssetType.UNKNOWN.delete("foo", "bar")

    def test_creation(self, test_prefix, creatable_asset_type):
        asset_name = self.asset_name_map[creatable_asset_type]
        result = creatable_asset_type.create_new(test_prefix, asset_name)
        assert result

    def test_creation_failure(self, test_prefix, uncreatable_asset_type):
        asset_name = self.asset_name_map[uncreatable_asset_type]
        with pytest.raises(RuntimeError):
            uncreatable_asset_type.create_new(test_prefix, asset_name)

    def test_create_new_version(self, test_prefix, creatable_asset_type):
        asset_name = existing_asset_name_map[creatable_asset_type]
        result = creatable_asset_type.create_new_version(test_prefix, asset_name)
        assert result

    def test_create_new_version_failure(self, test_prefix, uncreatable_asset_type):
        asset_name = existing_asset_name_map[uncreatable_asset_type]
        with pytest.raises(RuntimeError):
            uncreatable_asset_type.create_new_version(test_prefix, asset_name)

    def test_fork(self, test_prefix, forkable_asset_type):
        source_asset_name = existing_asset_name_map[forkable_asset_type]
        dest_asset_name = self.asset_name_map[forkable_asset_type]
        result = forkable_asset_type.fork(
            test_prefix, source_asset_name, dest_asset_name
        )
        assert result

    def test_fork_failure(self, test_prefix, unforkable_asset_type):
        source_asset_name = existing_asset_name_map[unforkable_asset_type]
        dest_asset_name = self.asset_name_map[unforkable_asset_type]
        with pytest.raises(RuntimeError):
            unforkable_asset_type.fork(test_prefix, source_asset_name, dest_asset_name)

    def test_delete(self, test_prefix, asset_type):
        with tempfile.TemporaryDirectory(suffix=".prefix") as prefix:
            tmp_prefix = os.path.join(prefix, "prefix")
            shutil.copytree(test_prefix, tmp_prefix)
            asset_name = existing_asset_name_map[asset_type]
            result = asset_type.delete(tmp_prefix, asset_name)
            assert result


class TestAsset:
    """Test that the asset works correctly"""

    def test_from_path(self, test_prefix, asset_type):
        asset_name = existing_asset_name_map[asset_type]
        full_path = os.path.join(test_prefix, asset_type.path, asset_name)
        asset = Asset.from_path(test_prefix, full_path)
        assert asset.prefix == test_prefix
        assert asset.type == asset_type
        assert asset.name == asset_name

    def test_unknown_declaration_path(self):
        asset = Asset("dummy", AssetType.UNKNOWN, "dummy/dummy/1")
        with pytest.raises(RuntimeError):
            asset.declaration_path

    def test_declaration_path(self, test_prefix, asset_type):
        asset_name = existing_asset_name_map[asset_type]
        asset = Asset(test_prefix, asset_type, asset_name)
        assert os.path.exists(asset.declaration_path)

    def test_unknown_documentation_path(self):
        asset = Asset("dummy", AssetType.UNKNOWN, "dummy/dummy/1")
        with pytest.raises(RuntimeError):
            asset.documentation_path

    def test_documentation_path(self, test_prefix, asset_type):
        asset_name = existing_asset_name_map[asset_type]
        asset = Asset(test_prefix, asset_type, asset_name)
        assert os.path.exists(asset.documentation_path)

    def test_unknown_code_path(self):
        asset = Asset("dummy", AssetType.UNKNOWN, "dummy/dummy/1")
        with pytest.raises(RuntimeError):
            asset.code_path

    def test_code_path(self, test_prefix, asset_type):
        asset_name = existing_asset_name_map[asset_type]
        asset = Asset(test_prefix, asset_type, asset_name)
        if asset_type.has_code():
            assert os.path.exists(asset.code_path)
        else:
            assert asset.code_path is None

    def test_delete(self, test_prefix, asset_type):
        with tempfile.TemporaryDirectory(suffix=".prefix") as prefix:
            tmp_prefix = os.path.join(prefix, "prefix")
            shutil.copytree(test_prefix, tmp_prefix)
            asset_name = existing_asset_name_map[asset_type]
            asset = Asset(tmp_prefix, asset_type, asset_name)
            result = asset.delete()
            assert result

    def test_declaration_property(self, test_prefix, asset_type):
        asset_name = existing_asset_name_map[asset_type]
        asset = Asset(test_prefix, asset_type, asset_name)
        declaration = asset.declaration
        with open(asset.declaration_path, "rt") as json_file:
            file_content = json.load(json_file)
            assert declaration == file_content

        if asset_type is not AssetType.DATAFORMAT:
            declaration["description"] = "New description"
        else:
            declaration["#description"] = "New description"

        asset.declaration = declaration

        with open(asset.declaration_path, "rt") as json_file:
            file_content = json.load(json_file)
            assert declaration == file_content

    def test_storage(self, test_prefix, asset_type):
        asset_name = existing_asset_name_map[asset_type]
        asset = Asset(test_prefix, asset_type, asset_name)
        storage = asset.storage()
        assert isinstance(storage, asset_type.storage)

    def test_is_valid(self, test_prefix, asset_type):
        asset_name = existing_asset_name_map[asset_type]
        asset = Asset(test_prefix, asset_type, asset_name)
        valid, errors = asset.is_valid()
        assert valid
        assert not errors

    def test_is_invalid(self, test_prefix, asset_type):
        asset_name = existing_asset_name_map[asset_type]
        asset = Asset(test_prefix, asset_type, asset_name)

        with open(asset.declaration_path, "wt") as json_file:
            json_file.write("")

        valid, errors = asset.is_valid()

        assert not valid
        assert errors
