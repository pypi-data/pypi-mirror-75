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

import click

from PyQt5.QtCore import QFileSystemWatcher
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from ..backend.asset import Asset
from ..backend.asset import AssetType
from ..backend.experimentmodel import ExperimentModel
from ..backend.resourcemodels import experiment_resources
from ..decorators import frozen
from .algorithmeditor import AlgorithmEditor
from .algorithmeditor import migrate_to_api_v2
from .algorithmeditor import update_code
from .databaseeditor import DatabaseEditor
from .dataformateditor import DataformatEditor
from .editor import PlaceholderEditor
from .experimenteditor import ExperimentEditor
from .libraryeditor import LibraryEditor
from .plottereditor import PlotterEditor
from .plotterparameterseditor import PlotterParametersEditor
from .protocoltemplateeditor import ProtocolTemplateEditor
from .toolchaineditor import ToolchainEditor


def widget_for_asset_type(asset_type):
    """Factory method to create the correct widget for the given asset_type.

    :param asset_type AssetType: type of asset

    :return: the editor matching the asset type
    """

    editor = None
    if asset_type == AssetType.UNKNOWN:
        editor = PlaceholderEditor()
    elif asset_type == AssetType.ALGORITHM:
        editor = AlgorithmEditor()
    elif asset_type == AssetType.DATABASE:
        editor = DatabaseEditor()
    elif asset_type == AssetType.DATAFORMAT:
        editor = DataformatEditor()
    elif asset_type == AssetType.EXPERIMENT:
        editor = ExperimentEditor()
    elif asset_type == AssetType.LIBRARY:
        editor = LibraryEditor()
    elif asset_type == AssetType.PLOTTER:
        editor = PlotterEditor()
    elif asset_type == AssetType.PLOTTERPARAMETER:
        editor = PlotterParametersEditor()
    elif asset_type == AssetType.PROTOCOLTEMPLATE:
        editor = ProtocolTemplateEditor()
    elif asset_type == AssetType.TOOLCHAIN:
        editor = ToolchainEditor()
    else:
        raise RuntimeError("Invalid asset type given {}".format(asset_type))
    return editor


class FileBlocker:
    """Context manager to suspend QFileSystemWatcher from watching a file"""

    def __init__(self, watcher, path):
        """Constructor

        :param watch QFileSystemWatcher: watcher to suspend
        :param path str: path to suspend watching from
        """
        self.watcher = watcher
        self.path = path

    def __enter__(self):
        """Stop watching file"""

        self.watcher.removePath(self.path)

    def __exit__(self, *args):
        """Start watching file again"""

        self.watcher.addPath(self.path)


