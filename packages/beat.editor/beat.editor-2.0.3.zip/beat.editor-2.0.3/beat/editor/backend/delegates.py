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

from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QStyledItemDelegate

from .assetmodel import AbstractAssetModel


class AssetItemDelegate(QStyledItemDelegate):
    """Delegate to edit asset entries"""

    def __init__(self, asset_model, parent=None):
        super().__init__(parent)

        if not isinstance(asset_model, AbstractAssetModel):
            raise TypeError("Wrong model type")

        self.asset_model = asset_model

    def createEditor(self, parent, options, index):
        """Create a combox box with all available assets"""

        combobox = QComboBox(parent)
        combobox.setModel(self.asset_model)
        return combobox
