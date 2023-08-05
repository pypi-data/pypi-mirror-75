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

from enum import Enum
from enum import unique

import numpy as np

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from ..utils import dataformat_basetypes
from .spinboxes import NumpySpinBox


@unique
class InputType(Enum):
    """All possible assets available on the BEAT platform"""

    UNKNOWN = None
    INT8 = np.int8
    INT16 = np.int16
    INT32 = np.int32
    INT64 = np.int64
    UINT8 = np.uint8
    UINT16 = np.uint16
    UINT32 = np.uint32
    UINT64 = np.uint64
    FLOAT32 = np.float32
    FLOAT64 = np.float64
    BOOL = np.bool
    STRING = np.str

    def __init__(self, np_type):
        super().__init__()
        self.np_type = np_type

    @property
    def numpy_info(self):
        info = None

        if self is InputType.UNKNOWN:
            raise RuntimeError(f"Invalid type")
        elif np.issubdtype(self.np_type, np.floating):
            info = np.finfo(self.np_type)
        elif np.issubdtype(self.np_type, np.integer):
            info = np.iinfo(self.np_type)
        else:
            raise RuntimeError(f"No information available for {self}")

        return info

    @staticmethod
    def numerical_types():
        return [
            item
            for item in InputType
            if item not in [InputType.UNKNOWN, InputType.BOOL, InputType.STRING]
        ]


class StackedWidget(QStackedWidget):
    """Subclass that will use the current widget height to adjust the stack
    size.

    This allows to keep a compact widget.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

    def sizeHint(self):
        """Returns a size hint based on the current widget in place of the
        biggest of all widgets added.
        """

        size = super().size()
        current_size_hint = self.currentWidget().sizeHint()
        size.setHeight(current_size_hint.height())
        return size

    def minimumSizeHint(self):
        """Returns a minimum size hint base on the current widget in place of
        the biggest of all widgets added.
        """

        size = super().size()
        current_size_hint = self.currentWidget().minimumSizeHint()
        size.setHeight(current_size_hint.height())
        return size


class NumericalChoiceDialog(QDialog):
    """Dialog to retrieve a value to to add to a choice list"""

    def __init__(self, selected_type, parent=None):
        """Constructor

        :param selected_type: current basetype
        :param parent QWidget: parent widget
        """

        super().__init__(parent)

        self.setWindowTitle(self.tr("Input"))
        self.label = QLabel(self.tr("New Choice:"))
        self.spinbox = NumpySpinBox(selected_type.np_type)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.spinbox)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )
        layout.addWidget(self.buttons)

        # Signals/Slots connection
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def value(self):
        """Returns the value selected"""

        return self.spinbox.value

    @staticmethod
    def getChoiceValue(selected_type, parent=None):
        """Static method to create the dialog and return qdialog accepted/spinbox value

        :param selected_type: current basetype
        :param parent QWidget: parent widget
        """

        dialog = NumericalChoiceDialog(selected_type, parent)
        result = dialog.exec_()
        value = None

        if result == QDialog.Accepted:
            value = dialog.value()

        return (value, result)


class BoolSetupWidget(QWidget):
    """Editor to setup a boolean parameter"""

    dataChanged = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor

        :param parent QWidget: parent widget
        """

        super().__init__(parent)

        # Member variables
        # Added self for auto-exclusion to work correctly
        self.true_button = QRadioButton(self.tr("True"), self)
        self.true_button.setChecked(True)
        self.false_button = QRadioButton(self.tr("False"), self)

        # Layouts
        radio_buttons_layout = QVBoxLayout()
        radio_buttons_layout.addWidget(self.true_button)
        radio_buttons_layout.addWidget(self.false_button)
        radio_buttons_layout.addStretch(1)

        layout = QFormLayout(self)
        layout.addRow(self.tr("Default"), radio_buttons_layout)

        # Signals
        self.true_button.toggled.connect(self.dataChanged)
        self.false_button.toggled.connect(self.dataChanged)

    def load(self, data):
        """Load the json object passed as parameter"""

        self.reset()

        default = data.get("default", True)
        if default:
            self.true_button.setChecked(True)
        else:
            self.false_button.setChecked(True)

    def dump(self):
        """Returns the json representation of this editor"""

        return {"default": self.true_button.isChecked()}

    def reset(self):
        """Reset editor to default values"""

        self.true_button.setChecked(True)


