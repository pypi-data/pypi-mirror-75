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

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QInputDialog

from ..backend.asset import Asset
from ..backend.asset import AssetType
from ..widgets.parameterwidget import BoolSetupWidget
from ..widgets.parameterwidget import InputType
from ..widgets.parameterwidget import NumericalChoiceDialog
from ..widgets.parameterwidget import NumericalSetupWidget
from ..widgets.parameterwidget import ParameterWidget
from ..widgets.parameterwidget import StringSetupWidget
from .conftest import prefix
from .conftest import sync_prefix

# ------------------------------------------------------------------------------
# Constants


DEFAULT_ALGORITHM = "autonomous/parametrized/1"
UNSIGNED_TYPES = [InputType.UINT8, InputType.UINT16, InputType.UINT32, InputType.UINT64]


# ------------------------------------------------------------------------------
# Helpers


def get_algorithm_declaration(prefix_path, algorithm_name):
    asset = Asset(prefix_path, AssetType.ALGORITHM, algorithm_name)
    return asset.declaration


def get_parameters(prefix_path, algorithm_name):
    return get_algorithm_declaration(prefix_path, algorithm_name)["parameters"]


def parameter_default_map(prefix_path, algorithm_name):
    sync_prefix()
    parameters = get_parameters(prefix_path, algorithm_name)
    return {name: value["default"] for name, value in parameters.items()}


# ------------------------------------------------------------------------------
# Fixtures


@pytest.fixture(params=InputType.numerical_types())
def numerical_input_type(request):
    return request.param


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


@pytest.fixture()
def parametrized_algorithm():
    return DEFAULT_ALGORITHM


@pytest.fixture(params=parameter_default_map(prefix, DEFAULT_ALGORITHM))
def parameter_name(request):
    return request.param


# ------------------------------------------------------------------------------
# Tests


class TestInputType:
    """Test the InputType enum class"""

    def test_numerical_info(self, numerical_input_type):
        type_ = type(numerical_input_type.numpy_info)
        assert type_ in [np.iinfo, np.finfo]

    @pytest.mark.parametrize(
        "input_type",
        [item for item in InputType if item not in InputType.numerical_types()],
    )
    def test_non_numerical_info(self, input_type):
        with pytest.raises(RuntimeError):
            input_type.numpy_info


class TestNumericalChoiceDialog:
    """Test the NumericalChoiceDialog class"""

    def test_dialog(self, qtbot, numerical_input_type):
        dialog = NumericalChoiceDialog(numerical_input_type)
        qtbot.addWidget(dialog)
        qtbot.mouseClick(
            dialog.buttons.button(QDialogButtonBox.Ok), QtCore.Qt.LeftButton
        )
        assert dialog.value() == 0

    @pytest.mark.parametrize(
        "input_type",
        [item for item in InputType if item not in InputType.numerical_types()],
    )
    def test_non_numerical_info(self, input_type):
        with pytest.raises(RuntimeError):
            NumericalChoiceDialog(input_type)


class TestBoolSetupWidget:
    """Test the BoolSetupWidget is set up and works correctly"""

    @pytest.fixture()
    def default_state_dump(self):
        return {"default": True}

    @pytest.fixture()
    def bool_setup_widget(self, qtbot, default_state_dump):
        bool_setup_widget = BoolSetupWidget()
        qtbot.addWidget(bool_setup_widget)
        assert bool_setup_widget.dump() == default_state_dump
        return bool_setup_widget

    @pytest.mark.parametrize("default", [True, False])
    def test_load_and_dump(self, qtbot, bool_setup_widget, default):
        new_setup = {"default": default}

        if default:
            with qtbot.assertNotEmitted(bool_setup_widget.dataChanged):
                bool_setup_widget.load(new_setup)
        else:
            with qtbot.waitSignal(bool_setup_widget.dataChanged):
                bool_setup_widget.load(new_setup)

        assert bool_setup_widget.dump() == new_setup

    @pytest.mark.parametrize("default", [True, False])
    def test_change_default_value(self, qtbot, bool_setup_widget, default):
        new_setup = {"default": default}

        if default:
            with qtbot.assertNotEmitted(bool_setup_widget.dataChanged):
                qtbot.mouseClick(bool_setup_widget.true_button, QtCore.Qt.LeftButton)
        else:
            with qtbot.waitSignal(bool_setup_widget.dataChanged):
                qtbot.mouseClick(bool_setup_widget.false_button, QtCore.Qt.LeftButton)

        assert bool_setup_widget.dump() == new_setup


