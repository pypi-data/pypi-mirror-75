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

from PyQt5.QtCore import QLineF
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QGraphicsScene


class ToolchainScene(QGraphicsScene):

    """Playground scene for block objects"""

    def __init__(self, configuration):

        super().__init__()

        self.grid_size = configuration.get("grid_size", 36)
        self.grid_color = configuration.get("grid_color", [232, 232, 232, 255])

        if not isinstance(self.grid_size, int):
            raise TypeError(
                self.tr("Grid size configuration has to be of type integer")
            )

        if not isinstance(self.grid_color, list):
            raise TypeError(self.tr("Grid color configuration has to be of type list"))

        if (
            not all(isinstance(x, int) for x in self.grid_color)
            or len(self.grid_color) != 4
        ):
            raise TypeError(self.tr("Invalid grid element types or unmatching size"))

    def drawBackground(self, painter, rect):
        """Background grid"""

        leftVerticalLine = rect.left() - rect.left() % self.grid_size
        topHorizontalLine = rect.top() - rect.top() % self.grid_size
        lines = []

        for i in range(int(leftVerticalLine), int(rect.right()), self.grid_size):
            lines.append(QLineF(i, rect.top(), i, rect.bottom()))

        for i in range(int(topHorizontalLine), int(rect.bottom()), self.grid_size):
            lines.append(QLineF(rect.left(), i, rect.right(), i))

        self.pen = QPen()
        self.pen.setColor(QColor(*self.grid_color))
        self.pen.setWidth(0)
        painter.setPen(self.pen)
        painter.drawLines(lines)
