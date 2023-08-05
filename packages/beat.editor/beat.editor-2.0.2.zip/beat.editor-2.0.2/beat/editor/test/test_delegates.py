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

from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QListView

from ..backend.assetmodel import AssetModel
from ..backend.delegates import AssetItemDelegate


class TestAssetItemDelegate:
    """Test that the delegate provides the correct editor"""

    def test_valid_model(self, qtbot, test_prefix, asset_type):
        asset_model = AssetModel()
        asset_model.asset_type = asset_type
        asset_model.prefix_path = test_prefix

        delegate = AssetItemDelegate(asset_model)
        model = QStandardItemModel(1, 1)
        model.setItem(0, 0, QStandardItem(""))

        view = QListView()
        qtbot.addWidget(view)

        view.setModel(model)
        view.setItemDelegate(delegate)
        view.edit(model.index(0, 0))
        widget_list = view.viewport().findChildren(QComboBox)
        assert len(widget_list) == 1

        editor = widget_list[0]
        editor_model = editor.model()
        assert isinstance(editor_model, AssetModel)
        assert editor_model == asset_model

    def test_invalid_model(self, qtbot):

        with pytest.raises(TypeError):
            AssetItemDelegate(QStringListModel())