class TestStringSetupWidget:
    """Test the StringSetupWidget is set up and works correctly"""

    @pytest.fixture()
    def default_state_dump(self):
        return {"default": ""}

    @pytest.fixture()
    def string_setup_widget(self, qtbot, default_state_dump):
        string_setup_widget = StringSetupWidget()
        qtbot.addWidget(string_setup_widget)
        assert string_setup_widget.dump() == default_state_dump
        return string_setup_widget

    def test_load_and_dump_single(self, string_setup_widget):
        new_setup = {"default": "text 2"}

        string_setup_widget.load(new_setup)
        assert string_setup_widget.dump() == new_setup

    def test_load_and_dump_choices(self, qtbot, string_setup_widget):
        new_setup = {"default": "text 2", "choice": ["text 1", "text 2", "text 3"]}

        with qtbot.waitSignal(string_setup_widget.dataChanged):
            string_setup_widget.load(new_setup)
        assert string_setup_widget.dump() == new_setup

    def test_load_and_dump_invalid_same_choice(
        self, string_setup_widget, default_state_dump
    ):
        new_setup = {"default": "text 2", "choice": ["text 1", "text 2", "text 1"]}

        with pytest.raises(RuntimeError) as excinfo:
            string_setup_widget.load(new_setup)
        assert "Invalid duplicate choice" in str(excinfo.value)
        assert string_setup_widget.dump() == default_state_dump

    def test_load_and_dump_invalid_default_choice(
        self, string_setup_widget, default_state_dump
    ):
        new_setup = {"default": "text 4", "choice": ["text 1", "text 2", "text 3"]}

        with pytest.raises(RuntimeError) as excinfo:
            string_setup_widget.load(new_setup)
        assert "Invalid default choice" in str(excinfo.value)
        assert string_setup_widget.dump() == default_state_dump

    def test_select_choices_setup(self, qtbot, string_setup_widget):
        setup_choices_clicked = {"default": "", "choice": []}

        with qtbot.waitSignal(string_setup_widget.dataChanged):
            qtbot.mouseClick(string_setup_widget.choices_button, QtCore.Qt.LeftButton)
        assert string_setup_widget.dump() == setup_choices_clicked

    def test_single_change_default(self, qtbot, string_setup_widget):
        default_changed = {"default": "newstring"}

        with qtbot.waitSignal(string_setup_widget.dataChanged):
            qtbot.keyClicks(
                string_setup_widget.single_default_lineedit, default_changed["default"]
            )
        assert string_setup_widget.dump() == default_changed

    def test_choices_click_add_select(self, qtbot, monkeypatch, string_setup_widget):
        change_to_choices = {"default": "", "choice": []}
        setup_choices = {"default": "text 2", "choice": ["text 1", "text 2", "text 3"]}

        # click choices radio button
        with qtbot.waitSignal(string_setup_widget.dataChanged):
            qtbot.mouseClick(string_setup_widget.choices_button, QtCore.Qt.LeftButton)
        assert string_setup_widget.dump() == change_to_choices

        # add some choices
        for i in range(0, 3):
            with qtbot.waitSignal(string_setup_widget.dataChanged):
                monkeypatch.setattr(
                    QInputDialog,
                    "getText",
                    classmethod(lambda *args: (setup_choices["choice"][i], True)),
                )
                string_setup_widget.add_button.click()

        # select default
        with qtbot.waitSignal(string_setup_widget.dataChanged):
            qtbot.keyClicks(
                string_setup_widget.choices_default_combobox, setup_choices["choice"][1]
            )

        assert string_setup_widget.dump() == setup_choices

    def test_choices_click_remove(self, qtbot, monkeypatch, string_setup_widget):
        setup_choices = {"default": "text 2", "choice": ["text 1", "text 2", "text 3"]}
        removed_choices = {"default": "text 3", "choice": ["text 1", "text 3"]}

        # loading data
        with qtbot.waitSignal(string_setup_widget.dataChanged):
            string_setup_widget.load(setup_choices)
        assert string_setup_widget.dump() == setup_choices

        # remove a choice
        string_setup_widget.choices_listwidget.setCurrentRow(1)
        with qtbot.waitSignal(string_setup_widget.dataChanged):
            qtbot.mouseClick(string_setup_widget.remove_button, QtCore.Qt.LeftButton)

        assert string_setup_widget.dump() == removed_choices

    def test_choices_click_add_invalid_same_choice(
        self, qtbot, monkeypatch, string_setup_widget
    ):
        change_to_choices = {"default": "", "choice": []}
        wrong_setup_choices = {
            "default": "text 2",
            "choice": ["text 1", "text 2", "text 1"],
        }
        correct_setup_choices = {"default": "text 2", "choice": ["text 1", "text 2"]}

        # click choices radio button
        with qtbot.waitSignal(string_setup_widget.dataChanged):
            qtbot.mouseClick(string_setup_widget.choices_button, QtCore.Qt.LeftButton)
        assert string_setup_widget.dump() == change_to_choices

        # add some choices
        for i in range(0, 3):
            monkeypatch.setattr(
                QInputDialog,
                "getText",
                classmethod(lambda *args: (wrong_setup_choices["choice"][i], True)),
            )
            string_setup_widget.add_button.click()

        # select default
        with qtbot.waitSignal(string_setup_widget.dataChanged):
            qtbot.keyClicks(
                string_setup_widget.choices_default_combobox,
                wrong_setup_choices["choice"][1],
            )

        assert string_setup_widget.dump() == correct_setup_choices


