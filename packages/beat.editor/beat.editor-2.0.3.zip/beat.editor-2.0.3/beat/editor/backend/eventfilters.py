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

from PyQt5.QtCore import QEvent
from PyQt5.QtCore import QObject
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractSpinBox
from PyQt5.QtWidgets import QComboBox


class MouseWheelFilter(QObject):
    """Event filter to avoid spin boxes and combo boxes to get triggered
       when scrolling the mouse in for example a QScrollArea

       Based on https://stackoverflow.com/a/5821874/5843716
    """

    def eventFilter(self, obj, event):
        event_type = event.type()
        if event_type == QEvent.ChildAdded:
            widget = event.child()
            if isinstance(widget, QAbstractSpinBox) or isinstance(widget, QComboBox):
                widget.setFocusPolicy(Qt.StrongFocus)
        if isinstance(obj, QAbstractSpinBox) or isinstance(obj, QComboBox):
            if event_type == QEvent.HoverLeave:
                obj.clearFocus()
            elif event_type == QEvent.FocusIn:
                obj.setFocusPolicy(Qt.WheelFocus)
                event.accept()
                return False
            elif event_type == QEvent.FocusOut:
                obj.setFocusPolicy(Qt.StrongFocus)
                event.accept()
                return False
            elif event_type == QEvent.Wheel:
                if obj.focusPolicy() == Qt.WheelFocus:
                    event.accept()
                    return False
                else:
                    event.ignore()
                    return True

        return super().eventFilter(obj, event)
