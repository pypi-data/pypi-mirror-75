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

from PyQt5.QtCore import Qt

from ..backend.asset import Asset
from ..backend.asset import AssetType
from ..widgets.assetbrowser import AssetBrowser


class TestAssetBrowser:
    def test_set_current_asset(self, qtbot, test_prefix, beat_context):
        browser = AssetBrowser()
        qtbot.addWidget(browser)
        browser.set_context(beat_context)

        asset = Asset(test_prefix, AssetType.ALGORITHM, "user/integers_add_v2/1")

        with qtbot.waitSignal(browser.view.selectionModel().currentChanged):
            browser.setCurrentAsset(asset)
        assert browser.currentAsset() == asset

    def test_double_click(self, qtbot, test_prefix, beat_context):
        browser = AssetBrowser()
        qtbot.addWidget(browser)
        browser.set_context(beat_context)

        asset = Asset(test_prefix, AssetType.ALGORITHM, "autonomous/add/1")
        browser.setCurrentAsset(asset)
        index = browser.view.currentIndex()
        browser.view.scrollTo(index)
        rect = browser.view.visualRect(index)
        click_point = rect.center()

        with qtbot.waitSignal(browser.view.clicked):
            qtbot.mouseClick(browser.view.viewport(), Qt.LeftButton, pos=click_point)
        with qtbot.waitSignal(browser.assetSelected):
            qtbot.mouseDClick(browser.view.viewport(), Qt.LeftButton, pos=click_point)

    def test_deletion_request(self, qtbot, test_prefix, beat_context):
        browser = AssetBrowser()
        qtbot.addWidget(browser)
        browser.set_context(beat_context)

        asset = Asset(test_prefix, AssetType.ALGORITHM, "autonomous/add/1")
        browser.setCurrentAsset(asset)
        index = browser.view.currentIndex()
        browser.view.scrollTo(index)
        rect = browser.view.visualRect(index)
        click_point = rect.center()
        right_click_point = browser.view.mapFromGlobal(
            browser.view.viewport().mapToGlobal(click_point)
        )

        # customContextMenuRequested doesn't currently seem to work in testing.
        # with qtbot.waitSignal(browser.view.customContextMenuRequested):
        #     qtbot.mouseClick(browser.view, Qt.RightButton, pos=right_click_point)

        # therefore let's manually trigger the slot

        browser._openMenu(right_click_point)

        with qtbot.waitSignal(browser.deletionRequested):
            qtbot.mouseClick(browser.contextual_menu, Qt.LeftButton)
