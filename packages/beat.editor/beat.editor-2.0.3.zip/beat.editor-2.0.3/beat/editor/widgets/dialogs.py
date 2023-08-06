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

import os

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QButtonGroup
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QVBoxLayout

from ..backend.asset import AssetType
from ..backend.assetmodel import AssetModel
from ..utils import dataformat_basetypes
from .validatedhelpers import NameLineEdit


class CreationType:
    (NEW, NEW_VERSION, FORK) = range(3)

    def __init__(self, **kwds):
        super().__init__(**kwds)

    @staticmethod
    def typeToString(type_):
        text = QCoreApplication.translate("CreationType", "Unknown")
        if type_ == CreationType.NEW:
            text = QCoreApplication.translate("CreationType", "New")
        elif type_ == CreationType.NEW_VERSION:
            text = QCoreApplication.translate("CreationType", "New version")
        elif type_ == CreationType.FORK:
            text = QCoreApplication.translate("CreationType", "Fork")

        return text


class AssetCreationDialog(QDialog, CreationType):
    def __init__(self, context, asset_type, parent=None):
        super().__init__(parent)

        self.asset_type = asset_type

        config = context.meta["config"]
        user = config.user
        prefix_path = config.path

        asset_model = AssetModel()
        asset_model.asset_type = asset_type
        asset_model.prefix_path = prefix_path

        self.fork_asset_list = asset_model.stringList()
        self.new_version_asset_list = asset_model.stringList()

        if asset_type == AssetType.DATAFORMAT:
            basetypes = dataformat_basetypes()
            self.fork_asset_list = [
                asset for asset in self.fork_asset_list if asset not in basetypes
            ]
            self.new_version_asset_list = [
                asset for asset in self.fork_asset_list if user in asset
            ]

        # New asset
        self.name_lineedit = NameLineEdit()
        self.new_radio_button = QRadioButton(self.tr("New"))
        self.new_radio_button.setChecked(True)
        self.toolchain_combobox = None
        if asset_type == AssetType.EXPERIMENT:
            self.toolchain_combobox = QComboBox()
            toolchain_model = AssetModel()
            toolchain_model.asset_type = AssetType.TOOLCHAIN
            toolchain_model.prefix_path = prefix_path
            self.toolchain_combobox.setModel(toolchain_model)

        # New version
        self.new_version_combobox = QComboBox()
        self.new_version_combobox.addItems(self.new_version_asset_list)
        self.new_version_combobox.setEnabled(False)
        self.new_version_radio_button = QRadioButton(self.tr("New version"))

        # Fork part
        self.fork_combobox = QComboBox()
        self.fork_combobox.addItems(self.fork_asset_list)
        self.fork_combobox.setEnabled(False)
        self.fork_lineedit = NameLineEdit()
        self.fork_lineedit.setEnabled(False)
        self.fork_radio_button = QRadioButton(self.tr("Fork"))

        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonbox.button(QDialogButtonBox.Ok).setEnabled(False)

        button_group = QButtonGroup(self)
        button_group.addButton(self.new_radio_button)
        button_group.addButton(self.new_version_radio_button)
        button_group.addButton(self.fork_radio_button)

        # Layouts
        fork_layout = QVBoxLayout()
        fork_layout.addWidget(self.fork_combobox)
        fork_layout.addWidget(self.fork_lineedit)

        form_layout = QFormLayout(self)
        form_layout.addRow(self.new_radio_button, self.name_lineedit)
        if asset_type == AssetType.EXPERIMENT:
            form_layout.addRow(self.tr("Toolchain"), self.toolchain_combobox)

        if asset_type.has_versions():
            form_layout.addRow(self.new_version_radio_button, self.new_version_combobox)

        if asset_type.can_fork():
            form_layout.addRow(self.fork_radio_button, fork_layout)

        form_layout.addRow(self.buttonbox)

        self.name_lineedit.textChanged.connect(self.__validateName)
        self.new_radio_button.toggled.connect(self.name_lineedit.setEnabled)
        if asset_type == AssetType.EXPERIMENT:
            self.new_radio_button.toggled.connect(self.toolchain_combobox.setEnabled)
            self.toolchain_combobox.currentIndexChanged.connect(self.__updateUi)
        self.new_radio_button.toggled.connect(self.__updateUi)

        self.fork_lineedit.textChanged.connect(self.__validateName)
        self.fork_radio_button.toggled.connect(self.fork_combobox.setEnabled)
        self.fork_radio_button.toggled.connect(self.fork_lineedit.setEnabled)
        self.fork_radio_button.toggled.connect(self.__updateUi)
        self.new_version_radio_button.toggled.connect(
            self.new_version_combobox.setEnabled
        )

        self.new_version_radio_button.toggled.connect(self.__updateUi)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)

    @pyqtSlot()
    def __updateUi(self):
        if self.isNew():
            self.__validateName(self.name_lineedit.text())
        elif self.isFork():
            self.__validateName(self.fork_lineedit.text())
        else:
            self.buttonbox.button(QDialogButtonBox.Ok).setEnabled(True)

    @pyqtSlot(str)
    def __validateName(self, name):
        """Validate that new name is not already used"""

        ok_button = self.buttonbox.button(QDialogButtonBox.Ok)
        if name:
            if self.asset_type == AssetType.EXPERIMENT:
                name = os.path.join(self.toolchain_combobox.currentText(), name)
                used_names = [
                    asset[asset.find("/") + 1 :] for asset in self.fork_asset_list
                ]
            else:
                used_names = [asset.split("/")[-2] for asset in self.fork_asset_list]

            ok_button.setEnabled(name not in used_names)
        else:
            ok_button.setEnabled(False)

    def isNew(self):
        return self.new_radio_button.isChecked()

    def isNewVersion(self):
        return self.new_version_radio_button.isChecked()

    def isFork(self):
        return self.fork_radio_button.isChecked()

    def assetInfo(self):
        if self.isNew():
            if self.asset_type == AssetType.EXPERIMENT:
                return (
                    self.toolchain_combobox.currentText(),
                    self.name_lineedit.text(),
                )
            return self.name_lineedit.text()
        elif self.isNewVersion():
            return self.new_version_combobox.currentText()
        else:
            return (self.fork_combobox.currentText(), self.fork_lineedit.text())

    def open(self, slot):
        self.accepted.connect(slot)
        super().open()

    def creationType(self):
        """Returns the type of creation done"""

        if self.isNew():
            return self.NEW
        elif self.isNewVersion():
            return self.NEW_VERSION
        else:
            return self.FORK

    @staticmethod
    def getAssetInfo(parent, context, asset_type):
        dialog = AssetCreationDialog(context, asset_type, parent)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            return True, dialog.creationType(), dialog.assetInfo()
        else:
            return False, None, None


class NameInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.name_lineedit = NameLineEdit()
        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        layout = QFormLayout(self)
        layout.addRow(self.tr("Name"), self.name_lineedit)
        layout.addWidget(self.buttonbox)

        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)

    def name(self):
        return self.name_lineedit.text()

    @staticmethod
    def getText(parent, title=""):
        dialog = NameInputDialog(parent)
        dialog.setWindowTitle(title)

        result = dialog.exec_()

        if result == QDialog.Accepted:
            return dialog.name(), True
        else:
            return None, False
