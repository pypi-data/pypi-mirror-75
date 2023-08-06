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

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from ..widgets.scrollwidget import EditorListWidget
from ..widgets.scrollwidget import ScrollWidget


@pytest.fixture(params=[EditorListWidget, ScrollWidget])
def test_class(request):
    return request.param


class ChangeWidget(QWidget):
    dataChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._prefix_path = None

    def changeMe(self):
        self.dataChanged.emit()

    def setPrefixPath(self, prefix_path):
        self._prefix_path = prefix_path

    @property
    def prefix_path(self):
        return self._prefix_path


class TestDataChangedHandling:
    def test_dataChanged_on_add_and_remove(self, qtbot, test_class):
        test_widget = test_class()
        qtbot.addWidget(test_widget)

        widget = QWidget()

        with qtbot.waitSignal(test_widget.dataChanged):
            test_widget.addWidget(widget)

        assert len(test_widget.widget_list) == 1

        with qtbot.waitSignal(test_widget.dataChanged):
            test_widget.removeWidget(widget)

        assert len(test_widget.widget_list) == 0

    def test_widget_with_dataChanged(self, qtbot, test_class):
        test_widget = test_class()
        qtbot.addWidget(test_widget)

        widget = ChangeWidget()
        test_widget.addWidget(widget)

        with qtbot.waitSignal(test_widget.dataChanged):
            widget.changeMe()

    def test_widget_with_prefix_path(self, qtbot, test_class):
        test_widget = test_class()
        qtbot.addWidget(test_widget)

        widget = ChangeWidget()
        test_widget.addWidget(widget)
        test_widget.setPrefixPath("dummy")

        assert widget.prefix_path == "dummy"

    def test_widget_without_prefix_path(self, qtbot, test_class):
        test_widget = test_class()
        qtbot.addWidget(test_widget)

        test_widget.addWidget(QWidget())
        test_widget.setPrefixPath("dummy")
