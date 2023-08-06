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

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


class EditorListWidget(QWidget):
    """Container widget to show list of widgets"""

    dataChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._widget_list = []

        self.widget_layout = QVBoxLayout(self)
        self.widget_layout.addStretch(1)

    @property
    def widget_list(self):
        """List of the widgets contained"""

        return self._widget_list

    def addWidget(self, widget):
        """Add a new widget at the bottom of this list

        :param widget QWidget: widget to add
        """

        self._widget_list.append(widget)
        index = self.widget_layout.count() - 1
        self.widget_layout.insertWidget(index, widget)
        if hasattr(widget, "dataChanged"):
            widget.dataChanged.connect(self.dataChanged)
        self.dataChanged.emit()

    def removeWidget(self, widget):
        """Removes the widget from the list

        :param widget QWidget: widget to remove
        """

        self.widget_layout.removeWidget(widget)
        self._widget_list.pop(self._widget_list.index(widget))
        widget.setParent(None)
        self.dataChanged.emit()

    @pyqtSlot(str)
    def setPrefixPath(self, prefix_path):
        """Set the prefix path on all widgets if they provide that attribute

        :param prefix_path str: path to the prefix
        """

        for widget in self._widget_list:
            set_prefix = getattr(widget, "setPrefixPath", None)
            if callable(set_prefix):
                set_prefix(prefix_path)

    def clear(self):
        """Clear the content of the area"""

        while self._widget_list:
            self.removeWidget(self._widget_list[-1])


class ScrollWidget(QScrollArea):
    """Scroll area wrapper around an EditorListWidget"""

    dataChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=None)

        self.list_widget = EditorListWidget()
        self.setWidget(self.list_widget)
        self.setWidgetResizable(True)

        self.list_widget.dataChanged.connect(self.dataChanged)

    @property
    def widget_list(self):
        """Returns the list of widgets contained in this area"""

        return self.list_widget.widget_list

    def addWidget(self, widget):
        """Adds the widget to this area

        :param widget QWidget: widget to add
        """

        self.list_widget.addWidget(widget)

    def removeWidget(self, widget):
        """Removes the widget from this area

        :param widget QWidget: widget to remove
        """

        self.list_widget.removeWidget(widget)

    def clear(self):
        """Adds the content of this area"""

        self.list_widget.clear()

    @pyqtSlot(str)
    def setPrefixPath(self, prefix_path):
        """Set the prefix path on all widgets if they provide that attribute

        :param prefix_path str: path to the prefix
        """

        self.list_widget.setPrefixPath(prefix_path)
