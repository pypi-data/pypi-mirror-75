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

import copy

import pytest

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QPushButton

from beat.backend.python.algorithm import Algorithm
from beat.core.experiment import EVALUATOR_PREFIX
from beat.core.experiment import PROCESSOR_PREFIX

from ..backend.asset import Asset
from ..backend.asset import AssetType
from ..backend.assetmodel import AssetModel
from ..backend.resourcemodels import AlgorithmResourceModel
from ..backend.resourcemodels import ExperimentResources
from ..backend.resourcemodels import QueueResourceModel
from ..backend.resourcemodels import experiment_resources
from ..widgets.experimenteditor import AlgorithmParametersEditor
from ..widgets.experimenteditor import AnalyzerBlockEditor
from ..widgets.experimenteditor import BlockEditor
from ..widgets.experimenteditor import DatasetEditor
from ..widgets.experimenteditor import EnvironmentModel
from ..widgets.experimenteditor import ExecutionPropertiesEditor
from ..widgets.experimenteditor import ExperimentEditor
from ..widgets.experimenteditor import GlobalParametersEditor
from ..widgets.experimenteditor import IOMapperDialog
from ..widgets.experimenteditor import LoopBlockEditor
from ..widgets.experimenteditor import typed_user_property
from ..widgets.spinboxes import NumpySpinBox
from .conftest import prefix
from .conftest import sync_prefix

# ------------------------------------------------------------------------------
# Constants


DEFAULT_ALGORITHM = "autonomous/parametrized/1"


# ------------------------------------------------------------------------------
# Helpers


def get_experiment_declaration(prefix_path, experiment_name):
    asset = Asset(prefix, AssetType.EXPERIMENT, experiment_name)
    return asset.declaration


def get_algorithm_declaration(prefix_path, algorithm_name):
    asset = Asset(prefix, AssetType.ALGORITHM, algorithm_name)
    return asset.declaration


def get_parameters(prefix_path, algorithm_name):
    return get_algorithm_declaration(prefix_path, algorithm_name)["parameters"]


def parameter_default_map(prefix_path, algorithm_name):
    sync_prefix()
    parameters = get_parameters(prefix_path, algorithm_name)
    return {name: value["default"] for name, value in parameters.items()}


def parameter_range_map(prefix_path, algorithm_name):
    sync_prefix()
    parameters = get_parameters(prefix_path, algorithm_name)
    return {
        name: value["default"] for name, value in parameters.items() if "range" in value
    }


def parameter_choice_map(prefix_path, algorithm_name):
    sync_prefix()
    parameters = get_parameters(prefix_path, algorithm_name)
    return {
        name: value["default"]
        for name, value in parameters.items()
        if "choice" in value
    }


def change_index(index):
    if index > 0:
        return index - 1
    else:
        return index + 1


# ------------------------------------------------------------------------------
# Fixtures


@pytest.fixture()
def algorithm_model(test_prefix):
    algorithm_model = AssetModel()
    algorithm_model.asset_type = AssetType.ALGORITHM
    algorithm_model.prefix_path = test_prefix
    return algorithm_model


@pytest.fixture()
def parametrized_algorithm():
    return DEFAULT_ALGORITHM


@pytest.fixture()
def test_experiment():
    return "user/user/two_loops/1/two_loops"


@pytest.fixture(params=parameter_default_map(prefix, DEFAULT_ALGORITHM))
def parameter_name(request):
    return request.param


@pytest.fixture(params=parameter_range_map(prefix, DEFAULT_ALGORITHM))
def range_parameter_name(request):
    return request.param


@pytest.fixture(params=parameter_choice_map(prefix, DEFAULT_ALGORITHM))
def choice_parameter_name(request):
    return request.param


# ------------------------------------------------------------------------------
# Tests


class TestExperimentResources:
    """Test that the prefix modelisation generates the expected data"""

    def test_model(self, beat_context):
        model = ExperimentResources(beat_context)

        model = QSqlTableModel()
        model.setTable("algorithms")
        model.select()

        total = model.rowCount()
        assert total > 0

        model.setFilter("is_analyzer=True")

        analyzer_count = model.rowCount()
        assert analyzer_count > 0
        assert analyzer_count < total


