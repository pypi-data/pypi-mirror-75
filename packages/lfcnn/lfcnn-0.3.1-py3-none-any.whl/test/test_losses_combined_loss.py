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


"""Test lfcnn.losses
"""
# Set CPU as device:
from lfcnn.utils.tf_utils import use_cpu
use_cpu()

from pytest import approx

from tensorflow import convert_to_tensor
import tensorflow.keras.backend as K
import numpy as np

from lfcnn.losses.combined_losses import CenterLoss, DisparityLoss
from lfcnn.losses.combined_losses import center_loss, disparity_loss

ALL_LOSSES = [center_loss, disparity_loss]


def test_shape_center_loss():
    """Test that center loss returns a single float value (reduce batch mean)
    """
    for shape in [(10, 32, 32, 3), (10, 32, 32, 13)]:
        y_true = K.variable(np.random.random(shape))
        y_pred = K.variable(np.random.random(shape))
        res = center_loss(y_true, y_pred,
                          mu=0.5, gamma=0.25,
                          power_factors=[1, 1, 1], filter_size=3, k1=0.1, k2=0.1)
        # Always returns single float value
        assert res.ndim == 0


def test_shape_disparity_loss():
    """Test that center loss returns a single float value (reduce batch mean)
    """
    shape = (10, 32, 32, 1)
    y_true = K.variable(np.random.random(shape))
    y_pred = K.variable(np.random.random(shape))
    res = disparity_loss(y_true, y_pred, mu=0.5)
    # Always returns single float value
    assert res.ndim == 0


def test_center_loss():
    """Test that all losses return a single float value (reduce batch mean)
    """
    mu = 0.25
    gamma = 0.5
    power_factors = (0.5, 0.3, 0.2)
    filter_size = 3
    k1 = 0.03
    k2 = 0.09

    loss_inst = CenterLoss(mu, gamma, power_factors, filter_size, k1, k2)
    loss = center_loss

    # Identical true, pred
    y_true = np.random.rand(10, 32, 32, 3)
    y_pred = y_true.copy()

    y_true = convert_to_tensor(y_true, dtype=K.floatx())
    y_pred = convert_to_tensor(y_pred, dtype=K.floatx())
    assert approx(K.eval(loss(y_true, y_pred, mu, gamma, power_factors, filter_size, k1, k2)), abs=1e-6) == 0
    assert approx(K.eval(loss_inst.call(y_true, y_pred)), abs=1e-6) == 0


def test_disparity_loss():
    """Test that all losses return a single float value (reduce batch mean)
    """
    loss_inst = CenterLoss()
    loss = disparity_loss

    # Identical true, pred
    y_true = np.random.rand(10, 32, 32, 3)
    y_pred = y_true.copy()

    y_true = convert_to_tensor(y_true, dtype=K.floatx())
    y_pred = convert_to_tensor(y_pred, dtype=K.floatx())
    assert approx(K.eval(loss(y_true, y_pred)), abs=1e-6) == 0
    assert approx(K.eval(loss_inst.call(y_true, y_pred)), abs=1e-6) == 0
