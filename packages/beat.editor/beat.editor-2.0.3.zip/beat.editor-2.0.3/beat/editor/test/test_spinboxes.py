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
import pytest

from ..widgets.spinboxes import NumpySpinBox


@pytest.fixture()
def expected_values():
    return [
        (np.uint8, 477218588),
        (np.uint16, 477218588),
        (np.uint32, 477218588),
        (np.uint64, 4444444444444444444),
        (np.int8, -84),
        (np.int16, 24564),
        (np.int32, 1081950908),
        (np.int64, 4444444444444444444),
        (np.float32, 4.444445e16),
        (np.float64, 4.444444444444445e164),
    ]


class TestInvalidTypes:
    """Test using invalid types for creation"""

    @pytest.mark.parametrize("invalid_type", [None, np.bool, np.str])
    def test_invalid_type(self, qtbot, invalid_type):
        with pytest.raises(RuntimeError):
            NumpySpinBox(invalid_type)


class SpinBoxBaseTest:
    numpy_type = None

    @pytest.mark.parametrize("invalid_type", [None, np.bool, np.str])
    def test_set_invalid_type(self, qtbot, invalid_type):
        spinbox = NumpySpinBox(self.numpy_type)
        with pytest.raises(RuntimeError):
            spinbox.setNumpyType(invalid_type)

    def test_range(self, qtbot):
        spinbox = NumpySpinBox(self.numpy_type)
        qtbot.addWidget(spinbox)

        minimum = 0
        maximum = 10
        spinbox.setRange(minimum, maximum)
        assert spinbox.minimum() == minimum
        assert spinbox.maximum() == maximum

        spinbox.setValue(-10)
        assert spinbox.value == spinbox.minimum()

        spinbox.setValue(20)
        assert spinbox.value == spinbox.maximum()

    def test_valid_input(self, qtbot):
        spinbox = NumpySpinBox(self.numpy_type)
        qtbot.addWidget(spinbox)
        value = "42"

        with qtbot.waitSignal(spinbox.valueChanged):
            qtbot.keyClicks(spinbox, value)
        assert spinbox.value == spinbox.numpy_type(value)

    def test_invalid_input(self, qtbot, expected_values):
        spinbox = NumpySpinBox(self.numpy_type)
        qtbot.addWidget(spinbox)
        value = "44444444444444444444444444444444444444444444444444444444444"
        expected_value = None
        for item in expected_values:
            if spinbox.numpy_type == item[0]:
                expected_value = item[1]
                break

        assert expected_value is not None

        with qtbot.waitSignal(spinbox.valueChanged):
            qtbot.keyClicks(spinbox, value)
        assert spinbox.value == spinbox.numpy_type(expected_value)


class UintSpinBoxBaseTest(SpinBoxBaseTest):
    def test_invalid_range(self, qtbot):
        spinbox = NumpySpinBox(self.numpy_type)
        qtbot.addWidget(spinbox)

        spinbox.setRange(-10, 10)
        assert spinbox.minimum() == 0

    def test_values(self, qtbot):
        spinbox = NumpySpinBox(self.numpy_type)
        qtbot.addWidget(spinbox)

        spinbox.setRange(0, 10)

        spinbox.setValue(-10)
        assert spinbox.value == spinbox.minimum()

        spinbox.setValue(20)
        assert spinbox.value == spinbox.maximum()


class IntSpinBoxBaseTest(SpinBoxBaseTest):
    def test_values(self, qtbot):
        spinbox = NumpySpinBox(self.numpy_type)
        qtbot.addWidget(spinbox)

        spinbox.setRange(0, 10)

        spinbox.setValue(5)
        assert spinbox.value == 5

        spinbox.setValue(-5)
        assert spinbox.value == spinbox.minimum()


class FloatSpinBoxBaseTest(SpinBoxBaseTest):
    def test_values(self, qtbot):
        spinbox = NumpySpinBox(self.numpy_type)
        qtbot.addWidget(spinbox)

        spinbox.setRange(-10.45, 10.45)

        spinbox.setValue(5.32)
        assert spinbox.value == self.numpy_type(5.32)

        spinbox.setValue(-5.32)
        assert spinbox.value == self.numpy_type(-5.32)

        spinbox.setValue(-15)
        assert spinbox.value == spinbox.minimum()

        spinbox.setValue(15)
        assert spinbox.value == spinbox.maximum()


class TestUint8SpinBox(UintSpinBoxBaseTest):
    numpy_type = np.uint8


class TestUint16SpinBox(UintSpinBoxBaseTest):
    numpy_type = np.uint16


class TestUint32SpinBox(UintSpinBoxBaseTest):
    numpy_type = np.uint32


class TestUint64SpinBox(UintSpinBoxBaseTest):
    numpy_type = np.uint64


class TestInt8SpinBox(IntSpinBoxBaseTest):
    numpy_type = np.int8


class TestInt16SpinBox(IntSpinBoxBaseTest):
    numpy_type = np.int16


class TestInt32SpinBox(IntSpinBoxBaseTest):
    numpy_type = np.int32


class TestInt64SpinBox(IntSpinBoxBaseTest):
    numpy_type = np.int64


class TestFloat32SpinBox(FloatSpinBoxBaseTest):
    numpy_type = np.float32


class TestFloat64SpinBox(FloatSpinBoxBaseTest):
    numpy_type = np.float64


class TestTypeChange(SpinBoxBaseTest):
    numpy_type = np.uint8

    def test_invalid_range_uint8(self, qtbot):
        spinbox = NumpySpinBox(self.numpy_type)
        qtbot.addWidget(spinbox)

        spinbox.setRange(-10, 10)
        assert spinbox.minimum() == 0

    def test_values_uint8(self, qtbot):
        spinbox = NumpySpinBox(self.numpy_type)
        qtbot.addWidget(spinbox)

        spinbox.setRange(0, 10)

        spinbox.setValue(-10)
        assert spinbox.value == spinbox.minimum()

        spinbox.setValue(20)
        assert spinbox.value == spinbox.maximum()

    def test_values_from_uint8_to_float_64(self, qtbot):
        spinbox = NumpySpinBox(self.numpy_type)
        qtbot.addWidget(spinbox)

        self.numpy_type = np.float64

        with qtbot.waitSignal(spinbox.numpyTypeChanged):
            spinbox.setNumpyType(self.numpy_type)

        assert spinbox.numpy_type == self.numpy_type

        spinbox.setRange(-10.45, 10.45)

        spinbox.setValue(5.32)
        assert spinbox.value == self.numpy_type(5.32)

        spinbox.setValue(-5.32)
        assert spinbox.value == self.numpy_type(-5.32)

        spinbox.setValue(-15)
        assert spinbox.value == spinbox.minimum()

        spinbox.setValue(15)
        assert spinbox.value == spinbox.maximum()

    def test_type_change_with_same_type(self, qtbot):
        spinbox = NumpySpinBox(self.numpy_type)
        qtbot.addWidget(spinbox)

        with qtbot.assertNotEmitted(spinbox.numpyTypeChanged):
            spinbox.setNumpyType(self.numpy_type)

        assert spinbox.numpy_type == self.numpy_type