class TestAlgorithmResourceModel:
    """Test the model used to generate suitable algorithm selections"""

    @pytest.fixture
    def prefix_model(self, beat_context):
        return ExperimentResources(beat_context)

    def test_default(self, prefix_model):
        algorithm_model = AlgorithmResourceModel()

        query = QSqlQuery()
        assert query.exec_(
            "SELECT COUNT(name) AS cnt FROM algorithms WHERE is_analyzer=false"
        )

        query.next()

        assert algorithm_model.rowCount() == query.value("cnt")

    def test_analyzers(self, prefix_model):
        algorithm_model = AlgorithmResourceModel()
        algorithm_model.setAnalyzerEnabled(True)

        query = QSqlQuery()
        assert query.exec_(
            "SELECT COUNT(name) AS cnt FROM algorithms WHERE is_analyzer=true"
        )

        query.next()

        assert algorithm_model.rowCount() == query.value("cnt")

    def test_types(self, prefix_model):
        algorithm_model = AlgorithmResourceModel()
        algorithm_model.setTypes(
            [Algorithm.LEGACY, Algorithm.SEQUENTIAL, Algorithm.AUTONOMOUS]
        )

        query = QSqlQuery()
        assert query.exec_(
            "SELECT COUNT(name) AS cnt FROM algorithms WHERE is_analyzer=false AND type IN ('legacy', 'sequential', 'autonomous')"
        )

        query.next()

        assert algorithm_model.rowCount() == query.value("cnt")

    def test_output_count(self, prefix_model):
        algorithm_model = AlgorithmResourceModel()
        algorithm_model.setOutputCount(2)

        query = QSqlQuery()
        assert query.exec_(
            "SELECT COUNT(name) AS cnt FROM algorithms WHERE is_analyzer=false AND outputs='2'"
        )

        query.next()

        assert algorithm_model.rowCount() == query.value("cnt")

    def test_input_count(self, prefix_model):
        algorithm_model = AlgorithmResourceModel()
        algorithm_model.setInputCount(2)

        query = QSqlQuery()
        assert query.exec_(
            "SELECT COUNT(name) AS cnt FROM algorithms WHERE is_analyzer=false AND inputs='2'"
        )

        query.next()

        assert algorithm_model.rowCount() == query.value("cnt")

    def test_input_output_count(self, prefix_model):
        algorithm_model = AlgorithmResourceModel()
        algorithm_model.setInputCount(1)
        algorithm_model.setOutputCount(1)

        query = QSqlQuery()
        assert query.exec_(
            "SELECT COUNT(name) AS cnt FROM algorithms WHERE is_analyzer=false AND inputs='1' AND outputs='1'"
        )

        query.next()

        assert algorithm_model.rowCount() == query.value("cnt")

    def test_input_output_count_and_types(self, prefix_model):
        algorithm_model = AlgorithmResourceModel()
        algorithm_model.setInputCount(1)
        algorithm_model.setOutputCount(1)
        algorithm_model.setTypes([Algorithm.SEQUENTIAL])

        query = QSqlQuery()
        assert query.exec_(
            "SELECT COUNT(name) AS cnt FROM algorithms WHERE is_analyzer=false AND inputs='1' AND outputs='1' AND type IN ('sequential')"
        )

        query.next()

        assert algorithm_model.rowCount() == query.value("cnt")


class TestQueueResourceModel:
    """Test the model used to generate suitable algorithm selections"""

    @pytest.fixture
    def prefix_model(self, beat_context):
        return ExperimentResources(beat_context)

    def test_default(self, prefix_model):
        model = QueueResourceModel()

        query = QSqlQuery()
        assert query.exec_("SELECT COUNT(name) AS cnt FROM queues")

        query.next()

        assert model.rowCount() > 0
        assert model.rowCount() == query.value("cnt")

    def test_types(self, prefix_model):
        model = QueueResourceModel()
        for type_ in ["remote", "docker"]:
            model.setType(type_)

            query = QSqlQuery()
            assert query.exec_(
                f"SELECT COUNT(name) AS cnt FROM queues WHERE env_type='{type_}'"
            )

            query.next()

            assert model.rowCount() > 0
            assert model.rowCount() == query.value("cnt")


class TestIOMapperDialog:
    """Test that the dialog used for input/output mapping works as expected"""

    @staticmethod
    def get_dialog_parameters(test_prefix, test_experiment, block_type):
        experiment = Asset(test_prefix, AssetType.EXPERIMENT, test_experiment)
        declaration = experiment.declaration

        block_data = next(iter(declaration[block_type].values()))

        algorithm = Asset(test_prefix, AssetType.ALGORITHM, block_data["algorithm"])
        return algorithm.declaration, block_data

    @pytest.fixture()
    def algorithm_data(self, test_prefix, test_experiment):
        return self.get_dialog_parameters(test_prefix, test_experiment, "blocks")

    @pytest.fixture()
    def analyzer_data(self, test_prefix, test_experiment):
        return self.get_dialog_parameters(test_prefix, test_experiment, "analyzers")

    def test_load_and_dump_algorithm(self, qtbot, algorithm_data):
        algorithm, block_data = algorithm_data
        dialog = IOMapperDialog(algorithm, block_data)
        qtbot.addWidget(dialog)
        io_mapping = dialog.ioMapping()

        assert "inputs" in io_mapping
        assert "outputs" in io_mapping
        for field in io_mapping:
            assert block_data[field] == io_mapping[field]

    def test_load_and_dump_analyser(self, qtbot, analyzer_data):
        analyzer, block_data = analyzer_data
        dialog = IOMapperDialog(analyzer, block_data)
        qtbot.addWidget(dialog)
        io_mapping = dialog.ioMapping()

        assert "outputs" not in io_mapping
        for field in io_mapping:
            assert block_data[field] == io_mapping[field]


