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


from ..backend.asset import Asset
from ..backend.asset import AssetType
from ..backend.experimentmodel import ExperimentModel


class TestExperimentModeling:
    """Test that the experiment modeling works correctly"""

    def test_model_load(self, test_prefix):
        experiment = Asset(
            test_prefix, AssetType.EXPERIMENT, "user/user/two_loops/1/two_loops"
        )
        experiment_model = ExperimentModel()
        experiment_model.load_experiment(experiment)
        error_list = experiment_model.check_block("offsetter_for_loop_evaluator")
        assert len(error_list) == 0

        error_map = experiment_model.check_all_blocks()
        assert len(error_map) == 0

    def test_error(self, test_prefix):
        experiment = Asset(
            test_prefix, AssetType.EXPERIMENT, "user/user/two_loops/1/two_loops"
        )
        experiment_model = ExperimentModel()
        experiment_model.load_experiment(experiment)
        configuration = {
            "algorithm": "user/string_offsetter/1",
            "inputs": {"in_data": "in"},
            "outputs": {"out_data": "out"},
        }
        BLOCK_TO_CHANGE = "offsetter_for_loop_evaluator"
        experiment_model.update_block(BLOCK_TO_CHANGE, configuration)

        error_list = experiment_model.check_block(BLOCK_TO_CHANGE)
        assert len(error_list) > 0

        error_map = experiment_model.check_all_blocks()
        assert len(error_map) > 0
        assert BLOCK_TO_CHANGE in error_map

    def test_with_empty_blocks(self, test_prefix):
        experiment = Asset(
            test_prefix, AssetType.EXPERIMENT, "errors/user/two_loops/1/empty_blocks"
        )

        experiment_model = ExperimentModel()
        experiment_model.load_experiment(experiment)
        error_map = experiment_model.check_all_blocks()
        assert len(error_map) == 0
