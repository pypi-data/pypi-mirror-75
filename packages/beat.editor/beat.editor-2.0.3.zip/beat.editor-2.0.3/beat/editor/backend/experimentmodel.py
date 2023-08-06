# vim: set fileencoding=utf-8 :
###############################################################################
#                                                                             #
# Copyright (c) 2020 Idiap Research Institute, http://www.idiap.ch/           #
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

import typing

from beat.core.database import Database

from .asset import Asset
from .asset import AssetType


class Connection:
    """Class representing the connection between the output of a source block
    and the input of the corresponding sink.

    The information comes from the toolchain.
    """

    def __init__(
        self, source: str, output_name: str, sink: str, input_name: str
    ) -> None:
        self.source = source
        self.output_name = output_name
        self.sink = sink
        self.input_name = input_name

    def is_used_by_block(self, block_name: str):
        """Returns whether the given block is concerned by this connection"""

        return self.source == block_name or self.sink == block_name

    def __repr__(self) -> str:
        text = [
            f"{self.__class__.__name__}(",
            f"from: {self.source}.{self.output_name}",
            f"to:   {self.sink}.{self.input_name}",
            ")",
        ]

        return "\n".join(text)

    @property
    def from_output(self) -> str:
        return f"{self.source}.{self.output_name}"

    @property
    def to_input(self) -> str:
        return f"{self.sink}.{self.input_name}"


class ExperimentBlock:
    """Base class experiment blocks representation"""

    def __init__(self, name: str, config: dict) -> None:
        self.name: str = name

        self.parse(config)

    def parse(self, config: dict) -> None:
        raise NotImplementedError

    def dataformat_for_endpoint(self, endpoint: str) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"


class AlgorithmData:
    """Class containing the information related to the endpoints of an algorithm
    """

    def __init__(self) -> None:
        self.input_type_map: typing.Mapping[str, str] = {}
        self.output_type_map: typing.Mapping[str, str] = {}

        # left: alg io right: block io
        self.input_mapping: typing.Mapping[str, str] = {}
        self.output_mapping: typing.Mapping[str, str] = {}

    def parse(self, config: dict) -> None:
        prefix = config.pop("prefix")
        algorithm_name = config.get("algorithm")
        if algorithm_name is not None and algorithm_name != "":
            algorithm = Asset(prefix, AssetType.ALGORITHM, algorithm_name)
            is_valid, _ = algorithm.is_valid()
            if is_valid:
                for group in algorithm.declaration["groups"]:
                    for io_type, type_map in [
                        ("inputs", self.input_type_map),
                        ("outputs", self.output_type_map),
                    ]:
                        for input_name, input_data in group.get(io_type, {}).items():
                            type_map[input_name] = input_data["type"]

        self.input_mapping = config.get("inputs", {})
        self.output_mapping = config.get("outputs", {})

    def dataformat_for_endpoint(self, endpoint: str) -> str:
        for alg_in, block_in in self.input_mapping.items():
            if block_in == endpoint:
                return self.input_type_map.get(alg_in, "")

        for alg_out, block_out in self.output_mapping.items():
            if block_out == endpoint:
                return self.output_type_map.get(alg_out, "")
        return ""

    def __repr__(self) -> str:
        representation = [f"{self.__class__.__name__}("]
        if self.input_type_map:
            representation += [
                "inputs:" f"    {self.input_mapping}" f"    {self.input_type_map}"
            ]
        if self.output_type_map:
            representation += [
                "outputs:" f"    {self.output_mapping}" f"    {self.output_type_map}"
            ]
        representation.append(")")

        return "\n".join(representation)


class AlgorithmBlock(ExperimentBlock):
    """Class containing the endpoints of an algorithm block"""

    def __init__(self, name: str, config: dict) -> None:
        self.algorithm_data: AlgorithmData = AlgorithmData()

        super().__init__(name, config)

    def parse(self, config: dict) -> None:
        self.algorithm_data.parse(config)

    def dataformat_for_endpoint(self, endpoint: str) -> str:
        return self.algorithm_data.dataformat_for_endpoint(endpoint)

    def __repr__(self) -> str:
        text = [
            f"{self.__class__.__name__}(",
            f"name: {self.name}",
            f"    {self.algorithm_data}",
            ")",
        ]

        return "\n".join(text)