class TestDatasetEditor:
    """Test that the dataset editor works as expected"""

    @pytest.fixture()
    def datasets(self, test_prefix, test_experiment):
        asset = Asset(test_prefix, AssetType.EXPERIMENT, test_experiment)
        declaration = asset.declaration
        return declaration.get("datasets")

    @pytest.fixture()
    def original_dataset(self, datasets):
        dataset = next(iter(datasets))
        return datasets[dataset]

    @pytest.fixture()
    def other_dataset(self, datasets):
        iterator = iter(datasets)
        for i in range(0, 2):
            dataset = next(iterator)
        return datasets[dataset]

    @pytest.fixture()
    def editor(self, qtbot, test_prefix, datasets):
        editor = DatasetEditor("test_block", test_prefix)
        qtbot.addWidget(editor)
        return editor

    def test_load_and_dump(self, qtbot, editor, original_dataset):
        editor.load(original_dataset)

        assert editor.dump() == original_dataset

    def test_modification(self, qtbot, editor, original_dataset, other_dataset):
        editor.load(original_dataset)

        assert editor.dump() == original_dataset

        new_entry = "{}/{}/{}".format(
            other_dataset["database"], other_dataset["protocol"], other_dataset["set"]
        )

        with qtbot.waitSignal(editor.dataChanged):
            editor.dataset_combobox.setCurrentText(new_entry)

        assert editor.dump() == other_dataset

    def test_reset(self, qtbot, editor, original_dataset, other_dataset):
        editor.load(original_dataset)

        assert editor.dump() == original_dataset

        new_entry = "{}/{}/{}".format(
            other_dataset["database"], other_dataset["protocol"], other_dataset["set"]
        )

        with qtbot.waitSignal(editor.dataChanged):
            editor.dataset_combobox.setCurrentText(new_entry)

        assert editor.dump() == other_dataset

        with qtbot.waitSignal(editor.dataChanged):
            qtbot.mouseClick(editor.reset_button, Qt.LeftButton)

        assert editor.dump() == original_dataset


class TestAlgorithmParametersEditor:
    """Test that the algorithm parameters editor works as expected"""

    def test_load_and_dump(self, qtbot, test_prefix, parametrized_algorithm):
        editor = AlgorithmParametersEditor(test_prefix)
        qtbot.addWidget(editor)
        assert editor.isEmpty()

        with qtbot.waitSignal(editor.parameterCountChanged) as blocker:
            editor.setup(parametrized_algorithm)
        assert blocker.args == [33]

        editor.load({})

        assert editor.dump() == {}

    def test_edit(self, qtbot, test_prefix, parametrized_algorithm, parameter_name):
        editor = AlgorithmParametersEditor(test_prefix)
        qtbot.addWidget(editor)
        editor.setup(parametrized_algorithm)

        parameter_values = parameter_default_map(test_prefix, parametrized_algorithm)
        editor.load(parameter_values)
        widget = editor.editorForLabel(parameter_name)
        if isinstance(widget, NumpySpinBox):
            with qtbot.waitSignal(editor.dataChanged):
                widget.stepUp()

        elif isinstance(widget, QComboBox):
            with qtbot.waitSignal(editor.dataChanged):
                if widget.currentIndex() > 0:
                    new_index = 0
                else:
                    new_index = widget.count() - 1
                widget.setCurrentIndex(new_index)

        elif isinstance(widget, QCheckBox):
            with qtbot.waitSignal(editor.dataChanged):
                widget.setChecked(not widget.isChecked())

        json_reference = {parameter_name: typed_user_property(widget)}

        assert editor.dump() == json_reference

    def test_range(
        self, qtbot, test_prefix, parametrized_algorithm, range_parameter_name
    ):
        editor = AlgorithmParametersEditor(test_prefix)
        qtbot.addWidget(editor)
        editor.setup(parametrized_algorithm)

        parameters = get_parameters(test_prefix, parametrized_algorithm)
        minimum, maximum = parameters[range_parameter_name]["range"]

        widget = editor.editorForLabel(range_parameter_name)
        assert widget.minimum() == minimum
        assert widget.maximum() == maximum

    def test_out_of_range(
        self, qtbot, test_prefix, parametrized_algorithm, range_parameter_name
    ):
        editor = AlgorithmParametersEditor(test_prefix)
        qtbot.addWidget(editor)
        editor.setup(parametrized_algorithm)
        editor.load({range_parameter_name: 1})

        parameters = get_parameters(test_prefix, parametrized_algorithm)
        minimum, maximum = parameters[range_parameter_name]["range"]
        widget = editor.editorForLabel(range_parameter_name)

        with qtbot.waitSignal(editor.dataChanged):
            widget.setValue(maximum + 1)

        json_reference = {range_parameter_name: maximum}

        assert editor.dump() == json_reference

        with qtbot.waitSignal(editor.dataChanged):
            widget.setValue(minimum - 1)

        json_reference = {range_parameter_name: minimum}

        assert editor.dump() == json_reference

    def test_choice(
        self, qtbot, test_prefix, parametrized_algorithm, choice_parameter_name
    ):
        editor = AlgorithmParametersEditor(test_prefix)
        qtbot.addWidget(editor)
        editor.setup(parametrized_algorithm)

        parameters = get_parameters(test_prefix, parametrized_algorithm)
        parameter = parameters[choice_parameter_name]
        choices = parameter["choice"]

        # Numerical choices are stored as text in the editor
        choices = [str(choice) for choice in choices]
        widget = editor.editorForLabel(choice_parameter_name)
        widget.count() == len(choices)
        for i in range(0, widget.count()):
            assert widget.itemText(i) in choices


class TestEnvironmentModel:
    """Test that the environment model shows and return value as expected"""

    def test_setup(self, beat_context):
        model = EnvironmentModel()
        model.setContext(beat_context)

        assert model.rowCount() == 4

    def test_visual_name(self, beat_context):
        model = EnvironmentModel()
        model.setContext(beat_context)
        combobox = QComboBox()
        combobox.setModel(model)

        for i in range(0, model.rowCount()):
            environment = model.environment(model.index(i, 0))
            visual_name = "{name} ({version})".format(**environment)
            assert combobox.itemText(i) == visual_name


