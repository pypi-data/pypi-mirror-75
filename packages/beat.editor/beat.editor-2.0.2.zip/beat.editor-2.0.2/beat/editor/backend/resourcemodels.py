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

import logging

import simplejson as json

from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtSql import QSqlTableModel

from beat.core.database import Database

from .asset import Asset
from .asset import AssetType
from .assetmodel import AssetModel

PARAMETER_TYPE_KEY = "parameter_type"
DEFAULT_VALUE_KEY = "default_value"
EDITED_KEY = "edited"

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------

# Prefix modelization


class ExperimentResources:
    """Modelization of the experiments resources"""

    def __init__(self, context=None):
        self.context = context

        database = QSqlDatabase.addDatabase("QSQLITE")
        database.setDatabaseName(":memory:")

        if not database.open():
            raise RuntimeError(
                f"Failed to open database: {database.lastError().text()}"
            )

        self.refresh()

    def setContext(self, context):
        if self.context == context:
            return

        self.context = context
        self.refresh()

    def refresh(self):
        ALGORITHM_TABLE_CLEANUP = "DROP TABLE IF EXISTS algorithms"
        ALGORITHM_TABLE = "CREATE TABLE algorithms(name varchar, type varchar, inputs integer, outputs integer, is_analyzer boolean)"
        INSERT_ALGORITHM = "INSERT INTO algorithms(name, type, inputs, outputs, is_analyzer) VALUES(?, ?, ?, ?, ?)"
        QUEUE_TABLE_CLEANUP = "DROP TABLE IF EXISTS queues"
        QUEUE_TABLE = "CREATE TABLE queues(name varchar, env_name varchar, env_version varchar, env_type varchar)"
        INSERT_QUEUE = "INSERT INTO queues(name, env_name, env_version, env_type) VALUES (?, ?, ?, ?)"
        DATASET_TABLE_CLEANUP = "DROP TABLE IF EXISTS datasets"
        DATASET_TABLE = "CREATE TABLE datasets(name varchar, outputs integer)"
        INSERT_DATASET = "INSERT INTO datasets(name, outputs) VALUES(?, ?)"

        query = QSqlQuery()

        for query_str in [
            ALGORITHM_TABLE_CLEANUP,
            QUEUE_TABLE_CLEANUP,
            DATASET_TABLE_CLEANUP,
        ]:
            if not query.exec_(query_str):
                raise RuntimeError(f"Failed to drop table: {query.lastError().text()}")

        for query_str in [ALGORITHM_TABLE, QUEUE_TABLE, DATASET_TABLE]:
            if not query.exec_(query_str):
                raise RuntimeError(
                    f"Failed to create table: {query.lastError().text()}"
                )

        if self.context is None:
            return

        prefix_path = self.context.meta["config"].path
        model = AssetModel()
        model.asset_type = AssetType.ALGORITHM
        model.prefix_path = prefix_path
        model.setLatestOnlyEnabled(False)

        if not query.prepare(INSERT_ALGORITHM):
            raise RuntimeError(f"Failed to prepare query: {query.lastError().text()}")

        for algorithm in model.stringList():
            asset = Asset(prefix_path, AssetType.ALGORITHM, algorithm)
            is_valid, _ = asset.is_valid()
            if not is_valid:
                logger.debug("Skipping invalid algorithm {}".format(algorithm))
                continue

            declaration = asset.declaration
            inputs = {}
            outputs = {}
            for group in declaration["groups"]:
                inputs.update(group.get("inputs", {}))
                outputs.update(group.get("outputs", {}))

            query.addBindValue(algorithm)
            query.addBindValue(declaration.get("type", "legacy"))
            query.addBindValue(len(inputs))
            query.addBindValue(len(outputs))
            query.addBindValue("results" in declaration)

            if not query.exec_():
                raise RuntimeError(
                    f"Failed to insert algorithm: {query.lastError().text()}"
                )

        if not query.prepare(INSERT_QUEUE):
            raise RuntimeError(f"Failed to prepare query: {query.lastError().text()}")

        environments_path = self.context.meta["environments"]
        with open(environments_path, "rt") as file:
            environment_data = json.load(file)

        for item in environment_data.get("remote", []):
            env_name = item["name"]
            env_version = item["version"]
            # import ipdb; ipdb.set_trace()
            for name in item["queues"].keys():
                query.addBindValue(name)
                query.addBindValue(env_name)
                query.addBindValue(env_version)
                query.addBindValue("remote")

                if not query.exec_():
                    raise RuntimeError(
                        f"Failed to insert queue: {query.lastError().text()}"
                    )

        for _, image_info in environment_data.get("docker", {}).items():
            env_name = image_info["name"]
            env_version = image_info["version"]
            query.addBindValue("Local")
            query.addBindValue(env_name)
            query.addBindValue(env_version)
            query.addBindValue("docker")
            if not query.exec_():
                raise RuntimeError(
                    f"Failed to insert queue: {query.lastError().text()}"
                )

        model.asset_type = AssetType.DATABASE

        if not query.prepare(INSERT_DATASET):
            raise RuntimeError(f"Failed to prepare query: {query.lastError().text()}")

        for database_name in model.stringList():
            database = Database(prefix_path, database_name)
            if not database.valid:
                logger.debug("Skipping invalid database: {}".format(database_name))
                continue
            protocols = database.protocol_names
            for protocol_name in protocols:
                sets = database.set_names(protocol_name)
                for set_name in sets:
                    set_data = database.set(protocol_name, set_name)
                    name = f"{database_name}/{protocol_name}/{set_name}"
                    output_count = len(set_data["outputs"])
                    query.addBindValue(name)
                    query.addBindValue(output_count)

                    if not query.exec_():
                        raise RuntimeError(
                            f"Failed to insert dataset: {query.lastError().text()}"
                        )


