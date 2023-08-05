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

from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from ..backend.asset import AssetType
from ..backend.assetmodel import DataFormatModel
from ..backend.delegates import AssetItemDelegate
from ..decorators import frozen
from .dialogs import NameInputDialog
from .editor import AbstractAssetEditor
from .scrollwidget import ScrollWidget


class SetWidget(QWidget):
    """Editor for a set"""

    dataChanged = pyqtSignal()
    deletionRequested = pyqtSignal()

    def __init__(self, dataformat_model, parent=None):
        super().__init__(parent)

        self.dataformat_model = dataformat_model
        delegate = AssetItemDelegate(self.dataformat_model)

        self.delete_button = QPushButton(self.tr("-"))
        self.delete_button.setFixedSize(30, 30)

        delete_layout = QHBoxLayout()
        delete_layout.addStretch(1)
        delete_layout.addWidget(self.delete_button)

        self.name_lineedit = QLineEdit()
        self.outputs_tablewidget = QTableWidget()
        self.outputs_tablewidget.verticalHeader().setVisible(False)
        self.outputs_tablewidget.setColumnCount(2)
        self.outputs_tablewidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.outputs_tablewidget.setHorizontalHeaderLabels(
            [self.tr("Name"), self.tr("Type")]
        )
        self.outputs_tablewidget.setItemDelegateForColumn(1, delegate)
        self.outputs_tablewidget.setMinimumHeight(200)

        self.add_button = QPushButton(self.tr("+"))
        self.add_button.setFixedSize(30, 30)
        self.remove_button = QPushButton(self.tr("-"))
        self.remove_button.setFixedSize(30, 30)
        self.remove_button.setEnabled(False)
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)

        outputs_layout = QVBoxLayout()
        outputs_layout.addWidget(self.outputs_tablewidget, 2)
        outputs_layout.addLayout(button_layout)

        self.form_layout = QFormLayout()
        self.form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.form_layout.addRow(self.tr("Name"), self.name_lineedit)
        self.form_layout.addRow(self.tr("Outputs"), outputs_layout)

        layout = QVBoxLayout(self)
        layout.addLayout(delete_layout)
        layout.addLayout(self.form_layout)

        self.name_lineedit.textChanged.connect(self.dataChanged)
        self.delete_button.clicked.connect(self.deletionRequested)
        self.add_button.clicked.connect(self.__addOutput)
        self.remove_button.clicked.connect(self.__removeOutputs)
        self.outputs_tablewidget.cellChanged.connect(self.dataChanged)
        self.outputs_tablewidget.itemSelectionChanged.connect(
            self.__onItemSelectionChanged
        )

    @pyqtSlot()
    def __addOutput(self):
        """Add a new output"""

        new_row = self.outputs_tablewidget.rowCount()
        self.outputs_tablewidget.setRowCount(new_row + 1)
        name_item = QTableWidgetItem(self.tr("Change_me"))
        type_item = QTableWidgetItem(self.dataformat_model.index(0).data())
        self.outputs_tablewidget.setItem(new_row, 0, name_item)
        self.outputs_tablewidget.setItem(new_row, 1, type_item)
        self.outputs_tablewidget.scrollToItem(type_item)
        self.dataChanged.emit()

    @pyqtSlot()
    def __removeOutputs(self):
        """Remove the selected output(s)"""

        selected_items = self.outputs_tablewidget.selectedItems()

        rows = []
        while selected_items:
            item = selected_items.pop()
            rows.append(item.row())

        rows = set(sorted(rows))

        while rows:
            row = rows.pop()
            self.outputs_tablewidget.removeRow(row)
        self.dataChanged.emit()

    @pyqtSlot()
    def __onItemSelectionChanged(self):
        self.remove_button.setEnabled(bool(self.outputs_tablewidget.selectedItems()))

    def name(self):
        """Name of the set"""

        return self.name_lineedit.text()

    def load(self, json_data):
        """Load this widget with the content of json_data"""

        self.name_lineedit.setText(json_data.get("name"))
        outputs = json_data.get("outputs", {})
        self.outputs_tablewidget.setRowCount(len(outputs))
        row = 0
        for name, type_ in outputs.items():
            name_item = QTableWidgetItem(name)
            type_item = QTableWidgetItem(type_)
            self.outputs_tablewidget.setItem(row, 0, name_item)
            self.outputs_tablewidget.setItem(row, 1, type_item)
            row += 1

    def dump(self):
        """Returns the json representation of this set"""

        json_data = {"name": self.name_lineedit.text()}
        outputs = {}
        for i in range(self.outputs_tablewidget.rowCount()):
            outputs[
                self.outputs_tablewidget.item(i, 0).text()
            ] = self.outputs_tablewidget.item(i, 1).text()

        json_data["outputs"] = outputs
        return json_data