class ParameterTestMixin:
    """Mixin related to editors for blocks that can have parameters"""

    def test_edit_parameter(
        self, qtbot, properties_editor, test_prefix, test_experiment, algorithm_model
    ):
        qtbot.addWidget(properties_editor)

        experiment_declaration = get_experiment_declaration(
            test_prefix, test_experiment
        )
        algorithms = experiment_declaration[self.declaration_field]
        label = None
        parameter_editor = None
        for name, algorithm in algorithms.items():
            properties_editor.load(algorithm)
            parameters_editors = properties_editor.findChildren(
                AlgorithmParametersEditor
            )
            for parameters_editor in parameters_editors:
                if parameters_editor.parameterCount():
                    label = parameters_editor.labelForRow(0)
                    parameter_editor = parameters_editor.editorForRow(0)
                    # proper way to break out of nested loops
                    # https://mail.python.org/pipermail/python-3000/2007-July/008663.html
                    return

        assert isinstance(parameter_editor, NumpySpinBox)

        with qtbot.waitSignal(properties_editor.dataChanged):
            new_value = parameter_editor.value - 1
            parameter_editor.setValue(new_value)

        dump = properties_editor.dump()
        assert dump[self.parameter_field] == {label: new_value}

    def test_edit_parameter_going_back_to_default_value(
        self, qtbot, properties_editor, test_prefix, test_experiment, algorithm_model
    ):
        qtbot.addWidget(properties_editor)

        experiment_declaration = get_experiment_declaration(
            test_prefix, test_experiment
        )
        algorithms = experiment_declaration[self.declaration_field]
        parameter_editor = None
        for name, algorithm in algorithms.items():
            properties_editor.load(algorithm)
            parameters_editors = properties_editor.findChildren(
                AlgorithmParametersEditor
            )
            for parameters_editor in parameters_editors:
                if parameters_editor.parameterCount():
                    label = parameters_editor.labelForRow(0)
                    parameter_editor = parameters_editor.editorForRow(0)
                    break

        assert isinstance(parameter_editor, NumpySpinBox)

        with qtbot.waitSignal(properties_editor.dataChanged):
            new_value = parameter_editor.value - 1
            parameter_editor.setValue(new_value)

        with qtbot.waitSignal(properties_editor.dataChanged):
            new_value = parameter_editor.value + 1
            parameter_editor.setValue(new_value)

        dump = properties_editor.dump()
        assert dump[self.parameter_field] == {label: new_value}


class PropertiesEditorTestMixin:
    """Mixin that provides the common tests to execute for editors related to
       block properties
    """

    editor_klass = None
    declaration_field = ""
    parameter_field = ""

    def test_load_and_dump(
        self, qtbot, properties_editor, test_prefix, test_experiment, algorithm_model
    ):
        qtbot.addWidget(properties_editor)

        experiment_declaration = get_experiment_declaration(
            test_prefix, test_experiment
        )
        algorithms = experiment_declaration[self.declaration_field]
        first_algorithm = next(iter(algorithms))
        json_reference = algorithms[first_algorithm]

        properties_editor.load(json_reference)
        assert properties_editor.dump() == json_reference

    def test_edit_environment(
        self, qtbot, properties_editor, test_prefix, test_experiment, algorithm_model
    ):
        qtbot.addWidget(properties_editor)

        experiment_declaration = get_experiment_declaration(
            test_prefix, test_experiment
        )
        algorithms = experiment_declaration[self.declaration_field]
        first_algorithm = next(iter(algorithms))
        json_reference = algorithms[first_algorithm]

        properties_editor.load(json_reference)

        environment_model = properties_editor.environmentModel()
        environment = environment_model.environment(environment_model.index(1, 0))

        with qtbot.waitSignal(properties_editor.dataChanged):
            combobox = properties_editor.findChild(QComboBox, "environments")
            combobox.setCurrentIndex(1)

        assert properties_editor.dump()["environment"] == environment

    def test_edit_algorithm(
        self, qtbot, properties_editor, test_prefix, test_experiment, algorithm_model
    ):
        qtbot.addWidget(properties_editor)

        experiment_declaration = get_experiment_declaration(
            test_prefix, test_experiment
        )
        algorithms = experiment_declaration[self.declaration_field]
        first_algorithm = next(iter(algorithms))
        json_reference = algorithms[first_algorithm]

        properties_editor.load(json_reference)
        combobox = properties_editor.findChild(QComboBox, "algorithms")

        with qtbot.waitSignal(properties_editor.dataChanged):
            next_index = combobox.currentIndex() + 1
            if next_index == combobox.count():
                next_index -= 2
            combobox.setCurrentIndex(next_index)

        assert properties_editor.dump()["algorithm"] == combobox.currentText()

    def test_edit_io_mapping(
        self,
        qtbot,
        monkeypatch,
        properties_editor,
        test_prefix,
        test_experiment,
        algorithm_model,
    ):
        qtbot.addWidget(properties_editor)

        experiment_declaration = get_experiment_declaration(
            test_prefix, test_experiment
        )

        algorithms = experiment_declaration[self.declaration_field]
        first_algorithm = next(iter(algorithms))
        json_reference = algorithms[first_algorithm]

        properties_editor.load(json_reference)

        io_mapping_answer = {"inputs": json_reference["inputs"]}

        for key in io_mapping_answer["inputs"]:
            io_mapping_answer["inputs"] = "changed"

        if "outputs" in json_reference:
            io_mapping_answer["outputs"] = json_reference["outputs"]
            for key in io_mapping_answer["outputs"]:
                io_mapping_answer["outputs"] = "changed"

        monkeypatch.setattr(
            IOMapperDialog, "getIOMapping", lambda *args: (True, io_mapping_answer)
        )

        remap_button = properties_editor.findChild(QPushButton, "remap")
        with qtbot.waitSignal(properties_editor.dataChanged):
            qtbot.mouseClick(remap_button, Qt.LeftButton)

        assert properties_editor.dump()["inputs"] == io_mapping_answer["inputs"]
        if "outputs" in json_reference:
            assert properties_editor.dump()["outputs"] == io_mapping_answer["outputs"]


