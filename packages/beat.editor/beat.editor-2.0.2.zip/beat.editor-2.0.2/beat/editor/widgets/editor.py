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

import pkg_resources
import simplejson as json

from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from beat.backend.python import utils

from ..backend.asset import Asset
from ..backend.asset import AssetType
from .dialogs import AssetCreationDialog


class AbstractAssetEditor(QWidget):
    """Base class for BEAT asset editors"""

    dataChanged = pyqtSignal()
    contextChanged = pyqtSignal()

    def __init__(self, asset_type, parent=None):
        """Constructor

        :param str title: Title of the editor
        :param parent QWidget: parent of this widget
        """

        if not isinstance(asset_type, AssetType):
            raise RuntimeError("Invalid parameter")

        super().__init__(parent)

        self.context = None
        self.asset_type = asset_type
        self.schema_version = None
        common_data = pkg_resources.resource_string("beat.core", "schema/common/1.json")
        common_data = json.loads(common_data)
        definitions = common_data["definitions"]
        description = definitions["description"]
        description_max_length = description["maxLength"]

        self.clearDirty()

        self.create_action = QAction("{}".format(asset_type.name.title()))

        self.title_label = QLabel(self.tr("Unknown"))
        self.description_lineedit = QLineEdit()
        self.description_lineedit.setMaxLength(description_max_length)

        self.information_group_box = QGroupBox(self.tr("Information"))
        self.information_layout = QFormLayout(self.information_group_box)
        self.information_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.information_layout.addRow(
            self.tr("Short description"), self.description_lineedit
        )

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addWidget(self.information_group_box)

        # self.create_action.triggered.connect(self._onCreateActionTriggered)
        self.description_lineedit.textChanged.connect(self.dataChanged)
        self.dataChanged.connect(self.setDirty)

    @property
    def description_max_length(self):
        return self.description_lineedit.maxLength()

    @pyqtSlot()
    def refresh(self):
        """Reload the editor models"""

        for model in self._asset_models():
            model.reload()

    def _asset_models(self):
        """Returns a list of all asset models used"""

        return []

    def _add_information_widget(self, label, widget):
        """Add field to information widget

        :param label str: text for the field
        :param widget QWidget: field
        """

        self.information_layout.addRow(label, widget)

    def _set_information_widget_visible(self, widget, visible):
        """Set the row showing the widget visible

        :param widget QWidget: field to who hide
        :param visible bool: whether to show or hide
        """

        widget.setVisible(visible)
        self.information_layout.labelForField(widget).setVisible(visible)

    def createNewAsset(self):
        ok_pressed, creation_type, asset_info = AssetCreationDialog.getAssetInfo(
            self, self.context, self.asset_type
        )

        if ok_pressed:
            return self._createNewAsset(creation_type, asset_info)
        return None, None

    @pyqtSlot()
    def _onCreateActionTriggered(self):
        ok_pressed, creation_type, asset_info = AssetCreationDialog.getAssetInfo(
            self, self.context, self.asset_type
        )

        if ok_pressed:
            self._createNewAsset(creation_type, asset_info)

    def _createNewAsset(self, creation_type, asset_info):
        """Implement whatever is needed to create a new asset managed by this editor"""

        user = self.context.meta["config"].user
        error_message = None
        status = False

        if creation_type == AssetCreationDialog.NEW:
            if self.asset_type.split_count() == 1:
                asset_name = f"{asset_info}/1"
            else:
                asset_name = f"{user}/{asset_info}/1"
            try:
                status = self.asset_type.create_new(self.prefix_path, asset_name)
            except RuntimeError as error:
                error_message = str(error)
            else:
                asset = Asset(self.prefix_path, self.asset_type, asset_name)

        elif creation_type == AssetCreationDialog.NEW_VERSION:
            status = self.asset_type.create_new_version(self.prefix_path, asset_info)
            version_location = asset_info.rfind("/") + 1
            asset_new_version = int(asset_info[version_location:]) + 1
            asset_name = asset_info[:version_location] + str(asset_new_version)
            asset = Asset(self.prefix_path, self.asset_type, asset_name)
        else:
            source_asset, target_name = asset_info
            if self.asset_type.split_count() == 1:
                name, version = source_asset.split("/")
                target_asset = f"{target_name}/{version}"
            elif self.asset_type.split_count() == 2:
                name, version = source_asset.split("/")[-2:]
                target_asset = f"{user}/{target_name}/{version}"
            else:
                items = source_asset.split("/")
                items[0] = user
                items[4] = target_name
                target_asset = "/".join(items)
            status = self.asset_type.fork(self.prefix_path, source_asset, target_asset)
            asset = Asset(self.prefix_path, self.asset_type, target_asset)

        if not status:
            error_text = self.tr(
                "The {} operation failed".format(
                    AssetCreationDialog.typeToString(creation_type)
                )
            )

            if error_message:
                error_text += self.tr("\nReason:{}".format(error_message))

            QMessageBox.critical(self, self.tr("Error occurred"), error_text)
            return None, None

        return asset, None

    def _load_json(self, json_object):
        """To be implemented by subclass to load their specific JSON parts"""

        raise NotImplementedError

    def _dump_json(self, json_object):
        """To be implemented by subclass to dump their specific JSON parts"""

        raise NotImplementedError

    def is_valid(self):
        _, errors = self.asset_type.validate(self.dump_json())

        return errors == [], errors

    @pyqtSlot()
    def setDirty(self):
        """Flag the editor as dirty"""

        self._dirty = True

    @pyqtSlot()
    def clearDirty(self):
        """Clear the dirty flag"""

        self._dirty = False

    def isDirty(self):
        """Returns whether there has been changes in this editor"""

        return self._dirty

    def create_action(self):
        """Returns the action to use to create a new asset"""

        raise NotImplementedError

    def set_title(self, title):
        """Set the title of the widget

        :param title str: Title of the widget
        """

        self.title_label.setText(title)

    def prefixPath(self):
        if self.context:
            return self.context.meta["config"].path
        return None

    prefix_path = pyqtProperty(str, fget=prefixPath)

    def set_context(self, context):
        """Sets the BEAT context"""

        if self.context == context:
            return

        self.context = context
        self.contextChanged.emit()

    def load_json(self, json_object):
        """Load the json object passed as parameter"""

        self.schema_version = json_object.get("schema_version")

        self.blockSignals(True)
        self.refresh()
        self.description_lineedit.setText(json_object.get("description"))
        self._load_json(json_object)
        self.blockSignals(False)
        self.clearDirty()

    def dump_json(self):
        """Returns the json representation of the asset"""

        json_data = {}

        if self.schema_version:
            json_data["schema_version"] = self.schema_version

        description = self.description_lineedit.text()
        if description:
            json_data["description"] = description

        json_data.update(self._dump_json())
        return json_data

    def dump_as_string(self):
        """Returns the string representation of this editor json"""

        return json.dumps(
            self.dump_json(), sort_keys=True, indent=4, cls=utils.NumpyJSONEncoder
        )


class PlaceholderEditor(AbstractAssetEditor):
    """Placeholder widget providing the API of an editor"""

    def __init__(self, parent=None):
        """Constructor

        :param parent QWidget: parent of this widget
        """

        super().__init__(AssetType.UNKNOWN, parent)
        self.set_title(self.tr("Nothing to edit"))
        self.information_group_box.hide()
        self.create_action = None

    def _load_json(self, json_object):
        """Re-imp. Does nothing"""

        pass

    def _dump_json(self):
        """Re-imp. Does nothing"""

        return {}
