# vim: set fileencoding=utf-8 :
###############################################################################
#                                                                             #
# Copyright (c) 2020 Idiap Research Institute, http://www.idiap.ch/           #
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


from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtWidgets import QWidget

NAME_REGULAREXPRESSION = QRegularExpression("^[a-zA-Z_][a-zA-Z0-9_-]*$")


class NameLineEdit(QLineEdit):
    """Line edit equipped with a validator for name related pattern properties"""

    def __init__(self, contents=None, parent=None):
        if contents is not None and not isinstance(contents, str):
            raise TypeError(f"Invalid contents parameter type {type(contents)}")

        if parent is not None and not isinstance(parent, QWidget):
            raise TypeError(f"Invalid parent parameter type {type(parent)}")

        super().__init__(contents, parent)

        self.setValidator(QRegularExpressionValidator(NAME_REGULAREXPRESSION, self))


class NameItemDelegate(QStyledItemDelegate):
    """Item delegate providing a NameLineEdit so add new entries follows the rules
       set in the schema
    """

    def createEditor(self, parent, options, index):
        """Create a name validated line edit"""

        return NameLineEdit(parent=parent)