class TestExecutionPropertiesEditor(PropertiesEditorTestMixin, ParameterTestMixin):
    """Test that the AlgorithmEditor works as expected"""

    editor_klass = ExecutionPropertiesEditor
    declaration_field = "blocks"
    parameter_field = "parameters"

    @pytest.fixture(autouse=True)
    def prefix_model(self, beat_context):
        return ExperimentResources(beat_context)

    @pytest.fixture()
    def algorithm_model(self):
        return AlgorithmResourceModel()

    @pytest.fixture()
    def properties_editor(self, beat_context, test_prefix, algorithm_model):
        environment_model = EnvironmentModel()
        environment_model.setContext(beat_context)

        editor = self.editor_klass(test_prefix)
        editor.setAlgorithmResourceModel(algorithm_model)
        editor.setEnvironmentModel(environment_model)
        return editor


class TestBlockEditor(TestExecutionPropertiesEditor):
    """Test that the editor for blocks works correctly"""

    editor_klass = BlockEditor
    declaration_field = "blocks"

    @pytest.fixture()
    def properties_editor(self, beat_context, test_prefix):
        environment_model = EnvironmentModel()
        environment_model.setContext(beat_context)

        editor = self.editor_klass("block_name", test_prefix)
        editor.setEnvironmentModel(environment_model)
        return editor


class TestAnalyzerBlockEditor(PropertiesEditorTestMixin):
    """Test that the editor for analyzer blocks works correctly"""

    editor_klass = AnalyzerBlockEditor
    declaration_field = "analyzers"

    @pytest.fixture()
    def properties_editor(self, beat_context, test_prefix):
        environment_model = EnvironmentModel()
        environment_model.setContext(beat_context)

        editor = self.editor_klass("block_name", test_prefix)
        editor.setEnvironmentModel(environment_model)
        return editor


