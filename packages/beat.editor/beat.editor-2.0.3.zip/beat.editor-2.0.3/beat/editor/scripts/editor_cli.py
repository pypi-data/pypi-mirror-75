#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (c) 2016 Idiap Research Institute, http://www.idiap.ch/           #
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

"""
The main entry for beat.editor (click-based) scripts.
"""

import os
import sys

import click
import pkg_resources

from click_plugins import with_plugins
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from beat.cmdline import environments
from beat.cmdline.click_helper import AliasedGroup
from beat.cmdline.decorators import raise_on_error
from beat.cmdline.decorators import verbosity_option

from .. import version
from ..backend.asset import Asset
from ..backend.asset import AssetType
from ..backend.eventfilters import MouseWheelFilter
from ..utils import check_prefix_dataformats
from ..utils import check_prefix_folders
from ..utils import setup_logger
from ..widgets.assetwidget import AssetWidget
from ..widgets.mainwindow import MainWindow

global logger
logger = None


def setup_environment_cache(ctx, param, value):
    """Click option callback to setup environment cache"""

    if not value:
        environments_file_path = ctx.meta["environments"]
        if not os.path.exists(environments_file_path):
            ctx.invoke(environments.list, type_="all", output=environments_file_path)


def check_prefix(prefix_path):
    """Check that the prefix is usable"""

    folder_status, _ = check_prefix_folders(prefix_path)
    dataformat_status, _ = check_prefix_dataformats(prefix_path)
    return folder_status and dataformat_status


refresh_environment_cache_flag = click.option(
    "--no-check-env",
    is_flag=True,
    expose_value=False,
    default=False,
    help="Do not check for environment cache",
    callback=setup_environment_cache,
)


@with_plugins(pkg_resources.iter_entry_points("beat.editor.cli"))
@click.group(cls=AliasedGroup)
@click.option(
    "--environments",
    "-e",
    help="Overrides the path to the environment file. If not set use the value from your RC file [default: <prefix>/.environments.json]",
    type=click.STRING,
    default=".environments.json",
)
@verbosity_option()
@click.pass_context
def editor(ctx, environments):
    """beat.editor commands."""

    config = ctx.meta["config"]
    config.set("prefix", os.path.abspath(config.path))

    if not os.path.isabs(environments):
        environments = os.path.abspath(os.path.join(config.prefix, environments))

    ctx.meta["environments"] = environments

    global logger
    logger = setup_logger("beat.editor", ctx.meta["verbosity"])
    logger.info("BEAT prefix set to `%s'", ctx.meta["config"].path)

    QCoreApplication.setApplicationName("beat.editor")
    QCoreApplication.setOrganizationName("Idiap")
    QCoreApplication.setOrganizationDomain("ch.idiap")
    QCoreApplication.setApplicationVersion(version.__version__)


@editor.command(
    epilog="""\b
Example:
        $ beat editor start

"""
)
@click.pass_context
@refresh_environment_cache_flag
@raise_on_error
def start(ctx):
    """Start the beat editor"""

    app = QApplication(sys.argv)

    config = ctx.meta["config"]
    if not check_prefix(config.prefix):
        return

    app.setWindowIcon(QIcon(":/resources/appicon"))
    app.installEventFilter(MouseWheelFilter(app))
    mainwindow = MainWindow()
    mainwindow.set_context(ctx)
    mainwindow.show()

    return app.exec_()


@editor.command(
    epilog="""\b
Example:
        $ beat editor edit algorithm user/my_algo/1

"""
)
@click.argument("asset_type")
@click.argument("asset_name")
@click.pass_context
@refresh_environment_cache_flag
@raise_on_error
def edit(ctx, asset_type, asset_name):
    """Edit one specific asset"""

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/resources/appicon"))

    asset_widget = AssetWidget()
    asset_widget.set_context(ctx)

    asset_type = AssetType[asset_type.upper()]
    asset = Asset(ctx.meta["config"].path, asset_type, asset_name)
    asset_widget.loadAsset(asset)
    asset_widget.show()

    return app.exec_()


@editor.command(
    epilog="""\b
Example:
        $ beat editor refresh_env

"""
)
@click.option(
    "--type",
    "-t",
    "type_",
    type=click.Choice(["docker", "remote", "all"], case_sensitive=False),
    default="all",
)
@click.pass_context
@raise_on_error
def refresh_env(ctx, type_):
    """Update environments cache"""

    environments_file_path = ctx.meta["environments"]
    if os.path.exists(environments_file_path):
        os.remove(environments_file_path)
    ctx.invoke(environments.list, type_=type_, output=environments_file_path)
