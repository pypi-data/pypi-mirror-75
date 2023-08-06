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
from PyQt5.QtWidgets import QDialogButtonBox

from ..backend.asset import AssetType
from ..widgets.dialogs import AssetCreationDialog


class TestAssetCreationDialog:
    """Test that the asset creation dialog works as expected"""

    def test_widget_visibility(self, qtbot, beat_context, asset_type):
        dialog = AssetCreationDialog(beat_context, asset_type)
        dialog.show()
        qtbot.addWidget(dialog)

        assert dialog.new_version_radio_button.isVisible() == asset_type.has_versions()
        assert dialog.fork_radio_button.isVisible() == asset_type.can_fork()

    def test_input_disabling(self, qtbot, beat_context):
        dialog = AssetCreationDialog(beat_context, AssetType.DATAFORMAT)
        dialog.show()
        qtbot.addWidget(dialog)

        assert dialog.name_lineedit.isEnabled()
        assert not dialog.new_version_combobox.isEnabled()
        assert not dialog.fork_combobox.isEnabled()
        assert dialog.creationType() == AssetCreationDialog.NEW

        qtbot.mouseClick(dialog.new_version_radio_button, QtCore.Qt.LeftButton)

        assert not dialog.name_lineedit.isEnabled()
        assert dialog.new_version_combobox.isEnabled()
        assert not dialog.fork_combobox.isEnabled()
        assert dialog.creationType() == AssetCreationDialog.NEW_VERSION

        qtbot.mouseClick(dialog.fork_radio_button, QtCore.Qt.LeftButton)

        assert not dialog.name_lineedit.isEnabled()
        assert not dialog.new_version_combobox.isEnabled()
        assert dialog.fork_combobox.isEnabled()
        assert dialog.creationType() == AssetCreationDialog.FORK

    def test_create_new(self, qtbot, beat_context, asset_type):
        dialog = AssetCreationDialog(beat_context, asset_type)
        qtbot.addWidget(dialog)
        asset_name = "test_asset"

        qtbot.mouseClick(dialog.new_radio_button, QtCore.Qt.LeftButton)

        with qtbot.waitCallback() as cb:
            dialog.open(cb)
            qtbot.keyClicks(dialog.name_lineedit, asset_name)
            qtbot.mouseClick(
                dialog.buttonbox.button(QDialogButtonBox.Ok), QtCore.Qt.LeftButton
            )

        assert dialog.creationType() == AssetCreationDialog.NEW
        if asset_type == AssetType.EXPERIMENT:
            asset_info = dialog.assetInfo()
            assert isinstance(asset_info, tuple)
            assert asset_info[1] == asset_name
        else:
            assert dialog.assetInfo() == asset_name

    @pytest.mark.parametrize(
        "asset_type", [item for item in AssetType if item.has_versions()]
    )
    def test_create_new_version(self, qtbot, beat_context, asset_type):
        dialog = AssetCreationDialog(beat_context, asset_type)
        qtbot.addWidget(dialog)

        with qtbot.waitCallback() as cb:
            dialog.open(cb)
            qtbot.mouseClick(dialog.new_version_radio_button, QtCore.Qt.LeftButton)
            qtbot.mouseClick(
                dialog.buttonbox.button(QDialogButtonBox.Ok), QtCore.Qt.LeftButton
            )

        assert dialog.creationType() == AssetCreationDialog.NEW_VERSION
        assert dialog.assetInfo() == dialog.new_version_combobox.currentText()

    @pytest.mark.parametrize(
        "asset_type", [item for item in AssetType if item.can_fork()]
    )
    def test_create_fork(self, qtbot, beat_context, asset_type):
        dialog = AssetCreationDialog(beat_context, asset_type)
        qtbot.addWidget(dialog)
        asset_name = "test_asset"

        with qtbot.waitCallback() as cb:
            dialog.open(cb)
            qtbot.mouseClick(dialog.fork_radio_button, QtCore.Qt.LeftButton)
            qtbot.keyClicks(dialog.fork_lineedit, asset_name)
            qtbot.mouseClick(
                dialog.buttonbox.button(QDialogButtonBox.Ok), QtCore.Qt.LeftButton
            )

        assert dialog.creationType() == AssetCreationDialog.FORK
        assert dialog.assetInfo() == (dialog.fork_combobox.currentText(), asset_name)