class TestLoopBlockEditor(TestExecutionPropertiesEditor):
    """Test that the editor for the loop blocks works correctly"""

    editor_klass = LoopBlockEditor
    declaration_field = "loops"

    @pytest.fixture()
    def properties_editor(self, beat_context, test_prefix, algorithm_model):
        environment_model = EnvironmentModel()
        environment_model.setContext(beat_context)

        editor = self.editor_klass("block_name", test_prefix)
        editor.setEnvironmentModel(environment_model)
        return editor

    def test_edit_environment(
        self, qtbot, properties_editor, test_prefix, test_experiment, algorithm_model
    ):
        qtbot.addWidget(properties_editor)

        experiment_declaration = get_experiment_declaration(
            test_prefix, test_experiment
        )
        algorithms = experiment_declaration[self.declaration_field]
        first_algorithm = next(iter(algorithms))
        json_reference = algorithms[first_algorithm]

        properties_editor.load(json_reference)

        environment_model = properties_editor.environmentModel()
        environment = environment_model.environment(environment_model.index(1, 0))

        for editor in [
            properties_editor.processor_properties_editor,
            properties_editor.evaluator_properties_editor,
        ]:
            with qtbot.waitSignal(properties_editor.dataChanged):
                combobox = editor.findChild(QComboBox, "environments")
                combobox.setCurrentIndex(1)

        assert properties_editor.dump()[PROCESSOR_PREFIX + "environment"] == environment
        assert properties_editor.dump()[EVALUATOR_PREFIX + "environment"] == environment

    def test_edit_algorithm(
        self, qtbot, properties_editor, test_prefix, test_experiment, algorithm_model
    ):
        qtbot.addWidget(properties_editor)

        experiment_declaration = get_experiment_declaration(
            test_prefix, test_experiment
        )
        algorithms = experiment_declaration[self.declaration_field]
        first_algorithm = next(iter(algorithms))
        json_reference = algorithms[first_algorithm]

        properties_editor.load(json_reference)
        processor_combobox = properties_editor.processor_properties_editor.findChild(
            QComboBox, "algorithms"
        )
        evaluator_combobox = properties_editor.evaluator_properties_editor.findChild(
            QComboBox, "algorithms"
        )

        for combobox in [processor_combobox, evaluator_combobox]:
            with qtbot.waitSignal(properties_editor.dataChanged):
                next_index = combobox.currentIndex() + 1
                if next_index == combobox.count():
                    next_index -= 2
                combobox.setCurrentIndex(next_index)

        assert (
            properties_editor.dump()[PROCESSOR_PREFIX + "algorithm"]
            == processor_combobox.currentText()
        )
        assert (
            properties_editor.dump()[EVALUATOR_PREFIX + "algorithm"]
            == evaluator_combobox.currentText()
        )

    def test_edit_parameter(
        self, qtbot, properties_editor, test_prefix, test_experiment, algorithm_model
    ):
        qtbot.addWidget(properties_editor)

        experiment_declaration = get_experiment_declaration(
            test_prefix, test_experiment
        )
        algorithms = experiment_declaration[self.declaration_field]

        tested = {}

        for name, algorithm in algorithms.items():
            properties_editor.load(algorithm)

            for field_prefix, sub_properties_editor in [
                (PROCESSOR_PREFIX, properties_editor.processor_properties_editor),
                (EVALUATOR_PREFIX, properties_editor.evaluator_properties_editor),
            ]:
                parameters_editors = sub_properties_editor.findChildren(
                    AlgorithmParametersEditor
                )
                for parameters_editor in parameters_editors:
                    if parameters_editor.parameterCount():
                        label = parameters_editor.labelForRow(0)
                        parameter_editor = parameters_editor.editorForRow(0)

                        assert isinstance(parameter_editor, NumpySpinBox)

                        with qtbot.waitSignal(properties_editor.dataChanged):
                            new_value = parameter_editor.value - 1
                            parameter_editor.setValue(new_value)

                        assert properties_editor.dump()[
                            field_prefix + self.parameter_field
                        ] == {label: new_value}
                        tested.update({field_prefix: True})
                        break

        assert tested.get(PROCESSOR_PREFIX, False)
        assert tested.get(EVALUATOR_PREFIX, False)

    def test_edit_parameter_going_back_to_default_value(
        self, qtbot, properties_editor, test_prefix, test_experiment, algorithm_model
    ):
        qtbot.addWidget(properties_editor)

        experiment_declaration = get_experiment_declaration(
            test_prefix, test_experiment
        )
        algorithms = experiment_declaration[self.declaration_field]

        tested = {}

        for name, algorithm in algorithms.items():
            properties_editor.load(algorithm)

            for field_prefix, sub_properties_editor in [
                (PROCESSOR_PREFIX, properties_editor.processor_properties_editor),
                (EVALUATOR_PREFIX, properties_editor.evaluator_properties_editor),
            ]:
                parameter_field = field_prefix + self.parameter_field
                if parameter_field not in algorithm:
                    continue

                parameters_editors = sub_properties_editor.findChildren(
                    AlgorithmParametersEditor
                )
                for parameters_editor in parameters_editors:
                    if parameters_editor.parameterCount():
                        label = parameters_editor.labelForRow(0)
                        parameter_editor = parameters_editor.editorForRow(0)

                        assert isinstance(parameter_editor, NumpySpinBox)

                        with qtbot.waitSignal(properties_editor.dataChanged):
                            new_value = parameter_editor.value - 1
                            parameter_editor.setValue(new_value)

                        with qtbot.waitSignal(properties_editor.dataChanged):
                            new_value = parameter_editor.value + 1
                            parameter_editor.setValue(new_value)

                        assert properties_editor.dump()[parameter_field] == {
                            label: new_value
                        }
                        tested.update({field_prefix: True})
                        break

        assert tested.get(PROCESSOR_PREFIX, False)
        assert tested.get(EVALUATOR_PREFIX, False)

    def test_edit_io_mapping(
        self,
        qtbot,
        monkeypatch,
        properties_editor,
        test_prefix,
        test_experiment,
        algorithm_model,
    ):
        qtbot.addWidget(properties_editor)

        experiment_declaration = get_experiment_declaration(
            test_prefix, test_experiment
        )

        algorithms = experiment_declaration[self.declaration_field]
        first_algorithm = next(iter(algorithms))
        json_reference = algorithms[first_algorithm]

        properties_editor.load(json_reference)

        for field_prefix, sub_properties_editor in [
            (PROCESSOR_PREFIX, properties_editor.processor_properties_editor),
            (EVALUATOR_PREFIX, properties_editor.evaluator_properties_editor),
        ]:
            prefixed_inputs = field_prefix + "inputs"
            prefixed_outputs = field_prefix + "outputs"

            io_mapping_answer = {"inputs": json_reference[prefixed_inputs]}

            for key in io_mapping_answer["inputs"]:
                io_mapping_answer["inputs"] = "changed"

            if prefixed_outputs in json_reference:
                io_mapping_answer["outputs"] = json_reference[prefixed_outputs]
                for key in io_mapping_answer["outputs"]:
                    io_mapping_answer["outputs"] = "changed"

            monkeypatch.setattr(
                IOMapperDialog, "getIOMapping", lambda *args: (True, io_mapping_answer)
            )

            remap_button = sub_properties_editor.findChild(QPushButton, "remap")
            with qtbot.waitSignal(sub_properties_editor.dataChanged):
                qtbot.mouseClick(remap_button, Qt.LeftButton)

            assert (
                properties_editor.dump()[prefixed_inputs] == io_mapping_answer["inputs"]
            )

            if prefixed_outputs in json_reference:
                assert (
                    properties_editor.dump()[prefixed_outputs]
                    == io_mapping_answer["outputs"]
                )


EXP_GLOBALS = {
    "queue": "queue",
    "environment": {"name": "Python 2.7", "version": "1.3.0"},
}

