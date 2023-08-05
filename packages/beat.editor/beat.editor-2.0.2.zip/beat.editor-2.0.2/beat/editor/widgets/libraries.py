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
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


class LibrariesWidget(QWidget):
    """Class holder for the various libraries"""

    dataChanged = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor"""

        super().__init__(parent)

        self.setMinimumHeight(200)
        self._available_libraries = []

        # Widgets
        available_libraries_label = QLabel(self.tr("Available Libraries"))
        self.available_libraries_listwidget = QListWidget()

        used_libraries_label = QLabel(self.tr("Used Libraries"))
        self.used_libraries_tablewidget = QTableWidget()
        self.used_libraries_tablewidget.setColumnCount(2)
        header = self.used_libraries_tablewidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.used_libraries_tablewidget.setHorizontalHeaderLabels(
            [self.tr("Library name"), self.tr("Library alias")]
        )
        self.used_libraries_tablewidget.setSelectionBehavior(QTableView.SelectRows)
        self.add_library_button = QPushButton(self.tr(">"))
        self.add_library_button.setToolTip(self.tr("Use selected libraries"))
        self.remove_library_button = QPushButton(self.tr("<"))
        self.remove_library_button.setToolTip(self.tr("Remove selected libraries"))

        # Layouts
        layout = QHBoxLayout(self)

        # QVBoxLayout for available libraries
        available_libraries_listwidget_layout = QVBoxLayout()
        available_libraries_listwidget_layout.addWidget(available_libraries_label)
        available_libraries_listwidget_layout.addWidget(
            self.available_libraries_listwidget
        )

        # QVBoxLayout for used libraries
        libraries_used_layout = QVBoxLayout()
        libraries_used_layout.addWidget(used_libraries_label)
        libraries_used_layout.addWidget(self.used_libraries_tablewidget)

        # QVBoxLayout for buttons >/<
        buttons_layout = QVBoxLayout()
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.add_library_button)
        buttons_layout.addWidget(self.remove_library_button)
        buttons_layout.addStretch(1)

        # Layouts Design
        layout.addLayout(available_libraries_listwidget_layout)
        layout.addLayout(buttons_layout)
        layout.addLayout(libraries_used_layout)

        # Signal/Slots connections
        self.add_library_button.clicked.connect(self.__onAddLibraryClicked)
        self.remove_library_button.clicked.connect(self.__onRemoveLibraryClicked)

        self.add_library_button.clicked.connect(self.dataChanged)
        self.remove_library_button.clicked.connect(self.dataChanged)

    def __use_library(self, library_name, library_alias):
        """Put the library in the used library table and removes it from
        from the available list.
        """

        # Remove it from available
        item_list = self.available_libraries_listwidget.findItems(
            library_name, Qt.MatchExactly
        )
        if len(item_list) > 0:
            item = item_list[0]
            row = self.available_libraries_listwidget.row(item)
            self.available_libraries_listwidget.takeItem(row)
            del item

            # Add it to used
            row = self.used_libraries_tablewidget.rowCount()
            self.used_libraries_tablewidget.insertRow(row)
            library_name_item = QTableWidgetItem(library_name)
            library_name_item.setFlags(library_name_item.flags() & ~Qt.ItemIsEditable)
            self.used_libraries_tablewidget.setItem(row, 0, library_name_item)
            self.used_libraries_tablewidget.setItem(
                row, 1, QTableWidgetItem(library_alias)
            )

    @pyqtSlot()
    def __onAddLibraryClicked(self):
        selected_libraries = self.available_libraries_listwidget.selectedItems()
        if selected_libraries:
            for library in selected_libraries:
                library_name = library.text()
                library_alias = library_name.split("/")[1]
                self.__use_library(library_name, library_alias)

    @pyqtSlot()
    def __onRemoveLibraryClicked(self):
        # Get reverse order for deletion and set for possible rowcolumn selection
        rows = sorted(
            set(
                list(
                    index.row()
                    for index in self.used_libraries_tablewidget.selectedIndexes()
                )
            ),
            reverse=True,
        )
        for row in rows:
            library_name = self.used_libraries_tablewidget.item(row, 0).text()
            self.available_libraries_listwidget.addItem(library_name)
            self.used_libraries_tablewidget.removeRow(row)

    def get_used_libraries(self):
        """Returns the libraries used"""
        # {key:value} for {library_alias:library_name}
        libraries = {}

        for row in range(0, self.used_libraries_tablewidget.rowCount()):
            libraries[
                self.used_libraries_tablewidget.item(row, 1).text()
            ] = self.used_libraries_tablewidget.item(row, 0).text()

        return libraries

    def set_used_libraries(self, libraries):
        self.set_available_libraries(self._available_libraries)
        for alias, library in libraries.items():
            self.__use_library(library, alias)

    def get_available_libraries(self):
        """Returns the available libraries"""
        # {key:value} for {library_alias:library_name}
        return self._available_libraries

    def set_available_libraries(self, available_libraries):
        """Set the available libraries"""
        # clear available and used libraries

        self.available_libraries_listwidget.clear()
        self.used_libraries_tablewidget.clear()
        self.used_libraries_tablewidget.setRowCount(0)
        self._available_libraries = available_libraries
        self.available_libraries_listwidget.addItems(self._available_libraries)
