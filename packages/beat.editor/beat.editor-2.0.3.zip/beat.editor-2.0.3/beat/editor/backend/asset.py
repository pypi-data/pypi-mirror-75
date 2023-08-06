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

import importlib

from enum import Enum
from enum import unique

import simplejson as json

import beat.core

from beat.backend.python import utils
from beat.cmdline import common
from beat.core.schema import validate


@unique
class AssetType(Enum):
    """All possible assets available on the BEAT platform"""

    UNKNOWN = ("unknown", None)
    ALGORITHM = ("algorithms", beat.core.algorithm.Algorithm)
    DATABASE = ("databases", beat.core.database.Database)
    DATAFORMAT = ("dataformats", beat.core.dataformat.DataFormat)
    EXPERIMENT = ("experiments", beat.core.experiment.Experiment)
    LIBRARY = ("libraries", beat.core.library.Library)
    PLOTTER = ("plotters", beat.core.plotter.Plotter)
    PLOTTERPARAMETER = (
        "plotterparameters",
        beat.core.plotterparameter.Plotterparameter,
    )
    PROTOCOLTEMPLATE = (
        "protocoltemplates",
        beat.core.protocoltemplate.ProtocolTemplate,
    )
    TOOLCHAIN = ("toolchains", beat.core.toolchain.Toolchain)

    def __init__(self, path, klass):
        self.path = path
        self.klass = klass

    @property
    def storage(self):
        mod = importlib.import_module(self.klass.__module__)
        return getattr(mod, "Storage")

    @staticmethod
    def from_path(path):
        for asset_type in AssetType:
            if asset_type.path == path:
                return asset_type
        raise RuntimeError("Unknown asset path {}".format(path))

    def can_create(self):
        """Returns whether a new asset can be created from scratch"""

        return self not in [self.UNKNOWN, self.EXPERIMENT]

    def has_versions(self):
        """Returns whether a new version of this asset can be created"""

        return self not in [self.UNKNOWN, self.EXPERIMENT]

    def can_fork(self):
        """Returns whether a new asset can be forked"""

        return self not in [self.UNKNOWN, self.DATABASE, self.PROTOCOLTEMPLATE]

    def split_count(self):
        """Returns the number of "/" that should be part of its name"""

        if self == self.UNKNOWN:
            return 0
        elif self == self.EXPERIMENT:
            return 5
        elif self not in [self.DATABASE, self.PROTOCOLTEMPLATE]:
            return 2
        else:
            return 1

    def validate(self, data):
        """Runs the schema validation and returns whether an asset is valid

        :param data str: asset content
        """

        if self == self.UNKNOWN:
            raise RuntimeError("Trying to validate unknown type")
        return validate(self.name.lower(), data)

    def create_new(self, prefix, name):
        """Create a new asset from a prototype

        :param prefix str: Path to the prefix
        :param name str: name of the asset
        """

        if self == self.UNKNOWN:
            raise RuntimeError("Trying to create an asset of unknown type")
        success = common.create(prefix, self.name.lower(), [name])
        return success == 0

    def create_new_version(self, prefix, name):
        """Create a new version of the asset

        :param prefix str: Path to the prefix
        :param name str: name of the asset
        """

        if self == self.UNKNOWN:
            raise RuntimeError(
                "Trying to create a new version of an asset of unknown type"
            )
        success = common.new_version(prefix, self.name.lower(), name)
        return success == 0

    def fork(self, prefix, source, destination):
        """Fork an asset

        :param prefix str: Path to the prefix
        :param source str: name of the original asset
        :param destination str: name of the new asset
        """

        if self == self.UNKNOWN:
            raise RuntimeError("Trying to fork an asset of unknown type")
        success = common.fork(prefix, self.name.lower(), source, destination)
        return success == 0

    def delete(self, prefix, name):
        """Delete an asset

        :param prefix str: Path to the prefix
        :param name str: name of the asset to delete
        """

        if self == self.UNKNOWN:
            raise RuntimeError("Trying to delete an asset of unknown type")
        success = common.delete_local(prefix, self.name.lower(), [name])
        return success == 0

    def has_code(self):
        """Returns whether this asset type contains code"""

        if self.klass is None:
            return False

        return issubclass(self.storage, utils.CodeStorage)


class Asset:
    """Class encapsulating an asset"""

    def __init__(self, prefix, asset_type, asset_name):
        self.prefix = prefix
        self.type = asset_type
        self.name = asset_name

    def __eq__(self, other):
        """Comparison operator"""

        if isinstance(other, Asset):
            return (
                self.type == other.type
                and self.name == other.name
                and self.prefix == other.prefix
            )
        return False

    def __repr__(self):
        """Representation"""

        return f"{self.type}: {self.name}"

    @staticmethod
    def from_path(prefix, path):
        """Builds an asset based on a full path with the given prefix"""

        asset_path = path[len(prefix) :]  # noqa
        asset_str = asset_path.split("/")[1]
        asset_type = AssetType.from_path(asset_str)
        asset_name = "/".join(asset_path.split("/")[2:]).split(".")[0]
        return Asset(prefix, asset_type, asset_name)

    @property
    def declaration_path(self):
        """Returns the full path to the declaration file"""

        if self.type == AssetType.UNKNOWN:
            raise RuntimeError("Trying to get declaration of unknown type")

        return self.storage().json.path

    @property
    def declaration(self):
        """Returns the JSON content loaded from the file"""

        with open(self.declaration_path, "rt") as json_file:
            return json.load(json_file)

    @declaration.setter
    def declaration(self, declaration):
        with open(self.declaration_path, "wt") as json_file:
            json_file.write(
                json.dumps(
                    declaration, sort_keys=True, indent=4, cls=utils.NumpyJSONEncoder
                )
            )

    @property
    def documentation_path(self):
        """Returns the full path to the documentation file"""

        if self.type == AssetType.UNKNOWN:
            raise RuntimeError("Trying to get documentation of unknown type")

        return self.storage().doc.path

    @property
    def code_path(self):
        """Returns the full path to the code file"""

        if self.type == AssetType.UNKNOWN:
            raise RuntimeError("Trying to get code of unknown type")

        if not self.type.has_code():
            return None

        return self.storage().code.path

    def delete(self):
        """Deletes the asset pointed to by this object"""

        return self.type.delete(self.prefix, self.name)

    def storage(self):
        """Returns the storage object for this asset"""

        return self.type.storage(self.prefix, self.name)

    def is_valid(self):
        """Returns whether the declaration of this asset is valid and the list
        of error associated.
        """

        _, error_list = self.type.validate(self.declaration_path)
        return len(error_list) == 0, error_list