class StringSetupWidget(QWidget):
    """Editor to setup a string parameter"""

    dataChanged = pyqtSignal()
    editorChanged = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor

        :param parent QWidget: parent widget
        """

        super().__init__(parent)

        # Member variables
        self.single_button = QRadioButton(self.tr("Single"), self)
        self.single_button.setChecked(True)
        self.choices_button = QRadioButton(self.tr("Choices"), self)

        # Layouts
        radio_buttons_layout = QHBoxLayout()
        radio_buttons_layout.addWidget(self.single_button)
        radio_buttons_layout.addWidget(self.choices_button)
        radio_buttons_layout.addStretch(1)

        layout = QVBoxLayout(self)
        layout.addLayout(radio_buttons_layout)

        # single items
        self.single_default_lineedit = QLineEdit()

        # choices items
        self.choices_default_combobox = QComboBox()
        self.choices_listwidget = QListWidget()
        self.add_button = QPushButton(self.tr("+"))
        self.remove_button = QPushButton(self.tr("-"))

        # Widgets to be stacked
        self.single_conf_widget = QWidget()
        self.choices_conf_widget = QWidget()

        # Stacked widget
        self.stacked_widget = StackedWidget()
        self.stacked_widget.addWidget(self.single_conf_widget)
        self.stacked_widget.addWidget(self.choices_conf_widget)

        self.__setup_single_ui()
        self.__setup_choices_ui()

        layout.addWidget(self.stacked_widget)

        # Signals
        self.single_button.toggled.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.single_conf_widget)
        )
        self.choices_button.toggled.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.choices_conf_widget)
        )

        self.add_button.clicked.connect(self.__onChoiceAddClicked)
        self.remove_button.clicked.connect(self.__onChoiceRemoveClicked)

        self.single_button.toggled.connect(self.dataChanged)
        self.choices_button.toggled.connect(self.dataChanged)
        self.single_default_lineedit.textChanged.connect(self.dataChanged)
        self.choices_default_combobox.currentIndexChanged.connect(self.dataChanged)
        choices_model = self.choices_listwidget.model()
        choices_model.rowsInserted.connect(self.dataChanged)
        choices_model.rowsRemoved.connect(self.dataChanged)

        self.stacked_widget.currentChanged.connect(lambda: self.adjustSize())
        self.stacked_widget.currentChanged.connect(self.editorChanged)

    def load(self, data):
        """Load the json object passed as parameter"""

        self.reset()

        choices = data.get("choice", [])
        default = data.get("default", "")

        if "choice" in data:
            # Check there are no duplicates
            if len(choices) != len(set(choices)):
                raise RuntimeError("Invalid duplicate choice")
            else:
                if default not in choices:
                    raise RuntimeError("Invalid default choice")
                else:
                    self.choices_button.setChecked(True)
                    self.choices_listwidget.addItems(choices)
                    self.choices_default_combobox.addItems(choices)
                    index = self.choices_default_combobox.findText(
                        default, Qt.MatchFixedString
                    )
                    if index >= 0:
                        self.choices_default_combobox.setCurrentIndex(index)
                    else:
                        raise RuntimeError("Invalid default value")
        else:
            self.single_button.setChecked(True)
            self.single_default_lineedit.setText(default)

    def dump(self):
        """Returns the json representation of the editor"""

        data = {}

        if self.single_button.isChecked():
            data["default"] = self.single_default_lineedit.text()
        else:
            data["default"] = self.choices_default_combobox.currentText()
            data["choice"] = [
                str(self.choices_listwidget.item(i).text())
                for i in range(self.choices_listwidget.count())
            ]

        return data

    def reset(self):
        """Reset the editor to its default state"""

        self.single_button.setChecked(True)
        self.single_default_lineedit.clear()
        self.choices_listwidget.clear()
        self.choices_default_combobox.clear()

    def __setup_single_ui(self):

        layout = QFormLayout()
        layout.addRow(self.tr("Default:"), self.single_default_lineedit)
        self.single_conf_widget.setLayout(layout)

    def __setup_choices_ui(self):

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.remove_button)
        buttons_layout.addStretch(1)

        choices_layout = QVBoxLayout()
        choices_layout.addWidget(self.choices_listwidget)
        choices_layout.addLayout(buttons_layout)

        layout = QFormLayout()
        layout.addRow(self.tr("Default:"), self.choices_default_combobox)
        layout.addRow(self.tr("Choices:"), choices_layout)

        self.choices_conf_widget.setLayout(layout)

    @pyqtSlot()
    def __onChoiceAddClicked(self):
        input_value = None
        ok = False

        input_value, ok = QInputDialog.getText(
            self, self.tr("Input"), self.tr("New Choice:"), QLineEdit.Normal, ""
        )
        if ok:
            if (
                len(
                    self.choices_listwidget.findItems(str(input_value), Qt.MatchExactly)
                )
                == 0
            ):
                self.choices_listwidget.addItem(str(input_value))
                self.choices_default_combobox.addItem(str(input_value))

    @pyqtSlot()
    def __onChoiceRemoveClicked(self):
        choices = self.choices_listwidget.selectedItems()
        for choice in choices:
            self.choices_default_combobox.removeItem(
                self.choices_listwidget.row(choice)
            )
            self.choices_listwidget.takeItem(self.choices_listwidget.row(choice))


class NumericalSetupWidget(QWidget):
    """Editor to setup a numerical parameter"""

    dataChanged = pyqtSignal()
    editorChanged = pyqtSignal()

    def __init__(self, selected_type, parent=None):
        """Constructor

        :param selected_type InputType: input type to edit
        :param parent QWidget: parent widget
        """

        super().__init__(parent)

        # Class variables
        self.current_type = selected_type

        # Member variables
        self.single_button = QRadioButton(self.tr("Single"), self)
        self.single_button.setChecked(True)
        self.choices_button = QRadioButton(self.tr("Choices"), self)
        self.range_button = QRadioButton(self.tr("Range"), self)

        # Layouts
        radio_buttons_layout = QHBoxLayout()
        radio_buttons_layout.addWidget(self.single_button)
        radio_buttons_layout.addWidget(self.choices_button)
        radio_buttons_layout.addWidget(self.range_button)
        radio_buttons_layout.addStretch(1)

        layout = QVBoxLayout(self)
        layout.addLayout(radio_buttons_layout)

        min_value = self.current_type.numpy_info.min
        max_value = self.current_type.numpy_info.max

        # single items
        self.single_default_spinbox = NumpySpinBox(self.current_type.np_type)
        self.single_default_spinbox.setMinimum(min_value)
        self.single_default_spinbox.setMaximum(max_value)

        # choices items
        self.choices_default_combobox = QComboBox()
        self.choices_listwidget = QListWidget()
        self.add_button = QPushButton(self.tr("+"))
        self.remove_button = QPushButton(self.tr("-"))

        # range items
        self.range_minimum_spinbox = NumpySpinBox(self.current_type.np_type)
        self.range_maximum_spinbox = NumpySpinBox(self.current_type.np_type)
        self.range_default_spinbox = NumpySpinBox(self.current_type.np_type)

        # free bounds
        self.range_minimum_spinbox.setMinimum(min_value)
        self.range_maximum_spinbox.setMaximum(max_value)

        self.range_minimum_spinbox.setValue(-10)
        self.range_maximum_spinbox.setValue(10)

        # restricted bounds
        self.restrict_range()

        # Widgets to be stacked
        self.single_conf_widget = QWidget()
        self.choices_conf_widget = QWidget()
        self.range_conf_widget = QWidget()

        # Stacked widget
        self.stacked_widget = StackedWidget(self)
        self.stacked_widget.addWidget(self.single_conf_widget)
        self.stacked_widget.addWidget(self.choices_conf_widget)
        self.stacked_widget.addWidget(self.range_conf_widget)

        self.__setup_single_ui()
        self.__setup_choices_ui()
        self.__setup_range_ui()

        layout.addWidget(self.stacked_widget)

        # Signals
        self.single_button.toggled.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.single_conf_widget)
        )
        self.choices_button.toggled.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.choices_conf_widget)
        )
        self.range_button.toggled.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.range_conf_widget)
        )

        self.add_button.clicked.connect(self.__onChoiceAddClicked)
        self.remove_button.clicked.connect(self.__onChoiceRemoveClicked)

        self.range_minimum_spinbox.valueChanged.connect(self.restrict_range_from_min)
        self.range_maximum_spinbox.valueChanged.connect(self.restrict_range_from_max)

        self.single_button.toggled.connect(self.dataChanged)
        self.choices_button.toggled.connect(self.dataChanged)
        self.range_button.toggled.connect(self.dataChanged)
        self.single_default_spinbox.valueChanged.connect(self.dataChanged)
        self.choices_default_combobox.currentIndexChanged.connect(self.dataChanged)
        choices_model = self.choices_listwidget.model()
        choices_model.rowsInserted.connect(self.dataChanged)
        choices_model.rowsRemoved.connect(self.dataChanged)
        self.range_default_spinbox.valueChanged.connect(self.dataChanged)
        self.range_minimum_spinbox.valueChanged.connect(self.dataChanged)
        self.range_maximum_spinbox.valueChanged.connect(self.dataChanged)
        self.stacked_widget.currentChanged.connect(lambda: self.adjustSize())
        self.stacked_widget.currentChanged.connect(self.editorChanged)

    def load(self, data):
        """Load the json object passed as parameter"""

        self.reset(self.current_type)

        choices = data.get("choice", [])
        str_choices = [str(item) for item in choices]
        range_values = data.get("range", [-10, 10])
        minimum = range_values[0]
        maximum = range_values[1]
        default = data.get("default", 0)

        if "choice" in data:
            # Check there are no duplicates
            if len(str_choices) != len(set(str_choices)):
                raise RuntimeError("Invalid duplicate choice")
            else:
                if default not in choices:
                    raise RuntimeError("Invalid default choice")
                else:
                    self.choices_button.setChecked(True)
                    self.choices_listwidget.addItems(str_choices)
                    self.choices_default_combobox.addItems(str_choices)
                    index = self.choices_default_combobox.findText(
                        str(default), Qt.MatchFixedString
                    )
                    if index >= 0:
                        self.choices_default_combobox.setCurrentIndex(index)
                    else:
                        raise RuntimeError("Invalid default value")
        elif "range" in data:
            if len(range_values) != len(set(range_values)):
                raise RuntimeError("Invalid duplicate range")
            else:
                if minimum <= default <= maximum:
                    self.range_button.setChecked(True)
                    self.range_maximum_spinbox.setValue(maximum)
                    self.range_minimum_spinbox.setValue(minimum)
                    self.range_default_spinbox.setValue(default)
                else:
                    raise RuntimeError("Invalid default or min/max range")
        else:
            self.single_button.setChecked(True)
            self.single_default_spinbox.setValue(default)

    def dump(self):
        """Returns the json representation of this editor"""

        data = {}
        numpy_type = self.current_type.np_type

        if self.choices_button.isChecked():
            if len(self.choices_default_combobox.currentText()) == 0:
                data["default"] = 0
            else:
                try:
                    data["default"] = numpy_type(
                        self.choices_default_combobox.currentText()
                    )
                except OverflowError:
                    raise RuntimeError("Invalid default value: OverflowError")

            if self.choices_listwidget.count() == 0:
                data["choice"] = []
            else:
                data["choice"] = [
                    numpy_type(self.choices_listwidget.item(i).text())
                    for i in range(self.choices_listwidget.count())
                ]
        elif self.range_button.isChecked():
            data["default"] = self.range_default_spinbox.value
            data["range"] = [
                self.range_minimum_spinbox.value,
                self.range_maximum_spinbox.value,
            ]
        else:
            data["default"] = self.single_default_spinbox.value

        return data

    def reset(self, selected_type):
        """Reset editor to default values"""

        self.current_type = selected_type

        # reset single state
        self.single_button.setChecked(True)
        self.single_default_spinbox.setNumpyType(self.current_type.np_type)

        # reset choices state
        self.choices_listwidget.clear()
        self.choices_default_combobox.clear()

        # reset range state
        self.range_default_spinbox.setNumpyType(self.current_type.np_type)
        self.range_minimum_spinbox.setNumpyType(self.current_type.np_type)
        self.range_maximum_spinbox.setNumpyType(self.current_type.np_type)

        self.range_minimum_spinbox.setValue(-10)
        self.range_maximum_spinbox.setValue(10)

        # restricted bounds
        self.restrict_range()

    def restrict_set_bounds(self, min_value, max_value, default_value):
        """Ensure that the values entered are in the correct bounds as well as
        ensure that a range is really a range.
        """

        min_value = self.range_minimum_spinbox.value
        max_value = self.range_maximum_spinbox.value
        default_value = self.range_default_spinbox.value

        self.range_minimum_spinbox.setMaximum(max_value)
        self.range_maximum_spinbox.setMinimum(min_value)
        self.range_default_spinbox.setMinimum(min_value)
        self.range_default_spinbox.setMaximum(max_value)

        # update default value when out of bounds
        if default_value < min_value:
            self.range_default_spinbox.setValue(min_value)
        if default_value > max_value:
            self.range_default_spinbox.setValue(max_value)

    def restrict_range(self):
        min_value = self.range_minimum_spinbox.value
        max_value = self.range_maximum_spinbox.value
        default_value = self.range_default_spinbox.value

        self.restrict_set_bounds(min_value, max_value, default_value)

    def restrict_range_from_min(self):
        min_value = self.range_minimum_spinbox.value
        max_value = self.range_maximum_spinbox.value
        default_value = self.range_default_spinbox.value

        if min_value == max_value:
            self.range_maximum_spinbox.setMinimum(min_value)
            self.range_maximum_spinbox.setValue(min_value + 1)
            self.range_default_spinbox.setMaximum(min_value + 1)
        else:
            self.restrict_set_bounds(min_value, max_value, default_value)

    def restrict_range_from_max(self):
        min_value = self.range_minimum_spinbox.value
        max_value = self.range_maximum_spinbox.value
        default_value = self.range_default_spinbox.value

        if min_value == max_value:
            self.range_minimum_spinbox.setMaximum(max_value)
            self.range_minimum_spinbox.setValue(max_value - 1)
            self.range_default_spinbox.setMinimum(max_value - 1)
        else:
            self.restrict_set_bounds(min_value, max_value, default_value)

    def __setup_single_ui(self):

        layout = QFormLayout()
        layout.addRow(self.tr("Default:"), self.single_default_spinbox)
        self.single_conf_widget.setLayout(layout)

    def __setup_choices_ui(self):

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.remove_button)
        buttons_layout.addStretch(1)

        choices_layout = QVBoxLayout()
        choices_layout.addWidget(self.choices_listwidget)
        choices_layout.addLayout(buttons_layout)

        layout = QFormLayout()
        layout.addRow(self.tr("Default:"), self.choices_default_combobox)
        layout.addRow(self.tr("Choices:"), choices_layout)

        self.choices_conf_widget.setLayout(layout)

    def __setup_range_ui(self):

        layout = QFormLayout()
        layout.addRow(self.tr("Default:"), self.range_default_spinbox)
        layout.addRow(self.tr("Minimum:"), self.range_minimum_spinbox)
        layout.addRow(self.tr("Maximum:"), self.range_maximum_spinbox)

        self.range_conf_widget.setLayout(layout)

    @pyqtSlot()
    def __onChoiceAddClicked(self):

        input_value = None
        ok = False

        input_value, ok = NumericalChoiceDialog.getChoiceValue(self.current_type)

        if ok:
            if (
                len(
                    self.choices_listwidget.findItems(str(input_value), Qt.MatchExactly)
                )
                == 0
            ):
                self.choices_listwidget.addItem(str(input_value))
                self.choices_default_combobox.addItem(str(input_value))

    @pyqtSlot()
    def __onChoiceRemoveClicked(self):

        choices = self.choices_listwidget.selectedItems()
        for choice in choices:
            self.choices_default_combobox.removeItem(
                self.choices_listwidget.row(choice)
            )
            self.choices_listwidget.takeItem(self.choices_listwidget.row(choice))


class ParameterWidget(QWidget):
    """Widget representing a parameter"""

    dataChanged = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor

        :param parent QWidget: parent widget
        """

        super().__init__(parent)

        unwanted_basetypes = {"complex64", "complex128"}
        basetypes = [
            base_type
            for base_type in dataformat_basetypes()
            if base_type not in unwanted_basetypes
        ]

        # Member variables
        self.description_lineedit = QLineEdit()
        self.basetype_comboxbox = QComboBox()
        self.basetype_comboxbox.addItems(basetypes)
        self.selected_type = InputType[basetypes[0].upper()]
        self.setup_stackedwidget = StackedWidget()

        # Stacked widgets
        self.numerical_setup_widget = NumericalSetupWidget(self.selected_type)
        self.string_setup_widget = StringSetupWidget(self)
        self.bool_setup_widget = BoolSetupWidget(self)

        self.setup_stackedwidget.addWidget(self.numerical_setup_widget)
        self.setup_stackedwidget.addWidget(self.string_setup_widget)
        self.setup_stackedwidget.addWidget(self.bool_setup_widget)

        layout = QFormLayout(self)
        layout.addRow(self.tr("Description:"), self.description_lineedit)
        layout.addRow(self.tr("Type:"), self.basetype_comboxbox)
        layout.addRow(self.tr("Setup:"), self.setup_stackedwidget)

        # Signal/Slots connections
        self.description_lineedit.textChanged.connect(self.dataChanged)

        self.basetype_comboxbox.currentIndexChanged.connect(self.__onTypeWidgetChanged)
        self.setup_stackedwidget.currentChanged.connect(self.dataChanged)
        self.setup_stackedwidget.currentChanged.connect(lambda: self.adjustSize())

        self.numerical_setup_widget.dataChanged.connect(self.dataChanged)
        self.numerical_setup_widget.editorChanged.connect(lambda: self.adjustSize())

        self.string_setup_widget.dataChanged.connect(self.dataChanged)
        self.string_setup_widget.editorChanged.connect(lambda: self.adjustSize())

        self.bool_setup_widget.dataChanged.connect(self.dataChanged)

    @pyqtSlot()
    def __onTypeWidgetChanged(self):
        self.selected_type = InputType[self.basetype_comboxbox.currentText().upper()]

        selected_widget = None
        if self.selected_type == InputType.BOOL:
            self.bool_setup_widget.reset()
            selected_widget = self.bool_setup_widget
        elif self.selected_type == InputType.STRING:
            self.string_setup_widget.reset()
            selected_widget = self.string_setup_widget
        else:
            self.numerical_setup_widget.reset(self.selected_type)
            selected_widget = self.numerical_setup_widget

        self.setup_stackedwidget.setCurrentWidget(selected_widget)

    def dump(self):
        """Returns the json representation of this editor"""

        data = self.setup_stackedwidget.currentWidget().dump()
        description = self.description_lineedit.text()
        if description:
            data["description"] = description
        data["type"] = self.selected_type.name.lower()

        return data

    def load(self, data):
        """Load the json object passed as parameter"""

        data = data.copy()
        description = data.get("description", "")
        selected_type = data.get("type", None)
        default = data.get("default", None)

        if selected_type is None:
            raise RuntimeError("Invalid parameter with no type")
        if default is None:
            raise RuntimeError("Invalid parameter with no default")

        index = self.basetype_comboxbox.findText(selected_type, Qt.MatchFixedString)
        if index == -1:
            raise RuntimeError("Invalid parameter type value")

        self.basetype_comboxbox.setCurrentIndex(index)
        self.selected_type = InputType[selected_type.upper()]
        self.description_lineedit.setText(description)

        data.pop("type")
        data.pop("description", None)

        if self.selected_type == InputType.BOOL:
            self.bool_setup_widget.load(data)
        elif self.selected_type == InputType.STRING:
            self.string_setup_widget.load(data)
        else:
            self.numerical_setup_widget.load(data)
