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

import importlib
import os
import shutil
import subprocess
import sys
import tempfile

from collections import namedtuple

import pkg_resources
import pytest
import simplejson as json

from beat.cmdline.config import Configuration

from ..backend.asset import AssetType

if sys.platform == "darwin":
    prefix_folder = tempfile.mkdtemp(prefix=__name__, suffix=".prefix", dir="/tmp")
else:
    prefix_folder = tempfile.mkdtemp(prefix=__name__, suffix=".prefix")


prefix = os.path.join(prefix_folder, "prefix")
environment_file = os.path.join(prefix, "environment.json")


def sync_prefix():
    """Copy the content of the various package test prefixes in the running test prefix"""

    prefixes = [
        pkg_resources.resource_filename("beat.backend.python.test", "prefix"),
        pkg_resources.resource_filename("beat.core.test", "prefix"),
        pkg_resources.resource_filename("beat.editor.test", "prefix"),
    ]

    for path in prefixes:
        subprocess.check_call(["rsync", "-arz", path, prefix_folder])


def clean_prefix():
    """Removes the content of the test prefix(s)"""

    shutil.rmtree(prefix_folder)

    # Getting the prefix from beat.core triggers its setup_package but not the
    # corresponding tear down, therefore trigger it manually
    beat_core_test = importlib.import_module("beat.core.test")
    teardown_package = getattr(beat_core_test, "teardown_package")

    try:
        teardown_package()
    except FileNotFoundError:
        # Only needed once because that prefix is generated on call of the
        # resource_filename of beat.core.test
        pass


@pytest.fixture(
    scope="module", params=[item for item in AssetType if item is not AssetType.UNKNOWN]
)
def asset_type(request):
    return request.param


@pytest.fixture(scope="module")
def test_prefix():
    sync_prefix()

    with open(environment_file, "wt") as env_file:
        env_file.write(
            json.dumps(
                {
                    "remote": [
                        {
                            "name": "Python 2.7",
                            "version": "1.3.0",
                            "queues": {"queue1": {}, "queue2": {}},
                        },
                        {
                            "name": "Python",
                            "version": "2.0.0",
                            "queues": {
                                "queue_extra_long": {},
                                "queue_long": {},
                                "queue_short": {},
                            },
                        },
                    ],
                    "docker": {
                        "Docker test env": {"name": "Pytorch", "version": "1.1.1"},
                        "Second Docker test env": {
                            "name": "Pytorch 1.0",
                            "version": "2.1.1",
                        },
                    },
                }
            )
        )

    yield prefix

    clean_prefix()


@pytest.fixture(scope="module")
def beat_context(test_prefix):
    Context = namedtuple("Context", ["meta"])
    context = Context(
        meta={
            "--user": "user",
            "--prefix": test_prefix,
            "environments": environment_file,
        }
    )

    config = Configuration(context.meta)
    context.meta["config"] = config
    return context
