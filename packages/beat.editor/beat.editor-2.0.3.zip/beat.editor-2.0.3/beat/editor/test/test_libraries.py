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

from ..widgets.libraries import LibrariesWidget


class TestLibrariesWidget:
    """Test that the library widget works correctly"""

    def test_dump_used_libraries(self, qtbot):
        no_libraries_set = {}

        libraries = LibrariesWidget()
        qtbot.addWidget(libraries)
        assert libraries.get_used_libraries() == no_libraries_set

    def test_load_dump_libraries(self, qtbot):
        available_libraries = ["user/lib1/1", "user/lib2/1", "user/lib3/1"]
        no_libraries_set = {}
        one_library_set = {"lib1": "user/lib1/1"}

        libraries = LibrariesWidget()
        qtbot.addWidget(libraries)
        libraries.set_available_libraries(available_libraries)

        assert libraries.get_used_libraries() == no_libraries_set
        libraries.set_used_libraries(one_library_set)
        assert libraries.get_used_libraries() == one_library_set

    def test_load_available_libraries(self, qtbot):
        available_libraries = ["user/lib1/1", "user/lib2/1", "user/lib3/1"]

        libraries = LibrariesWidget()
        qtbot.addWidget(libraries)
        libraries.set_available_libraries(available_libraries)
        assert libraries.get_available_libraries() == available_libraries

    def test_use_dump_libraries(self, qtbot):
        available_libraries = ["user/lib1/1", "user/lib2/1", "user/lib3/1"]
        one_library_set = {"lib1": "user/lib1/1"}
        two_libraries_set = {"lib1": "user/lib1/1", "lib3": "user/lib3/1"}

        libraries = LibrariesWidget()
        qtbot.addWidget(libraries)
        libraries.set_available_libraries(available_libraries)

        # Add lib1 from the available libraries
        libraries.available_libraries_listwidget.setCurrentRow(0)
        qtbot.mouseClick(libraries.add_library_button, QtCore.Qt.LeftButton)
        assert libraries.get_used_libraries() == one_library_set

        # Add lib3 item from the available libraries
        libraries.available_libraries_listwidget.setCurrentRow(1)
        qtbot.mouseClick(libraries.add_library_button, QtCore.Qt.LeftButton)
        assert libraries.get_used_libraries() == two_libraries_set

        # Remove lib3 from the used libraries
        libraries.used_libraries_tablewidget.selectRow(1)
        qtbot.mouseClick(libraries.remove_library_button, QtCore.Qt.LeftButton)
        assert libraries.get_used_libraries() == one_library_set

    def test_change_alias(self, qtbot):
        available_libraries = ["user/lib1/1", "user/lib2/1", "user/lib3/1"]
        one_library_set = {"lib1": "user/lib1/1"}
        modified_library_set = {"test1": "user/lib1/1"}

        libraries = LibrariesWidget()
        qtbot.addWidget(libraries)
        libraries.set_available_libraries(available_libraries)

        # Add lib1 from the available libraries
        libraries.available_libraries_listwidget.setCurrentRow(0)
        qtbot.mouseClick(libraries.add_library_button, QtCore.Qt.LeftButton)
        assert libraries.get_used_libraries() == one_library_set

        item = libraries.used_libraries_tablewidget.item(0, 1)
        item.setText("test1")
        assert libraries.get_used_libraries() == modified_library_set
