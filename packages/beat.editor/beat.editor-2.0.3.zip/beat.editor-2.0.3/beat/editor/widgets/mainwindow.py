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

from PyQt5.QtCore import QSettings
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import qApp

from .assetbrowser import AssetBrowser
from .assetwidget import AssetWidget


class MainWindow(QMainWindow):
    """
    Main window of the beat.editor application
    """

    def __init__(self, parent=None):
        """Constructor"""

        super().__init__(parent)

        menubar = self.menuBar()

        fileMenu = menubar.addMenu(self.tr("File"))
        newMenu = fileMenu.addMenu(self.tr("New..."))
        quitAction = fileMenu.addAction(self.tr("Quit"))
        quitAction.setShortcut("CTRL+Q")

        preferencesMenu = menubar.addMenu(self.tr("Preferences"))
        settingsAction = preferencesMenu.addAction(self.tr("Settings"))

        helpMenu = menubar.addMenu(self.tr("Help"))
        aboutAction = helpMenu.addAction(self.tr("About"))
        aboutQtAction = helpMenu.addAction(self.tr("About Qt"))

        self.assetBrowser = AssetBrowser()
        self.assetWidget = AssetWidget()
        for action in self.assetWidget.create_actions():
            newMenu.addAction(action)

        centralWidget = QSplitter()
        centralWidget.addWidget(self.assetBrowser)
        centralWidget.addWidget(self.assetWidget)
        self.setCentralWidget(centralWidget)

        self.assetBrowser.assetSelected.connect(self.assetWidget.loadAsset)
        self.assetBrowser.deletionRequested.connect(self.assetWidget.deleteAsset)
        self.assetWidget.currentAssetChanged.connect(self.assetBrowser.setCurrentAsset)
        quitAction.triggered.connect(qApp.quit)
        aboutAction.triggered.connect(self.showAbout)
        aboutQtAction.triggered.connect(self.showAboutQt)
        settingsAction.triggered.connect(self.showSettings)

        self.load_settings()

    def set_context(self, context):
        """Sets the BEAT context to use"""

        self.assetBrowser.set_context(context)
        self.assetWidget.set_context(context)

    @pyqtSlot()
    def showAbout(self):
        """About box for the application"""

        QMessageBox.about(
            self,
            self.tr("About"),
            self.tr(
                f"{qApp.applicationName()}<br>"
                f"Version: {qApp.applicationVersion()}<br>"
                "Copyright Idiap Research Institute<br>"
                f"List of <a target='_blank' href='https://gitlab.idiap.ch/beat/beat.editor/blob/{qApp.applicationVersion()}/doc/known_issues.rst'>known issues</a><br>"
                "<a target='_blank' href='https://icons8.com/icons/set/docker'>Docker</a> icon by <a target='_blank' href='https://icons8.com'>Icons8</a><br>"
                "<a target='_blank' href='https://icons8.com/icons/set/cloud-development'>Cloud Development</a> icon by <a target='_blank' href='https://icons8.com'>Icons8</a>"
            ),
        )

    @pyqtSlot()
    def showAboutQt(self):
        """About box for Qt"""

        QMessageBox.aboutQt(self, self.tr("About Qt"))

    @pyqtSlot()
    def showSettings(self):
        """Show settings dialog"""
        pass

    def save_settings(self):
        settings = QSettings()
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())

    def load_settings(self):
        # MainWindow settings
        settings = QSettings()
        if settings.value("geometry") is not None:
            self.restoreGeometry(settings.value("geometry"))
        if settings.value("windowState") is not None:
            self.restoreState(settings.value("windowState"))

    def closeEvent(self, event):
        self.assetWidget.maybe_save()
        self.save_settings()
        QMainWindow.closeEvent(self, event)