class TestNumericalSetupWidget:
    """Test the NumericalSetupWidget is set up and works correctly"""

    @pytest.fixture()
    def default_state_dump(self):
        return {"default": 0}

    @pytest.fixture()
    def numerical_setup_widget(self, qtbot, default_state_dump, numerical_input_type):
        numerical_setup_widget = NumericalSetupWidget(numerical_input_type)
        qtbot.addWidget(numerical_setup_widget)
        assert numerical_setup_widget.dump() == default_state_dump
        return numerical_setup_widget

    def test_load_and_dump_single(self, numerical_setup_widget):
        new_setup = {"default": 3}

        numerical_setup_widget.load(new_setup)
        assert numerical_setup_widget.dump() == new_setup

    def test_load_and_dump_choices(self, qtbot, numerical_setup_widget):
        new_setup = {"default": 3, "choice": [2, 3, 4]}

        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            numerical_setup_widget.load(new_setup)
        assert numerical_setup_widget.dump() == new_setup

    def test_load_and_dump_invalid_same_choice(
        self, numerical_setup_widget, default_state_dump
    ):
        new_setup = {"default": 3, "choice": [2, 3, 2]}

        with pytest.raises(RuntimeError) as excinfo:
            numerical_setup_widget.load(new_setup)
        assert "Invalid duplicate choice" in str(excinfo.value)

        assert numerical_setup_widget.dump() == default_state_dump

    def test_load_and_dump_invalid_default_choice(
        self, numerical_setup_widget, default_state_dump
    ):
        new_setup = {"default": 5, "choice": [2, 3, 4]}

        with pytest.raises(RuntimeError) as excinfo:
            numerical_setup_widget.load(new_setup)
        assert "Invalid default choice" in str(excinfo.value)

        assert numerical_setup_widget.dump() == default_state_dump

    def test_load_and_dump_range(self, qtbot, numerical_setup_widget):
        new_setup = {"default": 3, "range": [2, 4]}

        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            numerical_setup_widget.load(new_setup)
        assert numerical_setup_widget.dump() == new_setup

    def test_load_and_dump_invalid_same_range(
        self, numerical_setup_widget, default_state_dump
    ):
        new_setup = {"default": 2, "range": [2, 2]}

        with pytest.raises(RuntimeError) as excinfo:
            numerical_setup_widget.load(new_setup)
        assert "Invalid duplicate range" in str(excinfo.value)

        assert numerical_setup_widget.dump() == default_state_dump

    def test_load_and_dump_invalid_default_range(
        self, numerical_setup_widget, default_state_dump
    ):
        new_setup = {"default": 5, "range": [2, 4]}

        with pytest.raises(RuntimeError) as excinfo:
            numerical_setup_widget.load(new_setup)
        assert "Invalid default or min/max range" in str(excinfo.value)

        assert numerical_setup_widget.dump() == default_state_dump

    def test_load_and_dump_invalid_min_max_range(
        self, numerical_setup_widget, default_state_dump
    ):
        new_setup = {"default": 4, "range": [4, 2]}

        with pytest.raises(RuntimeError) as excinfo:
            numerical_setup_widget.load(new_setup)
        assert "Invalid default or min/max range" in str(excinfo.value)

        assert numerical_setup_widget.dump() == default_state_dump

    def test_setup_type_selection(
        self, qtbot, numerical_setup_widget, default_state_dump
    ):
        setup_choices_clicked = {"default": 0, "choice": []}
        setup_range_clicked = {"default": 0, "range": [-10, 10]}
        setup_range_clicked_uint = {"default": 0, "range": [0, 10]}

        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            qtbot.mouseClick(
                numerical_setup_widget.choices_button, QtCore.Qt.LeftButton
            )
        assert numerical_setup_widget.dump() == setup_choices_clicked

        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            qtbot.mouseClick(numerical_setup_widget.range_button, QtCore.Qt.LeftButton)

        if numerical_setup_widget.current_type in UNSIGNED_TYPES:
            assert numerical_setup_widget.dump() == setup_range_clicked_uint
        else:
            assert numerical_setup_widget.dump() == setup_range_clicked

        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            qtbot.mouseClick(numerical_setup_widget.single_button, QtCore.Qt.LeftButton)
        assert numerical_setup_widget.dump() == default_state_dump

    def test_single_change_default(
        self, qtbot, numerical_setup_widget, default_state_dump
    ):
        default_changed = {"default": 3}

        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            qtbot.keyClicks(
                numerical_setup_widget.single_default_spinbox,
                str(default_changed["default"]),
            )
        assert numerical_setup_widget.dump() == default_changed

    def test_single_change_default_invalid_input(
        self, qtbot, numerical_setup_widget, expected_values, default_state_dump
    ):
        value = "44444444444444444444444444444444444444444444444444444444444"

        spinbox = numerical_setup_widget.single_default_spinbox

        expected_value = None
        for item in expected_values:
            if spinbox.numpy_type == item[0]:
                expected_value = item[1]
                break

        assert expected_value is not None

        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            qtbot.keyClicks(spinbox, value)
        assert spinbox.value == spinbox.numpy_type(expected_value)
        default_state_dump["default"] = spinbox.value
        assert numerical_setup_widget.dump() == default_state_dump

    def test_choices_click_add(self, qtbot, monkeypatch, numerical_setup_widget):
        change_to_choices = {"default": 0, "choice": []}
        setup_choices = {"default": 2, "choice": [1, 2, 3]}

        # click choices radio button
        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            qtbot.mouseClick(
                numerical_setup_widget.choices_button, QtCore.Qt.LeftButton
            )
        assert numerical_setup_widget.dump() == change_to_choices

        # add some choices
        for i in range(0, 3):
            with qtbot.waitSignal(numerical_setup_widget.dataChanged):
                monkeypatch.setattr(
                    NumericalChoiceDialog,
                    "getChoiceValue",
                    classmethod(lambda *args: (str(setup_choices["choice"][i]), True)),
                )
                numerical_setup_widget.add_button.click()

        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            qtbot.keyClicks(
                numerical_setup_widget.choices_default_combobox,
                str(setup_choices["choice"][1]),
            )

        assert numerical_setup_widget.dump() == setup_choices

    def test_choices_click_remove(self, qtbot, monkeypatch, numerical_setup_widget):
        setup_choices = {"default": 2, "choice": [1, 2, 3]}
        removed_choices = {"default": 3, "choice": [1, 3]}

        # loading data
        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            numerical_setup_widget.load(setup_choices)
        assert numerical_setup_widget.dump() == setup_choices

        qtbot.keyClicks(
            numerical_setup_widget.choices_default_combobox,
            str(setup_choices["choice"][1]),
        )

        assert numerical_setup_widget.dump() == setup_choices

        # remove a choice
        numerical_setup_widget.choices_listwidget.setCurrentRow(1)
        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            qtbot.mouseClick(numerical_setup_widget.remove_button, QtCore.Qt.LeftButton)

        assert numerical_setup_widget.dump() == removed_choices

    def test_choices_click_add_invalid_same_choice(
        self, qtbot, monkeypatch, numerical_setup_widget
    ):
        change_to_choices = {"default": 0, "choice": []}
        wrong_setup_choices = {"default": 2, "choice": [1, 2, 1]}
        correct_setup_choices = {"default": 2, "choice": [1, 2]}

        # click choices radio button
        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            qtbot.mouseClick(
                numerical_setup_widget.choices_button, QtCore.Qt.LeftButton
            )
        assert numerical_setup_widget.dump() == change_to_choices

        # add some choices
        for i in range(0, 3):
            monkeypatch.setattr(
                NumericalChoiceDialog,
                "getChoiceValue",
                classmethod(
                    lambda *args: (str(wrong_setup_choices["choice"][i]), True)
                ),
            )
            numerical_setup_widget.add_button.click()

        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            qtbot.keyClicks(
                numerical_setup_widget.choices_default_combobox,
                str(wrong_setup_choices["choice"][1]),
            )

        assert numerical_setup_widget.dump() == correct_setup_choices

    def test_choices_click_add_invalid_input(
        self, qtbot, monkeypatch, numerical_setup_widget, expected_values
    ):
        value1 = "44444444444444444444444444444444444444444444444444444444444"
        value2 = "44444444444444444444444444444444444444444444444444444444445"
        value3 = "44444444444444444444444444444444444444444444444444444444446"
        overflow_float_64 = 4.4444444444444445e58
        change_to_choices = {"default": 0, "choice": []}
        setup_choices_float_32 = {"default": np.inf, "choice": [np.inf, np.inf, np.inf]}
        setup_choices_float_64 = {
            "default": overflow_float_64,
            "choice": [overflow_float_64, overflow_float_64, overflow_float_64],
        }

        # click choices radio button
        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            qtbot.mouseClick(
                numerical_setup_widget.choices_button, QtCore.Qt.LeftButton
            )
        assert numerical_setup_widget.dump() == change_to_choices

        expected_value = None
        for item in expected_values:
            if numerical_setup_widget.current_type.np_type == item[0]:
                expected_value = item[1]
                break

        assert expected_value is not None

        # add some choices
        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            monkeypatch.setattr(
                NumericalChoiceDialog,
                "getChoiceValue",
                classmethod(lambda *args: (value1, True)),
            )
            numerical_setup_widget.add_button.click()
            monkeypatch.setattr(
                NumericalChoiceDialog,
                "getChoiceValue",
                classmethod(lambda *args: (value2, True)),
            )
            numerical_setup_widget.add_button.click()
            monkeypatch.setattr(
                NumericalChoiceDialog,
                "getChoiceValue",
                classmethod(lambda *args: (value3, True)),
            )
            numerical_setup_widget.add_button.click()

        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            qtbot.keyClicks(numerical_setup_widget.choices_default_combobox, value2)

        if numerical_setup_widget.current_type.np_type not in [np.float32, np.float64]:
            with pytest.raises(RuntimeError) as excinfo:
                numerical_setup_widget.dump()
            assert "Invalid default value: OverflowError" in str(excinfo.value)
        elif numerical_setup_widget.current_type.np_type == np.float32:
            assert numerical_setup_widget.dump() == setup_choices_float_32
        else:
            assert numerical_setup_widget.dump() == setup_choices_float_64

        # remove a choice
        numerical_setup_widget.choices_listwidget.setCurrentRow(1)
        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            qtbot.mouseClick(numerical_setup_widget.remove_button, QtCore.Qt.LeftButton)

        if numerical_setup_widget.current_type.np_type not in [np.float32, np.float64]:
            with pytest.raises(RuntimeError) as excinfo:
                numerical_setup_widget.dump()
            assert "Invalid default value: OverflowError" in str(excinfo.value)
        elif numerical_setup_widget.current_type.np_type == np.float32:
            setup_choices_float_32["choice"].pop(0)
            assert numerical_setup_widget.dump() == setup_choices_float_32
        else:
            setup_choices_float_64["choice"].pop(0)
            assert numerical_setup_widget.dump() == setup_choices_float_64

    def test_range_change_default_min_max(self, qtbot, numerical_setup_widget):
        setup_range_clicked = {"default": 0, "range": [-10, 10]}
        setup_range_clicked_uint = {"default": 0, "range": [0, 10]}
        range_min_type = 1
        range_max_type = 4
        new_setup = {"default": 3, "range": [-101, 104]}
        new_setup_uint = {"default": 3, "range": [1, 104]}

        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            qtbot.mouseClick(numerical_setup_widget.range_button, QtCore.Qt.LeftButton)
        if numerical_setup_widget.current_type in UNSIGNED_TYPES:
            assert numerical_setup_widget.dump() == setup_range_clicked_uint
        else:
            assert numerical_setup_widget.dump() == setup_range_clicked

        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            qtbot.keyClicks(
                numerical_setup_widget.range_maximum_spinbox, str(range_max_type)
            )
        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            qtbot.keyClicks(
                numerical_setup_widget.range_default_spinbox, str(new_setup["default"])
            )
        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            qtbot.keyClicks(
                numerical_setup_widget.range_minimum_spinbox, str(range_min_type)
            )
        if numerical_setup_widget.current_type in UNSIGNED_TYPES:
            assert numerical_setup_widget.dump() == new_setup_uint
        else:
            assert numerical_setup_widget.dump() == new_setup

    def test_range_add_invalid_inputs(
        self, qtbot, monkeypatch, numerical_setup_widget, expected_values
    ):
        value = 12
        value1 = 44444444444444444444444444444444444444444444444444444444444e608
        required_invalid_setup = {"default": value, "range": [value, value1]}

        expected_value = None
        for item in expected_values:
            if numerical_setup_widget.current_type.np_type == item[0]:
                expected_value = item[1]
                break

        assert expected_value is not None

        # Adding invalid values
        with qtbot.waitSignal(numerical_setup_widget.dataChanged):
            numerical_setup_widget.load(required_invalid_setup)

        max_value = numerical_setup_widget.current_type.numpy_info.max
        valid_setup = {"default": value, "range": [value, max_value]}

        assert numerical_setup_widget.dump() == valid_setup


