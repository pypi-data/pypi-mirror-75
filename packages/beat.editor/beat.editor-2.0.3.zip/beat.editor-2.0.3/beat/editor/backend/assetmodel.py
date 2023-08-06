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

from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

from ..decorators import frozen
from ..utils import dataformat_basetypes
from .asset import Asset
from .asset import AssetType


def enumerate_assets(prefix_path, asset_type, latest_only=False):
    """Enumerate the assets available in the given prefix for the given type
    """

    def _find_json_files(path):
        """Return all json files from folder sorted"""

        asset_items = os.scandir(path)
        json_files = sorted(
            [
                item.name
                for item in asset_items
                if item.is_file() and item.name.endswith("json")
            ]
        )
        return json_files

    assets_list = []
    asset_folder = os.path.join(prefix_path, asset_type.path)

    if asset_type in [AssetType.DATABASE, AssetType.PROTOCOLTEMPLATE]:
        # These assets have no user associated with them
        asset_folders = [entry for entry in os.scandir(asset_folder) if entry.is_dir()]
        for asset_folder in asset_folders:
            json_files = _find_json_files(asset_folder)
            if json_files:
                if latest_only:
                    json_files = json_files[-1:]

                for json_file in json_files:
                    assets_list.append(
                        "{name}/{version}".format(
                            name=asset_folder.name, version=json_file.split(".")[0]
                        )
                    )
    else:
        # Assets belonging to a user
        asset_users = [entry for entry in os.scandir(asset_folder) if entry.is_dir()]

        for asset_user in asset_users:
            asset_folders = [
                entry for entry in os.scandir(asset_user) if entry.is_dir()
            ]
            for asset_folder in asset_folders:
                if asset_type == AssetType.EXPERIMENT:
                    for root, dirs, files in os.walk(asset_folder, topdown=False):
                        if dirs:
                            continue
                        anchor = "experiments/"
                        position = root.index(anchor) + len(anchor)
                        experiment_path = root[position:]
                        for json_file in [
                            file for file in files if file.endswith("json")
                        ]:
                            assets_list.append(
                                "{experiment_path}/{name}".format(
                                    experiment_path=experiment_path,
                                    name=json_file.split(".")[0],
                                )
                            )
                else:
                    json_files = _find_json_files(asset_folder)
                    if json_files:
                        if latest_only:
                            json_files = json_files[-1:]

                        for json_file in json_files:
                            assets_list.append(
                                "{user}/{name}/{version}".format(
                                    user=asset_user.name,
                                    name=asset_folder.name,
                                    version=json_file.split(".")[0],
                                )
                            )

    return sorted(assets_list)


def json_path(prefix_path, asset_type, asset_name):
    """Returns the full path to the json file matching the asset given

    :param prefix_path str: path of the prefix
    :param asset_type AssetType: asset type to search in
    :param asset_name str: fully qualified asset name
    """

    asset = Asset(prefix_path, asset_type, asset_name)
    if not os.path.exists(asset.declaration_path):
        raise ValueError("Invalid asset {}".format(asset_name))
    return asset.declaration_path


class AbstractAssetModel(QStringListModel):
    """Base class for asset related models"""

    prefixPathChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        """Constructor"""

        super().__init__(parent)

        self._latest_only = True
        self._prefix_path = None

    @property
    def asset_folder(self):
        """Returns the folder matching this model asset type"""

        raise NotImplementedError

    def lastestOnlyEnabled(self):
        return self._latest_only

    def setLatestOnlyEnabled(self, enabled):
        if self._latest_only == enabled:
            return

        self._latest_only = enabled
        self.reload()

    latest_only_enabled = pyqtProperty(
        str, fget=lastestOnlyEnabled, fset=setLatestOnlyEnabled
    )

    def prefixPath(self):
        """Returns the prefix path use by this model

        :return: the prefix path used
        """

        return self._prefix_path

    def setPrefixPath(self, path):
        """Set the prefix path use by this model

        :param str path: Path to prefix
        """

        if self._prefix_path == path:
            return

        self._prefix_path = path
        self.reload()
        self.prefixPathChanged.emit(path)

    prefix_path = pyqtProperty(
        str, fget=prefixPath, fset=setPrefixPath, notify=prefixPathChanged
    )

    def json_path(self, asset_name):
        """Returns the full path to the json file matching the asset given

        :param asset_name str: fully qualified asset name
        """

        raise NotImplementedError

    @pyqtSlot()
    def reload(self):
        """Loads the content regarding the asset property from the prefix"""

        raise NotImplementedError


@frozen
class AssetModel(AbstractAssetModel):
    """The asset model present a list of available asset from a given type"""

    assetTypeChanged = pyqtSignal(AssetType)

    def __init__(self, parent=None):
        """Constructor"""

        super().__init__(parent)

        self._asset_type = AssetType.UNKNOWN

    @property
    def asset_folder(self):
        """Reimpl"""

        return os.path.join(self.prefix_path, self.asset_type.path)

    def assetType(self):
        """Returns the asset type of this model

        :return: Asset type of this model
        """

        return self._asset_type

    def setAssetType(self, type_):
        """Set the asset type of this model

        :param AssetType type_: Asset type this model should show
        """

        if self._asset_type == type_:
            return

        self._asset_type = type_
        self.reload()
        self.assetTypeChanged.emit(type_)

    asset_type = pyqtProperty(
        AssetType, fget=assetType, fset=setAssetType, notify=assetTypeChanged
    )

    def json_path(self, asset_name):
        """Reimpl"""

        return json_path(self.prefix_path, self.asset_type, asset_name)

    @pyqtSlot()
    def reload(self):
        """Reimpl"""

        if not self.prefix_path or self._asset_type == AssetType.UNKNOWN:
            return

        self.setStringList(
            enumerate_assets(
                self.prefix_path, self.asset_type, self.latest_only_enabled
            )
        )


@frozen
class DataFormatModel(AbstractAssetModel):
    """DataFormat specific asset model"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self._full_list_enabled = False
        self.__asset_type = AssetType.DATAFORMAT

    @property
    def asset_folder(self):
        """Reimpl"""

        return os.path.join(self.prefix_path, self.__asset_type.path)

    def fullListEnabled(self):
        """Returns whether the full list mode is enabled.

        :return: if full list is enabled
        """

        return self._full_list_enabled

    def setFullListEnabled(self, enabled):
        """Enable/disable the full list mode

        :param bool enabled: enable the full list mode
        """

        if self._full_list_enabled == enabled:
            return

        self._full_list_enabled = enabled
        self.reload()

    full_list_enabled = pyqtProperty(str, fget=fullListEnabled, fset=setFullListEnabled)

    def json_path(self, asset_name):
        """Reimpl"""

        return json_path(self.prefix_path, self.__asset_type, asset_name)

    @pyqtSlot()
    def reload(self):
        """Reimpl"""

        if not self.prefix_path:
            return

        assets = enumerate_assets(
            self.prefix_path, self.__asset_type, self.latest_only_enabled
        )
        if self._full_list_enabled:
            assets = dataformat_basetypes() + assets

        self.setStringList(assets)
