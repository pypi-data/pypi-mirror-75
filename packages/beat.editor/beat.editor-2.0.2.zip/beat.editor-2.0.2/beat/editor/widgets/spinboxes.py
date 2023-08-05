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

import numpy as np

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QValidator
from PyQt5.QtWidgets import QAbstractSpinBox

from ..decorators import frozen


@frozen
class NumpySpinBox(QAbstractSpinBox):
    """Generic spinbox base class using numpy types

       Requires initialization with the numpy
       type that will be used.

       The three following signals are provided:
           - valueChanged
           - minimumChanged
           - maximumChanged
    """

    numpyTypeChanged = pyqtSignal()
    valueChanged = pyqtSignal()
    minimumChanged = pyqtSignal()
    maximumChanged = pyqtSignal()

    def __init__(self, numpy_type, parent=None):
        """Constructor

        :param parent QWidget: parent widget
        """

        super().__init__(parent)

        self._numpy_type = None

        self.setNumpyType(numpy_type)

        self.lineEdit().textEdited.connect(self.__onTextEdited)

    @pyqtSlot()
    def __onTextEdited(self):
        """Act when the spinbox line edit content has been changed"""

        input_ = self.lineEdit().text()
        pos = 0
        is_valid, input_, pos = self.validate(input_, pos)
        if is_valid == QValidator.Acceptable:
            self.setValue(self.valueFromText(input_, pos))
        else:
            self.lineEdit().setText(self.textFromValue(self.value()))

    def textFromValue(self, value):
        """Returns the text version of value

        :param value numpy_type: value to change to text
        """

        text = self._numpy_type(value).astype("str")
        if np.issubdtype(self._numpy_type, np.floating):
            if text.endswith(".0"):
                text = text[:-2]
        return text

    def valueFromText(self, text, pos):
        """Returns the value contained in the text

        :param text str: text to change in numpy_type
        :param pos int: position to start considerating the text from
        """

        return self._numpy_type(text)

    def minimum(self):
        """Returns the spin box minimum value"""

        return self._minimum

    def setMinimum(self, minimum):
        """Set the minium value of the spin box.

        In case the value given is outside of the spin box range,
        it will be adapated.

        :param minimum numpy_type: minimum value
        """

        if self._minimum == minimum:
            return

        if minimum > self.maximum():
            minimum = self.maximum()
        elif minimum < self._info.min:
            minimum = self._info.min

        self._minimum = self._numpy_type(minimum)
        self.minimumChanged.emit()

    def maximum(self):
        """Returns the spin box maximum value"""

        return self._maximum

    def setMaximum(self, maximum):
        """Set the maximum value of the spin box.

        In case the value given is outside of the spin box range,
        it will be adapated.

        :param maximum numpy_type: maximum value
        """

        if self._maximum == maximum:
            return

        if maximum < self.minimum():
            maximum = self.minimum()
        elif maximum > self._info.max:
            maximum = self._info.max

        self._maximum = self._numpy_type(maximum)
        self.maximumChanged.emit()

    def setRange(self, minimum, maximum):
        """Set the range of the spin box.

        In case the values given are outside of the type range,
        they will be adapated.

        :param minimum numpy_type: minimum value
        :param maximum numpy_type: maximum value
        """

        self.setMinimum(minimum)
        self.setMaximum(maximum)

    def value(self):
        """Returns the spin box current value"""

        return self._value

    def setValue(self, value):
        """Set the value of the spin box.

        If the value is outside the spin box range, it will
        be adapted.

        :param value numpy_type: value to set
        """

        if self._value == value:
            return

        if value > self.maximum():
            value = self.maximum()
        elif value < self.minimum():
            value = self.minimum()

        self.lineEdit().setText(self.textFromValue(value))
        self._value = self._numpy_type(value)

        self.valueChanged.emit()

    value = pyqtProperty(
        type="QVariant", fget=value, fset=setValue, notify=valueChanged, user=True
    )

    def stepBy(self, steps):
        """Update the value of the spin box by steps.

        This method is called for example when clicking on the arrow
        or using the keyboard.

        :param steps int: step to increment/decrement the spin box
        """

        new_value = self.value

        if steps < 0 and new_value + steps < self.minimum():
            new_value = self.minimum()
        elif steps > 0 and new_value + steps > self.maximum():
            new_value = self.maximum()
        else:
            new_value += steps

        self.setValue(new_value)

    def validate(self, input_, pos):
        """Validate the input value

        :param input_ text: text to to validate
        :param pos int: start of text to consider
        """

        is_valid = QValidator.Acceptable
        try:
            value = self.valueFromText(input_, pos)
        except (ValueError, OverflowError):
            is_valid = QValidator.Invalid
        else:
            if value < self.minimum() or value > self.maximum():
                is_valid = QValidator.Invalid

        return is_valid, input_, pos

    def stepEnabled(self):
        """Returns which kind of steps are available to modify the value
        of the spin box
        """

        return QAbstractSpinBox.StepUpEnabled | QAbstractSpinBox.StepDownEnabled

    def numpyType(self):
        """Returns the numpy type of the spinbox

        :return: the numpy type used
        """

        return self._numpy_type

    def setNumpyType(self, numpy_type):
        """Sets the input type of the spin box

        :param value numpy_type: value to set
        """

        if numpy_type is None or not np.issubdtype(numpy_type, np.number):
            raise RuntimeError(f"Invalid type {numpy_type}")

        if self._numpy_type != numpy_type:
            self._numpy_type = numpy_type
            if np.issubdtype(self._numpy_type, np.floating):
                self._info = np.finfo(self._numpy_type)
            else:
                self._info = np.iinfo(self._numpy_type)

            self._minimum = self._info.min
            self._maximum = self._info.max
            self._value = None

            self.setInputMethodHints(Qt.ImhFormattedNumbersOnly)

            self.setValue(0)

            self.numpyTypeChanged.emit()

    numpy_type = pyqtProperty(
        str, fget=numpyType, fset=setNumpyType, notify=numpyTypeChanged
    )