EXP_GLOBALS_PARAMETERS = {
    "v1/integers_add/1": {"offset": 1},
    "user/db_input_loop_evaluator/1": {"threshold": 9},
}


class TestGlobalParametersEditor:
    """Test that the global parameters editor works correctly"""

    @pytest.fixture()
    def exp_globals(self):
        return copy.deepcopy(EXP_GLOBALS)

    @pytest.fixture()
    def exp_globals_parameters(self):
        return copy.deepcopy(EXP_GLOBALS_PARAMETERS)

    @pytest.fixture()
    def gpe_editor(self, beat_context, test_prefix):
        editor = GlobalParametersEditor(test_prefix)
        environment_model = EnvironmentModel()
        environment_model.setContext(beat_context)
        editor.setEnvironmentModel(environment_model)
        return editor

    @pytest.mark.parametrize(
        "parameters",
        [{}, EXP_GLOBALS_PARAMETERS],
        ids=["No parameters", "With Parameters"],
    )
    def test_load_and_dump(self, qtbot, gpe_editor, exp_globals, parameters):
        exp_globals.update(parameters)
        gpe_editor.setup(set(parameters.keys()))
        gpe_editor.load(exp_globals)

        assert gpe_editor.dump() == exp_globals

    def test_add_algorithm(
        self, qtbot, gpe_editor, exp_globals, exp_globals_parameters
    ):
        gpe_editor.load(exp_globals)

        assert gpe_editor.dump() == exp_globals

        gpe_editor.setup(set(exp_globals_parameters.keys()))
        exp_globals.update(exp_globals_parameters)
        assert gpe_editor.dump() == exp_globals

    def test_remove_algorithm(
        self, qtbot, gpe_editor, exp_globals, exp_globals_parameters
    ):
        original_globals = copy.deepcopy(exp_globals)

        exp_globals.update(exp_globals_parameters)
        gpe_editor.setup(set(exp_globals_parameters.keys()))
        gpe_editor.load(exp_globals)

        assert gpe_editor.dump() == exp_globals

        gpe_editor.setup(set())
        assert gpe_editor.dump() == original_globals

    def test_change_environment(self, qtbot, gpe_editor, exp_globals):
        gpe_editor.load(exp_globals)
        with qtbot.waitSignal(gpe_editor.dataChanged):
            index = gpe_editor.environment_combobox.currentIndex()
            gpe_editor.environment_combobox.setCurrentIndex(change_index(index))
        assert gpe_editor.dump() != exp_globals

    def test_change_queue(self, qtbot, gpe_editor, exp_globals):
        gpe_editor.load(exp_globals)
        with qtbot.waitSignal(gpe_editor.dataChanged):
            index = gpe_editor.queue_combobox.currentIndex()
            gpe_editor.queue_combobox.setCurrentIndex(change_index(index))
        assert gpe_editor.dump() != exp_globals


def get_valid_experiments(test_prefix):
    model = AssetModel()
    model.asset_type = AssetType.EXPERIMENT
    model.prefix_path = test_prefix
    model.setLatestOnlyEnabled(False)
    return [
        experiment for experiment in model.stringList() if "errors" not in experiment
    ]


