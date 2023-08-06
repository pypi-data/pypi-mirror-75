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

from ..backend.asset import AssetType
from ..backend.assetmodel import AssetModel
from ..decorators import frozen
from .editor import AbstractAssetEditor
from .libraries import LibrariesWidget


@frozen
class LibraryEditor(AbstractAssetEditor):
    """Editor for the Library asset"""

    def __init__(self, parent=None):
        """Constructor

        :param parent QWidget: parent of this widget
        """

        super().__init__(AssetType.LIBRARY, parent)
        self.setObjectName(self.__class__.__name__)
        self.set_title(self.tr("Library"))

        self.language = None
        self.library_model = AssetModel()
        self.library_model.asset_type = AssetType.LIBRARY
        self.library_model.setLatestOnlyEnabled(False)

        self.libraries_widget = LibrariesWidget()
        self.layout().addWidget(self.libraries_widget)

        self.libraries_widget.dataChanged.connect(self.dataChanged)
        self.contextChanged.connect(
            lambda: self.library_model.setPrefixPath(self.prefix_path)
        )

    def _asset_models(self):
        """Reimpl"""

        return [self.library_model]

    def _load_json(self, json_object):
        """Load the json object passed as parameter"""

        self.language = json_object.get("language")
        self.libraries_widget.set_available_libraries(self.library_model.stringList())
        self.libraries_widget.set_used_libraries(json_object.get("uses", {}))

    def _dump_json(self):
        """Returns the json representation of the asset"""

        data = {"language": self.language}
        used_libraries = self.libraries_widget.get_used_libraries()
        if used_libraries:
            data["uses"] = used_libraries
        return data