class TestParameterWidget:
    """Test the ParameterWidget is set up and works correctly"""

    def test_parameter_load_dump(
        self, qtbot, test_prefix, parametrized_algorithm, parameter_name
    ):
        parameters = get_parameters(test_prefix, parametrized_algorithm)
        parameter = parameters[parameter_name]

        parameter_widget = ParameterWidget()
        qtbot.addWidget(parameter_widget)

        with qtbot.waitSignal(parameter_widget.dataChanged):
            parameter_widget.load(parameter)

        assert parameter_widget.dump() == parameter

    def test_parameter_change_combobox_numpy_types(self, qtbot, numerical_input_type):
        selected_type = numerical_input_type.name.lower()
        parameter = {"default": 0, "type": selected_type}
        parameter_widget = ParameterWidget()
        qtbot.addWidget(parameter_widget)

        with qtbot.waitSignal(parameter_widget.dataChanged):
            qtbot.keyClicks(parameter_widget.basetype_comboxbox, selected_type)

        assert parameter_widget.dump() == parameter

    def test_parameter_change_combobox_string_type(self, qtbot):
        selected_type = "string"
        parameter = {"default": "", "type": selected_type}
        parameter_widget = ParameterWidget()
        qtbot.addWidget(parameter_widget)

        with qtbot.waitSignal(parameter_widget.dataChanged):
            qtbot.keyClicks(parameter_widget.basetype_comboxbox, selected_type)

        assert parameter_widget.dump() == parameter

    def test_parameter_change_combobox_bool_type(self, qtbot):
        selected_type = "bool"
        parameter = {"default": True, "type": selected_type}
        parameter_widget = ParameterWidget()
        qtbot.addWidget(parameter_widget)

        with qtbot.waitSignal(parameter_widget.dataChanged):
            qtbot.keyClicks(parameter_widget.basetype_comboxbox, selected_type)

        assert parameter_widget.dump() == parameter

    def test_parameter_change_description_numpy_types(
        self, qtbot, numerical_input_type
    ):
        selected_type = numerical_input_type.name.lower()
        description = "some description"
        parameter = {"default": 0, "type": selected_type, "description": description}
        parameter_widget = ParameterWidget()
        qtbot.addWidget(parameter_widget)

        with qtbot.waitSignal(parameter_widget.dataChanged):
            qtbot.keyClicks(parameter_widget.basetype_comboxbox, selected_type)
            qtbot.keyClicks(parameter_widget.description_lineedit, description)

        assert parameter_widget.dump() == parameter

    def test_parameter_change_description_string_type(self, qtbot):
        selected_type = "string"
        description = "some description"
        parameter = {"default": "", "type": selected_type, "description": description}
        parameter_widget = ParameterWidget()
        qtbot.addWidget(parameter_widget)

        with qtbot.waitSignal(parameter_widget.dataChanged):
            qtbot.keyClicks(parameter_widget.basetype_comboxbox, selected_type)
            qtbot.keyClicks(parameter_widget.description_lineedit, description)

        assert parameter_widget.dump() == parameter

    def test_parameter_change_description_bool_type(self, qtbot):
        selected_type = "bool"
        description = "some description"
        parameter = {"default": True, "type": selected_type, "description": description}
        parameter_widget = ParameterWidget()
        qtbot.addWidget(parameter_widget)

        with qtbot.waitSignal(parameter_widget.dataChanged):
            qtbot.keyClicks(parameter_widget.basetype_comboxbox, selected_type)
            qtbot.keyClicks(parameter_widget.description_lineedit, description)

        assert parameter_widget.dump() == parameter