class TestExperimentEditor:
    """Test that the experiment editor works correctly"""

    @pytest.fixture()
    def test_experiment(self):
        return "user/user/single/1/single_add"

    @pytest.fixture()
    def experiment_declaration(self, test_prefix, test_experiment):
        return get_experiment_declaration(test_prefix, test_experiment)

    @pytest.fixture()
    def experiment_editor(self, qtbot, beat_context, experiment_declaration):
        experiment_resources.setContext(beat_context)
        editor = ExperimentEditor()
        editor.set_context(beat_context)
        editor.load_json(experiment_declaration)
        qtbot.addWidget(editor)
        return editor

    @pytest.mark.parametrize("experiment", get_valid_experiments(prefix))
    def test_load_and_dump(self, experiment_editor, test_prefix, experiment):
        experiment_declaration = get_experiment_declaration(test_prefix, experiment)
        experiment_editor.load_json(experiment_declaration)

        assert experiment_editor.dump_json() == experiment_declaration

    def test_change_dataset(self, qtbot, experiment_editor, experiment_declaration):
        dataset_editor = experiment_editor.datasets_widget.widget_list[0]
        dataset_combobox = dataset_editor.dataset_combobox
        with qtbot.waitSignal(experiment_editor.dataChanged):
            dataset_combobox.setCurrentIndex(dataset_combobox.currentIndex() + 1)

        dump = experiment_editor.dump_json()
        assert dump != experiment_declaration
        assert dump["datasets"]["set"]["set"] == dataset_editor.currentSet()

    def test_change_one_algorithm_parameter(
        self, qtbot, experiment_editor, experiment_declaration
    ):
        block_name = None
        parameter_editor = None
        for widget in experiment_editor.blocks_widget.widget_list:
            parameters_editor = widget.properties_editor.parameters_editor
            if parameters_editor.parameterCount():
                block_name = widget.block_name
                parameter_editor = parameters_editor.editorForRow(0)
                break

        assert isinstance(parameter_editor, NumpySpinBox)

        with qtbot.waitSignal(experiment_editor.dataChanged):
            new_value = parameter_editor.value - 1
            parameter_editor.setValue(new_value)

        dump = experiment_editor.dump_json()
        assert dump != experiment_declaration
        assert "parameters" in dump["blocks"][block_name]

    @pytest.mark.parametrize(
        ["widget_attribute", "json_entry"],
        [("blocks_widget", "blocks"), ("analyzers_widget", "analyzers")],
        ids=["Blocks", "Analyzers"],
    )
    def test_change_algorithm_in_blocks(
        self,
        qtbot,
        experiment_editor,
        experiment_declaration,
        widget_attribute,
        json_entry,
    ):
        list_widget = getattr(experiment_editor, widget_attribute)
        block_editor = list_widget.widget_list[0]
        combobox = block_editor.properties_editor.algorithm_combobox
        with qtbot.waitSignal(experiment_editor.dataChanged):
            combobox.setCurrentIndex(combobox.currentIndex() + 1)

        dump = experiment_editor.dump_json()
        assert dump != experiment_declaration
        assert (
            dump[json_entry][block_editor.block_name]["algorithm"]
            == combobox.currentText()
        )

    @pytest.mark.parametrize(
        ["widget_attribute", "json_entry"],
        [("blocks_widget", "blocks"), ("analyzers_widget", "analyzers")],
        ids=["Blocks", "Analyzers"],
    )
    def test_change_environment_in_blocks(
        self,
        qtbot,
        experiment_editor,
        experiment_declaration,
        widget_attribute,
        json_entry,
    ):
        list_widget = getattr(experiment_editor, widget_attribute)
        block_editor = list_widget.widget_list[0]
        properties_editor = block_editor.properties_editor
        combobox = properties_editor.environment_combobox

        with qtbot.waitSignal(experiment_editor.dataChanged):
            index = combobox.currentIndex()
            combobox.setCurrentIndex(change_index(index))

        dump = experiment_editor.dump_json()
        assert dump != experiment_declaration

        model = combobox.model()
        assert dump[json_entry][block_editor.block_name][
            "environment"
        ] == model.environment(model.index(1, 0))

    def test_change_environment_in_globals(
        self, qtbot, experiment_editor, experiment_declaration
    ):
        gpe_editor = experiment_editor.globalparameters_widget
        with qtbot.waitSignal(experiment_editor.dataChanged):
            gpe_editor.environment_combobox.setCurrentIndex(1)

        dump = experiment_editor.dump_json()

        assert dump != experiment_declaration
        model = gpe_editor.environment_combobox.model()
        assert dump["globals"]["environment"] == model.environment(model.index(1, 0))

    def test_no_parameter_in_algorithm_if_same_value_in_globals(
        self, qtbot, experiment_editor, experiment_declaration
    ):
        algorithm_name = None
        block_name = None
        parameter_editor = None
        for block_editor in experiment_editor.blocks_widget.widget_list:
            properties_editor = block_editor.properties_editor
            if properties_editor.parameters_editor.parameterCount():
                block_name = block_editor.block_name
                algorithm_name = properties_editor.parameters_editor.algorithm_name
                parameter_editor = properties_editor.parameters_editor.editorForRow(0)
                break

        assert isinstance(parameter_editor, NumpySpinBox)

        with qtbot.waitSignal(experiment_editor.dataChanged):
            new_value = parameter_editor.value - 1
            parameter_editor.setValue(new_value)

        dump = experiment_editor.dump_json()
        assert dump != experiment_declaration
        assert "parameters" in dump["blocks"][block_name]

        gpe_editor = experiment_editor.globalparameters_widget
        gpe_parameter_editor = None

        for widget in gpe_editor.parameters_editor_listwidget.widget_list:
            if widget.editor.algorithm_name == algorithm_name:
                gpe_parameter_editor = widget.editor.editorForRow(0)
                break

        assert isinstance(gpe_parameter_editor, NumpySpinBox)
        gpe_parameter_editor.setValue(parameter_editor.value)
        assert gpe_parameter_editor.value == parameter_editor.value

        dump = experiment_editor.dump_json()
        assert dump != experiment_declaration
        assert "parameters" not in dump["blocks"][block_name]

    def test_no_environment_in_algorithm_if_same_value_in_globals(
        self, qtbot, experiment_editor, experiment_declaration
    ):
        block_editor = experiment_editor.blocks_widget.widget_list[0]
        properties_editor = block_editor.properties_editor
        with qtbot.waitSignal(experiment_editor.dataChanged):
            properties_editor.environment_combobox.setCurrentIndex(1)

        dump = experiment_editor.dump_json()

        assert dump != experiment_declaration
        assert "environment" in dump["blocks"][block_editor.block_name]

        gpe_editor = experiment_editor.globalparameters_widget
        with qtbot.waitSignal(experiment_editor.dataChanged):
            gpe_editor.environment_combobox.setCurrentIndex(1)

        dump = experiment_editor.dump_json()
        assert dump != experiment_declaration
        assert "environment" not in dump["blocks"][block_editor.block_name]

    def test_showing_error(self, qtbot, experiment_editor, experiment_declaration):
        experiment_editor.load_json(experiment_declaration)

        ERROR_BLOCK = "echo"
        errors = {ERROR_BLOCK: ["show this error"]}

        experiment_editor.setBlockErrors(errors)

        editor = experiment_editor.findEditor(ERROR_BLOCK)
        assert editor.error_label.toolTip() == "show this error"

        experiment_editor.clearBlockErrors()
        assert editor.error_label.toolTip() == ""
