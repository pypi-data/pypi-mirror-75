# Copyright (C) 2020  The LFCNN Authors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""Test lfcnn.callbacks
"""
# Set CPU as device:
from lfcnn.utils.tf_utils import use_cpu
use_cpu()

from pytest import approx, raises

from tensorflow.keras.backend import clear_session
from tensorflow.keras import optimizers

import numpy as np

from lfcnn.losses import MeanSquaredError
from lfcnn.metrics import get_lf_metrics
from lfcnn.models.autoencoder import Dummy

from lfcnn import callbacks
from lfcnn.callbacks.lr_finder import LearningRateFinder
from lfcnn.callbacks.lr_schedules import PolynomialDecay, LinearDecay, ExponentialDecay
from lfcnn.callbacks.lr_schedules import SigmoidDecay, StepDecay
from lfcnn.callbacks.cyclic_learning import OneCycle, OneCycleCosine
from lfcnn.callbacks.cyclic_learning import OneCycleMomentum, OneCycleCosineMomentum
from lfcnn.callbacks.sacred import SacredMetricLogger, SacredTimeLogger, SacredEpochLogger, SacredLearningRateLogger


ALL_CALLBACKS = {
    "SacredMetricLogger": SacredMetricLogger,
    "SacredTimeLogger": SacredTimeLogger,
    "SacredEpochLogger": SacredEpochLogger,
    "SacredLearningRateLogger": SacredLearningRateLogger,
    "PolynomialDecay": PolynomialDecay,
    "LinearDecay": LinearDecay,
    "ExponentialDecay": ExponentialDecay,
    "SigmoidDecay": SigmoidDecay,
    "StepDecay": StepDecay,
    "OneCycle": OneCycle,
    "OneCycleMomentum": OneCycleMomentum,
    "OneCycleCosine": OneCycleCosine,
    "OneCycleCosineMomentum":OneCycleCosineMomentum,
    "LearningRateFinder": LearningRateFinder,
}


def test_getter():

    for callback in ALL_CALLBACKS:
        res = callbacks.get(callback)
        assert res == ALL_CALLBACKS[callback]

    # Check nonsense
    with raises(ValueError) as e:
        _ = callbacks.get("nonsense")
    assert "Unknown callback" in str(e)

    return
