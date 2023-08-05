#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###############################################################################
#                                                                             #
# Copyright (c) 2016 Idiap Research Institute, http://www.idiap.ch/           #
# Contact: beat.support@idiap.ch                                              #
#                                                                             #
# This file is part of the beat.cmdline module of the BEAT platform.          #
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
Test the utils.py file
"""

import os
import tempfile

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox

from .. import utils
from ..backend.asset import AssetType


def test_Qt_version_equal():
    assert utils.is_Qt_equal_or_higher(QtCore.QT_VERSION_STR)


def test_Qt_version_higher():
    assert utils.is_Qt_equal_or_higher("4.8.7")


def test_Qt_version_smaller():
    assert not utils.is_Qt_equal_or_higher("12.0.0")


def test_check_prefix_folders_yes(monkeypatch):
    monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.Yes)
    with tempfile.TemporaryDirectory() as prefix_folder:
        result, modified = utils.check_prefix_folders(prefix_folder)
        assert result
        assert modified

        for asset_type in AssetType:
            if asset_type == AssetType.UNKNOWN:
                continue
            assert os.path.exists(os.path.join(prefix_folder, asset_type.path))

        result, modified = utils.check_prefix_folders(prefix_folder)
        assert result
        assert not modified


def test_check_prefix_folders_no(monkeypatch):
    monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.No)
    with tempfile.TemporaryDirectory() as prefix_folder:
        result, modified = utils.check_prefix_folders(prefix_folder)
        assert not result
        assert not modified
        assert os.listdir(prefix_folder) == []


def test_check_prefix_folders_with_prefix(monkeypatch, test_prefix):
    result, modified = utils.check_prefix_folders(test_prefix)
    assert result
    assert not modified


def test_check_prefix_dataformats_yes(monkeypatch):
    monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.Yes)
    with tempfile.TemporaryDirectory() as prefix_folder:
        result, modified = utils.check_prefix_dataformats(prefix_folder)
        assert result
        assert modified

        asset_type = AssetType.DATAFORMAT
        assert os.path.exists(
            os.path.join(prefix_folder, asset_type.path, "user", "integers")
        )

        result, modified = utils.check_prefix_dataformats(prefix_folder)
        assert result
        assert not modified


def test_check_prefix_dataformats_no(monkeypatch):
    monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.No)
    with tempfile.TemporaryDirectory() as prefix_folder:
        result, modified = utils.check_prefix_dataformats(prefix_folder)
        assert not result
        assert not modified
        assert os.listdir(prefix_folder) == []


def test_check_prefix_dataformats_with_prefix(monkeypatch, test_prefix):
    result, modified = utils.check_prefix_dataformats(test_prefix)
    assert result
    assert not modified
