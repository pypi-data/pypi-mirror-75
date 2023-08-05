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

from PyQt5 import QtCore
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileSystemModel
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtWidgets import QTreeView
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from ..backend.asset import Asset
from ..backend.asset import AssetType


class AssetFilterProxyModel(QSortFilterProxyModel):
    """Filter proxy model showing only asset subfolder"""

    def filterAcceptsRow(self, source_row, source_parent):
        """Filters out all sub-folders that are not from a know asset type"""

        filesystem_model = self.sourceModel()
        root_path = filesystem_model.rootPath()

        index = filesystem_model.index(
            source_row, self.filterKeyColumn(), source_parent
        )
        path = filesystem_model.filePath(index)
        asset_folder = path[len(root_path) + 1 :].split("/")[0]  # noqa E203

        if path.startswith(root_path) and len(asset_folder) > 0:
            try:
                AssetType.from_path(asset_folder)
            except RuntimeError:
                return False

        return super().filterAcceptsRow(source_row, source_parent)


class AssetItemDelegate(QStyledItemDelegate):
    """Delegate to remove file extension"""

    def __init__(self, file_extension, parent=None):
        """Constructor

        :param file_extension str: file extension to filter the text from
        """

        super().__init__(parent)
        self.file_extension = file_extension

    def displayText(self, value, locale):
        """Returns the text to display without the configured extension"""

        if value.endswith(self.file_extension):
            return value.split(".")[0]
        return super().displayText(value, locale)


class AssetBrowser(QWidget):
    """
    Widget that will allow to browse the various assets
    """

    assetSelected = pyqtSignal([Asset])
    deletionRequested = pyqtSignal(["QString"])

    def __init__(self, parent=None):
        """Constructor"""

        super().__init__(parent)
        self.contextual_menu = None
        self.filesystem_model = QFileSystemModel()
        self.filesystem_model.setNameFilters(["*.json"])
        self.filesystem_model.setNameFilterDisables(False)
        self.proxy_model = AssetFilterProxyModel()
        self.proxy_model.setSourceModel(self.filesystem_model)
        self.view = QTreeView()
        self.view.setModel(self.proxy_model)
        self.view.setColumnHidden(1, True)
        self.view.setColumnHidden(2, True)
        self.view.header().setSectionResizeMode(QHeaderView.Interactive)
        self.view.setItemDelegateForColumn(0, AssetItemDelegate(".json"))
        self.view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        layout = QVBoxLayout(self)
        layout.addWidget(self.view)

        self.filesystem_model.directoryLoaded.connect(self.__onDirectoryLoaded)
        self.view.doubleClicked.connect(self._onItemDoubleClicked)
        self.view.customContextMenuRequested.connect(self._openMenu)

    @pyqtSlot()
    def __onDirectoryLoaded(self):
        """When a directory is loaded, resize the first column.

        This makes the navigation easier.
        """

        self.view.resizeColumnToContents(0)

    @pyqtSlot("QModelIndex")
    def _onItemDoubleClicked(self, index):
        """When an item is selected, emit the jsonSelected signal with
        the corresponding JSON file path.
        """

        source_index = self.proxy_model.mapToSource(index)
        if self.filesystem_model.type(source_index).lower() == "json file":
            self.assetSelected.emit(
                Asset.from_path(
                    self.filesystem_model.rootPath(),
                    self.filesystem_model.filePath(source_index),
                )
            )

    @pyqtSlot("QPoint")
    def _openMenu(self, position):
        """Handle the contextual menu"""

        indexes = self.view.selectedIndexes()
        if indexes and indexes[0].data().endswith(".json"):
            if self.contextual_menu is None:
                self.contextual_menu = QMenu()
                action = self.contextual_menu.addAction(self.tr("Delete"))
                action.triggered.connect(self._onDelete)

            self.contextual_menu.popup(self.view.viewport().mapToGlobal(position))

    @pyqtSlot()
    def _onDelete(self):
        """Delete the selected asset"""

        file_index, _ = self.view.selectedIndexes()
        source_index = self.proxy_model.mapToSource(file_index)
        path = self.filesystem_model.filePath(source_index)
        self.deletionRequested.emit(path)

    @pyqtSlot(Asset)
    def setCurrentAsset(self, asset):
        """Set the current index of the view to match the asset"""

        source_index = self.filesystem_model.index(asset.declaration_path)
        self.view.setCurrentIndex(self.proxy_model.mapFromSource(source_index))

    def currentAsset(self):
        """Returns the asset matching the currently selected index"""

        current_index = self.view.currentIndex()
        source_index = self.proxy_model.mapToSource(current_index)
        return Asset.from_path(
            self.filesystem_model.rootPath(),
            self.filesystem_model.filePath(source_index),
        )

    def set_context(self, context):
        """Sets the root path of the prefix to edit"""

        prefix_root_path = context.meta["config"].path

        root_index = self.filesystem_model.setRootPath(prefix_root_path)
        self.view.setRootIndex(self.proxy_model.mapFromSource(root_index))
