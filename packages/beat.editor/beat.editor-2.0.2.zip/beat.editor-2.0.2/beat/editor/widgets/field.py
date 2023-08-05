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

from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget

from .validatedhelpers import NameLineEdit


class FieldWidget(QWidget):
    """Class representing a dataformat field"""

    def __init__(self, dataformat_model, parent=None):
        """Constructor"""

        super().__init__(parent)

        self.dataformat_name = NameLineEdit()
        self.dataformat_box = QComboBox()
        self.dataformat_box.setModel(dataformat_model)

        layout = QGridLayout(self)
        layout.addWidget(self.dataformat_name, 0, 0)
        layout.addWidget(self.dataformat_box, 0, 1)

    @property
    def format_name(self):
        """Data format name property"""

        return self.dataformat_name.text()

    @format_name.setter
    def format_name(self, name):
        self.dataformat_name.setText(name)

    @property
    def format_type(self):
        """Data format type property"""

        return self.dataformat_box.currentText()

    @format_type.setter
    def format_type(self, name):
        self.dataformat_box.setCurrentText(name)
