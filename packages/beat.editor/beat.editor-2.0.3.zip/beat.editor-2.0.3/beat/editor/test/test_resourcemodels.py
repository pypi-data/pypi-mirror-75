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

import pytest

from PyQt5.QtSql import QSqlQuery
from PyQt5.QtSql import QSqlTableModel

from beat.backend.python.algorithm import Algorithm

from ..backend.resourcemodels import AlgorithmResourceModel
from ..backend.resourcemodels import DatasetResourceModel
from ..backend.resourcemodels import ExperimentResources

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


class TestDatasetResourceModel:
    """Test the model used to generate suitable dataset selections"""

    @pytest.fixture
    def prefix_model(self, beat_context):
        return ExperimentResources(beat_context)

    def test_default(self, prefix_model):
        dataset_model = DatasetResourceModel()

        query = QSqlQuery()
        assert query.exec_("SELECT COUNT(name) AS cnt FROM datasets")

        query.next()

        assert dataset_model.rowCount() == query.value("cnt")

    def test_output_count(self, prefix_model):
        dataset_model = DatasetResourceModel()
        dataset_model.setOutputCount(2)

        query = QSqlQuery()
        assert query.exec_("SELECT COUNT(name) AS cnt FROM datasets WHERE outputs='2'")

        query.next()

        assert dataset_model.rowCount() == query.value("cnt")