experiment_resources = ExperimentResources()


class AlgorithmResourceModel(QSqlTableModel):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._analyzer_enabled = False
        self._input_count = None
        self._output_count = None
        self._types = []

        self.setTable("algorithms")
        self.select()
        self.update()

    def update(self):
        filter_str = f"is_analyzer={self._analyzer_enabled}"
        if self._input_count is not None:
            filter_str += f" AND inputs={self._input_count}"
        if self._output_count is not None:
            filter_str += f" AND outputs={self._output_count}"

        if self._types:
            filter_str += " AND type in ({})".format(
                ",".join([f"'{type_}'" for type_ in self._types])
            )

        self.setFilter(filter_str)

    def setAnalyzerEnabled(self, enabled):
        if self._analyzer_enabled == enabled:
            return

        self._analyzer_enabled = enabled
        self.update()

    def setInputCount(self, count):
        if self._input_count == count:
            return

        self._input_count = count
        self.update()

    def setOutputCount(self, count):
        if self._output_count == count:
            return

        self._output_count = count
        self.update()

    def setTypes(self, type_list):
        if self._types == type_list:
            return

        self._types = type_list
        self.update()


class QueueResourceModel(QSqlTableModel):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._environment = None
        self._version = None
        self._type = None

        self.setTable("queues")
        self.select()
        self.update()

    def update(self):
        filter_str = ""
        if self._environment is not None:
            filter_str += f"env_name='{self._environment}'"

        if self._version is not None:
            if filter_str:
                filter_str += " AND "
            filter_str += f"env_version='{self._version}'"

        if self._type is not None:
            if filter_str:
                filter_str += " AND "
            filter_str += f"env_type='{self._type}'"

        self.setFilter(filter_str)

    def setEnvironment(self, name, version):
        if self._environment == name and self._version == version:
            return

        self._environment = name
        self._version = version
        self.update()

    def setType(self, type_):
        if self._type == type_:
            return

        self._type = type_
        self.update()

    def dump(self):
        print(self.filter())
        for i in range(self.rowCount()):
            print([self.index(i, j).data() for j in range(4)])


class DatasetResourceModel(QSqlTableModel):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._analyzer_enabled = False
        self._output_count = None

        self.setTable("datasets")
        self.select()

    def update(self):
        filter_str = ""

        if self._output_count is not None:
            filter_str = f"outputs={self._output_count}"

        self.setFilter(filter_str)

    def setOutputCount(self, count):
        if self._output_count == count:
            return

        self._output_count = count
        self.update()