class LoopBlock(ExperimentBlock):
    """Class containing the endpoints of a loop block"""

    def __init__(self, name: str, config: dict) -> None:
        self.processor_data: AlgorithmData = AlgorithmData()
        self.evaluator_data: AlgorithmData = AlgorithmData()

        super().__init__(name, config)

    def parse(self, config: dict) -> None:
        for algorithm_type, algorithm_data in (
            ("processor_", self.processor_data),
            ("evaluator_", self.evaluator_data),
        ):
            keys = [key for key in config.keys() if key.startswith(algorithm_type)]
            algorithm_config = {"prefix": config["prefix"]}
            for key in keys:
                algorithm_config[key[len(algorithm_type) :]] = config[key]
            algorithm_data.parse(algorithm_config)

    def dataformat_for_endpoint(self, endpoint: str) -> str:
        data_format = self.processor_data.dataformat_for_endpoint(endpoint)
        if not data_format:
            data_format = self.evaluator_data.dataformat_for_endpoint(endpoint)

        return data_format

    def __repr__(self) -> str:
        text = [
            f"{self.__class__.__name__}(",
            f"name: {self.name}",
            f"processor: {self.processor_data}",
            f"evaluator: {self.evaluator_data}",
            ")",
        ]

        return "\n".join(text)


class AnalyzerBlock(AlgorithmBlock):
    """Class containing the endpoints of an analyzer block"""


class DatasetBlock(ExperimentBlock):
    """Class containing the endpoints of a dataset block"""

    def __init__(self, name: str, config: dict) -> None:
        self.output_type_map: typing.Mapping[str, str] = {}

        super().__init__(name, config)

    def parse(self, config: dict) -> None:
        prefix = config.pop("prefix")
        database_name = config.get("database")
        if database_name:
            database = Database(prefix, database_name)
            if database.valid:
                set_data = database.set(config["protocol"], config["set"])
                self.output_type_map = set_data.get("outputs", {})

    def dataformat_for_endpoint(self, endpoint: str) -> str:
        return self.output_type_map.get(endpoint, "")

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"name: {self.name}\n"
            f"outputs: {self.output_type_map}\n"
            ")\n"
        )


ErrorMap = typing.Mapping[str, typing.List[str]]


class ExperimentModel:
    """This class contains the connection related information for an experiment.

    It's goal is to allow the verification of the compatibility between two
    blocks connected endpoints.
    """

    def __init__(self) -> None:
        self.connections: typing.List[Connection] = []
        self.blocks: typing.Mapping[str, ExperimentBlock] = {}
        self.experiment: Asset = None

    def _load_toolchain_info(self) -> None:
        """Load the needed information from the toolchain
           Currently only the connections are of interest.
        """

        toolchain = Asset(
            self.experiment.prefix,
            AssetType.TOOLCHAIN,
            "/".join(self.experiment.name.split("/")[1:4]),
        )
        declaration = toolchain.declaration

        # Load connections
        connections = declaration["connections"]

        for connection in connections:
            source, output = connection["from"].split(".")
            sink, input_ = connection["to"].split(".")
            self.connections.append(Connection(source, output, sink, input_))

    def _load_experiment_info(self) -> None:
        """Load all the endpoints related information."""

        declaration = self.experiment.declaration

        for block_type, klass in [
            ("blocks", AlgorithmBlock),
            ("loops", LoopBlock),
            ("analyzers", AnalyzerBlock),
            ("datasets", DatasetBlock),
        ]:
            for block_name, config in declaration.get(block_type, {}).items():
                config["prefix"] = self.experiment.prefix
                self.blocks[block_name] = klass(block_name, config)

    def load_experiment(self, experiment: Asset) -> None:
        """Load the required experiment data"""

        self.clear()
        self.experiment = experiment
        self._load_toolchain_info()
        self._load_experiment_info()

    def clear(self) -> None:
        """Clear the model content"""

        self.connections = []
        self.blocks = {}

    def update_block(self, block_name: str, config: dict) -> None:
        """Update one block content"""

        config["prefix"] = self.experiment.prefix
        self.blocks[block_name].parse(config)

    def check_all_blocks(self) -> ErrorMap:
        """Check that all blocks connections are compatible"""

        declaration = self.experiment.declaration
        error_map: ErrorMap = {}

        for block_type in ["blocks", "loops", "analyzers", "datasets"]:
            for block_name in declaration.get(block_type, {}).keys():
                error_list = self.check_block(block_name)
                if error_list:
                    error_map[block_name] = error_list

        return error_map

    def check_block(self, block_name: str) -> typing.List[str]:
        """Check that one block connections are compatible"""

        connections = [
            connection
            for connection in self.connections
            if connection.is_used_by_block(block_name)
        ]

        connection_error_list = []

        for connection in connections:
            source_block = self.blocks[connection.source]
            from_df = source_block.dataformat_for_endpoint(connection.output_name)
            sink_block = self.blocks[connection.sink]
            to_df = sink_block.dataformat_for_endpoint(connection.input_name)

            if from_df and to_df:
                if from_df != to_df:
                    connection_error_list.append(
                        f"{connection.from_output} {from_df} is not compatible with {connection.to_input} {to_df}"
                    )
            #  else:
            #  Either side of the connection being unassigned means that the
            #  connection is "correct".

        return connection_error_list