@frozen
class AssetWidget(QWidget):
    """
    This widget will show the asset specific editor and the JSON view of it.

    The corresponding file will be watched and the the widget refreshed
    accordingly.
    """

    currentAssetChanged = pyqtSignal([Asset])

    def __init__(self, parent=None):
        """Constructor"""

        super().__init__(parent)

        self.experiment_model = ExperimentModel()
        self.context = None
        self.current_asset = None
        self.watcher = QFileSystemWatcher()
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.setInterval(200)

        self.json_widget = QTextEdit()
        self.json_widget.setReadOnly(True)

        self.editors = QStackedWidget()
        self.type_editor_map = {}

        for asset_type in AssetType:
            editor = widget_for_asset_type(asset_type)
            self.editors.addWidget(editor)
            self.type_editor_map[asset_type] = editor

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.editors, self.tr("Editor"))
        self.tab_widget.addTab(self.json_widget, self.tr("Raw JSON"))

        self.asset_name_label = QLabel(self.tr("Unknown"))
        layout = QVBoxLayout(self)
        layout.addWidget(self.asset_name_label)
        layout.addWidget(self.tab_widget)

        edit_menu = QMenu(self)
        self.edit_code_action = edit_menu.addAction(self.tr("Code"))
        self.edit_documentation_action = edit_menu.addAction(self.tr("Documentation"))

        edit_button = QPushButton(self.tr("Edit"))
        edit_button.setMenu(edit_menu)

        self.save_button = QPushButton(self.tr("Save"))
        self.save_button.setEnabled(False)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(self.save_button)

        layout.addLayout(button_layout)

        self.watcher.fileChanged.connect(self.__reloadFromHarddrive)
        self.update_timer.timeout.connect(self.__enableSave)
        self.update_timer.timeout.connect(self.__updateJsonWidget)
        self.save_button.clicked.connect(self.saveJson)
        self.edit_code_action.triggered.connect(self.__editCode)
        self.edit_documentation_action.triggered.connect(self.__editDocumentation)

        for action in self.create_actions():
            action.triggered.connect(self.__onCreateActionTriggered)

        experiment_editor = self.type_editor_map[AssetType.EXPERIMENT]
        experiment_editor.blockChanged.connect(self.__onBlockChanged)
        self.set_current_editor(AssetType.UNKNOWN)

    @property
    def current_editor(self):
        """Returns the current visible editor """

        return self.editors.currentWidget()

    def set_current_editor(self, asset_type):
        """Set the current editor"""

        self.editors.setCurrentWidget(self.type_editor_map[asset_type])
        self.edit_code_action.setEnabled(asset_type.has_code())
        self.edit_documentation_action.setEnabled(asset_type is not AssetType.UNKNOWN)

    @property
    def prefix_root_path(self):
        """Returns the prefix root path"""

        return self.context.meta["config"].path

    def __update_content(self, json_data):
        """Update the content of this widget"""

        try:
            self.current_editor.dataChanged.disconnect(self.update_timer)
        except TypeError:
            # Nothing was connected yet
            pass

        editor = self.type_editor_map[self.current_asset.type]
        editor.load_json(json_data)

        if self.current_asset.type == AssetType.EXPERIMENT:
            editor.loadToolchainData("/".join(self.current_asset.name.split("/")[1:4]))

        editor.dataChanged.connect(self.update_timer.start)
        self.set_current_editor(self.current_asset.type)
        self.__updateJsonWidget()

        self.asset_name_label.setText(self.current_asset.name)
        self.save_button.setEnabled(False)

    def __update_editors_icon(self, is_valid, errors=None):
        tab_index = self.tab_widget.indexOf(self.editors)
        tab_icon = (
            self.style().standardIcon(QStyle.SP_MessageBoxCritical)
            if not is_valid
            else QIcon()
        )
        tab_tooltip = ""
        if errors is not None:
            tab_tooltip = "\n".join(errors)

        self.tab_widget.setTabIcon(tab_index, tab_icon)
        self.tab_widget.setTabToolTip(tab_index, tab_tooltip)

    def __clear_watcher(self):
        """Clears the content of the file system watcher"""

        files = self.watcher.files()
        if files:
            self.watcher.removePaths(files)

    @pyqtSlot()
    def __enableSave(self):
        """Enable the save button"""

        self.save_button.setEnabled(True)

    @pyqtSlot()
    def __reloadFromHarddrive(self):
        """Reload the content of this widget from the hard drive"""

        answer = QMessageBox.question(
            self,
            self.tr("File changed"),
            self.tr(
                "The file:\n{}\nhas changed on disk.\n"
                "Do you want to reload it ?".format(self.current_asset.declaration_path)
            ),
        )

        if answer == QMessageBox.Yes:
            self.__update_content(self.current_asset.declaration)

    @pyqtSlot()
    def __onCreateActionTriggered(self):
        action = self.sender()

        editor = [
            editor
            for editor in self.type_editor_map.values()
            if editor.create_action == action
        ][0]

        self.maybe_save()

        asset, json_data = editor.createNewAsset()

        if asset and json_data:
            self.__clear_watcher()
            self.current_asset = asset
            self.__update_content(json_data)
            self.current_editor.setDirty()
            self.save_button.setEnabled(True)
            self.__update_editors_icon(False)
            self.watcher.addPath(asset.declaration_path)
            if asset.type == AssetType.EXPERIMENT:
                self.experiment_model.load_experiment(asset)
            self.currentAssetChanged.emit(asset)
        elif asset:
            self.loadAsset(asset)

    @pyqtSlot(str, dict)
    def __onBlockChanged(self, block_name, configuration):
        self.experiment_model.update_block(block_name, configuration)
        errors_map = self.experiment_model.check_all_blocks()
        experiment_editor = self.type_editor_map[AssetType.EXPERIMENT]
        experiment_editor.setBlockErrors(errors_map)

    @pyqtSlot()
    def __updateJsonWidget(self):
        self.json_widget.setText(self.current_editor.dump_as_string())

    @pyqtSlot()
    def __editDocumentation(self):
        path = self.current_asset.documentation_path
        if not os.path.exists(path):
            answer = QMessageBox.question(
                self,
                self.tr("File not found"),
                self.tr(
                    "The documentation file does not exist.\n Would you like to create one ?"
                ),
            )
            if answer == QMessageBox.No:
                return
            with open(path, "wt") as doc_file:
                doc_file.write(self.tr("Empty"))
        click.launch(url=path)

    @pyqtSlot()
    def __editCode(self):
        if not self.current_asset.type.has_code():
            return
        path = self.current_asset.code_path
        click.launch(url=path)

    def closeEvent(self, event):
        """Re-impl will check and ask to save if the editor is dirty"""

        self.maybe_save()
        super().closeEvent(event)

    def maybe_save(self):
        """If the editor has been modified ask for saving"""

        if self.current_editor.isDirty():
            answer = QMessageBox.question(
                self,
                self.tr("Content changed"),
                self.tr(f"Do you wish to save:\n\n{self.current_asset.name}\n\n?"),
            )

            if answer == QMessageBox.Yes:
                self.saveJson()
            else:
                self.current_editor.clearDirty()

        self.save_button.setEnabled(False)

    def set_context(self, context):
        """Sets the BEAT context"""

        self.context = context

        experiment_resources.setContext(self.context)

        for i in range(0, self.editors.count()):
            self.editors.widget(i).set_context(context)

    def create_actions(self):
        """Return the creation actions of all editors"""

        action_list = [editor.create_action for editor in self.type_editor_map.values()]
        return filter(None, action_list)

    @pyqtSlot("QString")
    def deleteAsset(self, file_path):
        """Delete the requested asset

        :param file_path str: path to the json file of the asset to delete
        """

        if self.current_asset and self.current_asset.declaration_path == file_path:
            # Check before deletion
            answer = QMessageBox.question(
                self,
                self.tr("Deletion requested"),
                self.tr(
                    f"You are about to delete the asset you are currently editing:\n\n{self.current_asset.name}\n\nAre you sure you want to do that ?"
                ),
            )
            if answer == QMessageBox.No:
                return
            self.set_current_editor(AssetType.UNKNOWN)
            self.asset_name_label.setText(self.tr("Unknown"))
            self.json_widget.clear()
            self.__clear_watcher()
            self.current_asset.delete()
            self.current_asset = None
        else:
            # Check before deletion
            asset = Asset.from_path(self.prefix_root_path, file_path)
            asset_type = asset.type.name.lower()
            answer = QMessageBox.question(
                self,
                self.tr("Deletion requested"),
                self.tr(
                    f"You are about to delete an asset of type {asset_type} named:\n\n{asset.name}\n\nAre you sure you want to do that ?"
                ),
            )
            if answer == QMessageBox.No:
                return
            asset.delete()

    def confirm_loading(self, errors):
        """Request loading confirmation"""

        message_box = QMessageBox(
            QMessageBox.Critical,
            self.tr("Invalid asset"),
            self.tr("The asset you are trying to load is invalid."),
        )
        message_box.setDetailedText(f"{errors}")
        message_box.addButton(QMessageBox.Cancel)
        load_button = message_box.addButton(QMessageBox.Ignore)
        load_button.setText(self.tr("Load anyway"))

        return message_box.exec_()

    @pyqtSlot(Asset)
    def loadAsset(self, asset):
        """ Load the content of the file given in parameter

        :param asset Asset: asset to edit
        """

        if self.current_asset == asset and not self.current_editor.isDirty():
            return

        self.maybe_save()

        self.__clear_watcher()

        is_valid, errors = asset.is_valid()
        do_load = False

        if not is_valid:
            result = self.confirm_loading(errors)
            do_load = result == QMessageBox.Ignore
        else:
            do_load = True

        if do_load:
            self.__update_editors_icon(is_valid, errors)

            declaration = asset.declaration

            # Check if asset description size is bigger to what is allowed by the current editor
            if (
                len(declaration.get("description", ""))
                > self.current_editor.description_max_length
            ):
                QMessageBox.warning(
                    self,
                    self.tr("Description size"),
                    self.tr(
                        "The loaded description is too big and will be truncated. Please update your description."
                    ),
                )

            if asset.type == AssetType.ALGORITHM:
                if declaration.get("api_version", 0) < 2:
                    answer = QMessageBox.question(
                        self,
                        self.tr("Outdated content"),
                        self.tr(
                            "This algorithm implements an obsolete API\nWould you like to create a new updated version of it ?"
                        ),
                    )

                    if answer == QMessageBox.No:
                        return

                    status, asset = migrate_to_api_v2(asset)
                    if status:
                        update_code(asset)
                    else:
                        QMessageBox.information(
                            self,
                            self.tr("Error occured"),
                            self.tr("Failed to create new version"),
                        )
                        return
            elif asset.type == AssetType.EXPERIMENT:
                self.experiment_model.load_experiment(asset)

            self.watcher.addPath(asset.declaration_path)
            self.current_asset = asset
            self.__update_content(declaration)
            self.currentAssetChanged.emit(asset)

    @pyqtSlot()
    def saveJson(self):
        """Save the editor content back to the file"""

        json_data = self.current_editor.dump_json()

        declaration_path = self.current_asset.declaration_path
        with FileBlocker(self.watcher, declaration_path):
            self.current_asset.declaration = json_data

        is_valid, errors = self.current_asset.is_valid()
        self.__update_editors_icon(is_valid, errors)

        if self.current_asset.type == AssetType.ALGORITHM:
            update_code(self.current_asset)

        self.current_editor.clearDirty()
        self.save_button.setEnabled(False)
