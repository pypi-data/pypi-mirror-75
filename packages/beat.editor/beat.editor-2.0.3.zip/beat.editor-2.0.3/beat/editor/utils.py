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
Helper methods and utilities
"""

import logging
import os
import shutil
import sys

import pkg_resources
import simplejson as json

from packaging import version
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox

from beat.core.algorithm import load_algorithm_prototype

from .backend.asset import AssetType

logger = logging.getLogger(__name__)


def setup_logger(name, verbosity):
    """Sets up the logging of a script


    Parameters:

        name (str): The name of the logger to setup

        verbosity (int): The verbosity level to operate with. A value of ``0``
            (zero) means only errors, ``1``, errors and warnings; ``2``, errors,
            warnings and informational messages and, finally, ``3``, all types of
            messages including debugging ones.

    """

    logger = logging.getLogger(name)
    formatter = logging.Formatter(
        "%(name)s@%(asctime)s -- %(levelname)s: " "%(message)s"
    )

    _warn_err = logging.StreamHandler(sys.stderr)
    _warn_err.setFormatter(formatter)
    _warn_err.setLevel(logging.WARNING)

    class _InfoFilter:
        def filter(self, record):
            return record.levelno <= logging.INFO

    _debug_info = logging.StreamHandler(sys.stdout)
    _debug_info.setFormatter(formatter)
    _debug_info.setLevel(logging.DEBUG)
    _debug_info.addFilter(_InfoFilter())

    logger.addHandler(_debug_info)
    logger.addHandler(_warn_err)

    logger.setLevel(logging.ERROR)
    if verbosity == 1:
        logger.setLevel(logging.WARNING)
    elif verbosity == 2:
        logger.setLevel(logging.INFO)
    elif verbosity >= 3:
        logger.setLevel(logging.DEBUG)

    return logger


def dataformat_basetypes():
    """Returns the list of base types that can be used for dataformat"""

    common_data = pkg_resources.resource_string("beat.core", "schema/common/1.json")
    common_data = json.loads(common_data)

    definitions = common_data["definitions"]
    basetype = definitions["basetype"]
    types = []
    if "enum" in basetype:
        types = basetype["enum"]
    elif "anyOf" in basetype:
        for item in basetype["anyOf"]:
            if "$ref" in item:
                definition = item["$ref"].split("/")[-1]
                types += definitions[definition]["enum"]
            elif "enum" in item:
                types += item["enum"]
    else:
        raise RuntimeError("Unsupported schema version")

    return types


def is_Qt_equal_or_higher(version_string):
    return version.parse(QtCore.QT_VERSION_STR) >= version.parse(version_string)


def check_prefix_folders(prefix_path):
    """Check that all supported asset types have their containing folder
    available
    """

    modified = False
    result = True
    missing_folders = []

    for asset_type in AssetType:
        if asset_type is not AssetType.UNKNOWN:
            path = os.path.join(prefix_path, asset_type.path)
            if not os.path.exists(path):
                missing_folders.append(path)

    if missing_folders:
        answer = QMessageBox.question(
            None,
            QCoreApplication.translate("utils", "Prefix incomplete"),
            QCoreApplication.translate(
                "utils",
                "Your prefix is missing folders.\n" "Would you like to create them ?",
            ),
        )

        if answer == QMessageBox.Yes:
            for folder in missing_folders:
                os.makedirs(folder)
            modified = True
        else:
            result = False

    return result, modified


def check_prefix_dataformats(prefix_path):
    """Currently checks that the data format needed for the algorithm is
    available
    """

    modified = False
    result = True

    try:
        load_algorithm_prototype(prefix_path)
    except RuntimeError:
        answer = QMessageBox.question(
            None,
            QCoreApplication.translate("utils", "Prefix incomplete"),
            QCoreApplication.translate(
                "utils",
                "Your prefix is missing a mandatory data format.\n"
                "Would you like to create it ?",
            ),
        )

        if answer == QMessageBox.Yes:
            asset_type = AssetType.DATAFORMAT
            integers_path = os.path.join("prefix", asset_type.path, "user", "integers")
            integers_folder = pkg_resources.resource_filename(
                "beat.core.test", integers_path
            )
            shutil.copytree(
                integers_folder,
                os.path.join(prefix_path, asset_type.path, "user", "integers"),
            )
            modified = True
        else:
            result = False

    return result, modified