@frozen
class ProtocolTemplateEditor(AbstractAssetEditor):
    """Editor for protocol template objects"""

    def __init__(self, parent=None):
        super().__init__(AssetType.PROTOCOLTEMPLATE, parent)
        self.setObjectName(self.__class__.__name__)
        self.set_title(self.tr("Protocol Template"))

        self.dataformat_model = DataFormatModel()
        self.dataformat_model.full_list_enabled = True

        self.scroll_widget = ScrollWidget()

        self.add_set_button = QPushButton(self.tr("+"))
        self.add_set_button.setFixedSize(30, 30)

        self.layout().addWidget(self.scroll_widget, 1)
        self.layout().addWidget(self.add_set_button, 1)

        self.scroll_widget.dataChanged.connect(self.dataChanged)
        self.add_set_button.clicked.connect(self.__addSet)
        self.contextChanged.connect(
            lambda: self.dataformat_model.setPrefixPath(self.prefix_path)
        )

    @property
    def set_widgets(self):
        return self.scroll_widget.widget_list

    @pyqtSlot()
    def __onRemoveRequested(self):
        """Remove the widget clicked"""

        self.__remove_widget(self.sender())

    def __remove_widget(self, widget):
        """Removes the widget that which signal triggered this slot"""

        self.scroll_widget.removeWidget(widget)

    @pyqtSlot()
    def __addSet(self):
        """Add a new set"""

        set_names = [widget.name() for widget in self.set_widgets]

        while True:
            name, ok_pressed = NameInputDialog.getText(self, self.tr("Set name"))
            if not ok_pressed:
                break

            if ok_pressed and name not in set_names:
                self.__load_json(
                    {
                        "sets": [
                            {
                                "name": name,
                                "outputs": {
                                    "Change_me": self.dataformat_model.index(0).data()
                                },
                            }
                        ]
                    }
                )
                self.dataChanged.emit()
                break

    @pyqtSlot()
    def __showLatestSet(self):
        """Ensure that the latest set is visible"""

        if self.set_widgets:
            self.scroll_widget.ensureWidgetVisible(self.set_widgets[-1], 10, 10)

    def __load_json(self, json_object):
        """Load the json object passed as parameter"""

        for set_ in json_object.get("sets", []):
            set_widget = SetWidget(self.dataformat_model)
            set_widget.load(set_)
            self.scroll_widget.addWidget(set_widget)
            set_widget.deletionRequested.connect(self.__onRemoveRequested)

        if self.set_widgets:
            QTimer.singleShot(100, self.__showLatestSet)

    def _asset_models(self):
        """Returns a list of all asset models used"""

        return [self.dataformat_model]

    def _load_json(self, json_object):
        """Load the json object passed as parameter"""

        self.blockSignals(True)

        while self.set_widgets:
            widget = self.set_widgets[0]
            self.__remove_widget(widget)

        self.blockSignals(False)

        self.__load_json(json_object)

    def _dump_json(self):
        """Returns the json representation of the asset"""

        return {
            "schema_version": 1,
            "sets": [widget.dump() for widget in self.set_widgets],
        }
