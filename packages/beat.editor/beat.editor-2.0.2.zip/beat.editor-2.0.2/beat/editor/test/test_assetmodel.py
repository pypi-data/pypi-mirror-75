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

import pytest

from ..backend.asset import AssetType
from ..backend.assetmodel import AssetModel
from ..backend.assetmodel import DataFormatModel
from ..utils import dataformat_basetypes


@pytest.fixture()
def asset_model(qtbot, test_prefix, asset_type):
    model = AssetModel()

    with qtbot.waitSignals(
        [model.assetTypeChanged, model.prefixPathChanged]
    ) as blocker:
        model.asset_type = asset_type
        model.prefix_path = test_prefix

    assert blocker.all_signals_and_args[0].args[0] == asset_type
    assert blocker.all_signals_and_args[1].args[0] == test_prefix
    return model


class TestAssetModel:
    """Test that the mock editor works correctly"""

    def test_model_load(self, asset_model):
        asset_list = asset_model.stringList()
        assert len(asset_list) > 0
        asset_type = asset_model.asset_type

        if asset_type == AssetType.EXPERIMENT:
            split_size = 5
        elif asset_type in [AssetType.DATABASE, AssetType.PROTOCOLTEMPLATE]:
            split_size = 2
        else:
            split_size = 3
        for item in asset_list:
            assert len(item.split("/")) == split_size

    def test_json_path(self, asset_model):
        asset_list = asset_model.stringList()
        assert len(asset_list) > 0

        if asset_model.asset_type == AssetType.DATAFORMAT:
            basetypes = dataformat_basetypes()
            asset_list = [item for item in asset_list if item not in basetypes]

        for item in asset_list:
            path = asset_model.json_path(item)
            assert path

    def test_json_path_invalid_asset(self, asset_model):
        asset_type = asset_model.asset_type

        with pytest.raises(ValueError):
            if asset_type == AssetType.EXPERIMENT:
                path = "invalid/invalid/invalid/invalid/1"
            elif asset_type in [AssetType.DATABASE, AssetType.PROTOCOLTEMPLATE]:
                path = "invalid_name/1"
            else:
                path = "invalid/invalid_name/1"
            asset_model.json_path(path)

    def test_latest_only(self, asset_model):
        asset_list = asset_model.stringList()
        assert len(asset_list) > 0
        asset_model.setLatestOnlyEnabled(False)
        new_asset_list = asset_model.stringList()

        if asset_model.asset_type == AssetType.EXPERIMENT:
            assert len(new_asset_list) == len(asset_list)
            assert new_asset_list == asset_list
        else:
            assert len(new_asset_list) > len(asset_list)
            assert new_asset_list != asset_list

    def test_latest_only_no_reload(self, asset_model):
        asset_list = asset_model.stringList()
        assert len(asset_list) > 0
        asset_model.setLatestOnlyEnabled(True)
        new_asset_list = asset_model.stringList()
        assert asset_list == new_asset_list

    def test_setting_same_type_no_reload(self, qtbot, asset_model):
        asset_list = asset_model.stringList()
        assert len(asset_list) > 0
        with qtbot.assertNotEmitted(asset_model.assetTypeChanged):
            asset_model.setAssetType(asset_model.asset_type)
        new_asset_list = asset_model.stringList()
        assert asset_list == new_asset_list

    def test_setting_same_path_no_reload(self, qtbot, asset_model):
        asset_list = asset_model.stringList()
        assert len(asset_list) > 0
        with qtbot.assertNotEmitted(asset_model.prefixPathChanged):
            asset_model.setPrefixPath(asset_model.prefix_path)
        new_asset_list = asset_model.stringList()
        assert asset_list == new_asset_list

    def test_unexpected_files(self, asset_model):
        """This test ensures that unexpected files in the prefix don't break
           the AssetModel class loading code.
        """

        def __create_file(path):
            with open(os.path.join(path, "unexpected.txt"), "wt") as unexpected_file:
                unexpected_file.write("nothing")

        asset_list = asset_model.stringList()

        folders = os.scandir(asset_model.asset_folder)

        for folder in folders:
            __create_file(os.path.join(asset_model.asset_folder, folder))

        __create_file(asset_model.asset_folder)

        asset_model.reload()

        assert asset_model.stringList() == asset_list


class TestDataFormatModel:
    """Test that the mock editor works correctly"""

    @pytest.fixture(params=[False, True], ids=["Normal list", "Include base types"])
    def df_model(self, request, test_prefix):
        df_model = DataFormatModel()
        df_model.prefix_path = test_prefix
        df_model.full_list_enabled = request.param
        return df_model

    def test_model_load(self, df_model):
        asset_list = df_model.stringList()
        assert len(asset_list) > 0

        basetypes = dataformat_basetypes()
        for item in asset_list:
            assert len(item.split("/")) == 3 or item in basetypes

    def test_json_path(self, df_model):
        asset_list = df_model.stringList()
        assert len(asset_list) > 0
        base_types = dataformat_basetypes()
        for item in asset_list:

            if item in base_types:
                with pytest.raises(RuntimeError):
                    _ = df_model.json_path(item)
            else:
                path = df_model.json_path(item)
                assert path

    def test_json_path_invalid_asset(self, df_model):
        with pytest.raises(ValueError):
            path = "invalid/invalid_name/1"
            df_model.json_path(path)

    def test_latest_only(self, df_model):
        asset_list = df_model.stringList()
        assert len(asset_list) > 0
        df_model.setLatestOnlyEnabled(False)
        new_asset_list = df_model.stringList()

        assert len(new_asset_list) > len(asset_list)
        assert new_asset_list != asset_list

    def test_latest_only_no_reload(self, df_model):
        asset_list = df_model.stringList()
        assert len(asset_list) > 0
        df_model.setLatestOnlyEnabled(True)
        new_asset_list = df_model.stringList()
        assert asset_list == new_asset_list

    def test_setting_same_path_no_reload(self, qtbot, df_model):
        asset_list = df_model.stringList()
        assert len(asset_list) > 0
        with qtbot.assertNotEmitted(df_model.prefixPathChanged):
            df_model.setPrefixPath(df_model.prefix_path)
        new_asset_list = df_model.stringList()
        assert asset_list == new_asset_list

    def test_unexpected_files(self, df_model):
        """This test ensures that unexpected files in the prefix don't break
           the AssetModel class loading code.
        """

        def __create_file(path):
            with open(os.path.join(path, "unexpected.txt"), "wt") as unexpected_file:
                unexpected_file.write("nothing")

        asset_list = df_model.stringList()

        items = os.scandir(df_model.asset_folder)
        folders = []
        for item in items:
            path = os.path.join(df_model.asset_folder, item)
            if os.path.isdir(path):
                folders.append(path)

        for folder in folders:
            __create_file(os.path.join(df_model.asset_folder, folder))

        __create_file(df_model.asset_folder)

        df_model.reload()

        assert df_model.stringList() == asset_list
