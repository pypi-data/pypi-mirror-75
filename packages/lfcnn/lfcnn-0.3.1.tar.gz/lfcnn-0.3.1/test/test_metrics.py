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


"""Test lfcnn.metrics
"""
# Set CPU as device:
from lfcnn.utils.tf_utils import use_cpu
use_cpu()

import tensorflow.keras.backend as K
import numpy as np

from lfcnn import metrics

ALL_METRICS = [metrics.MeanAbsoluteError,
               metrics.MeanSquaredError,
               metrics.TotalVariation,
               metrics.CosineProximity,
               metrics.SpectralInformationDivergence,
               metrics.PSNR,
               metrics.BadPix01,
               metrics.BadPix03,
               metrics.BadPix07]

SSIM_METRICS = [metrics.StructuralSimilarity,
                metrics.MultiScaleStructuralSimilarity]

LF_METRICS = [metrics.MeanAbsoluteError,
              metrics.MeanSquaredError,
              metrics.CosineProximity,
              metrics.SpectralInformationDivergence,
              metrics.PSNR]


def test_shape_ssim():
    """Test that all metrics return a single float value (reduce batch mean)
    """
    # MS SSIM needs larger shape
    for shape in [(10, 256, 256, 3), (10, 256, 256, 1)]:
        y_true = K.variable(np.random.random(shape))
        y_pred = K.variable(np.random.random(shape))
        for metric_constr in SSIM_METRICS:
            metric = metric_constr()
            metric.update_state(y_true, y_pred)
            res = metric.result()
            # Always returns single float value
            assert res.ndim == 0


def test_shape_images():
    """Test that all metrics return a single float value (reduce batch mean)
    """
    for shape in [(10, 5, 5), (10, 5, 5, 3)]:
        y_true = K.variable(np.random.random(shape))
        y_pred = K.variable(np.random.random(shape))
        for metric_constr in ALL_METRICS:
            metric = metric_constr()
            metric.update_state(y_true, y_pred)
            res = metric.result()
            # Always returns single float value
            assert res.ndim == 0


def test_shape_lightfield():
    """Test that all metrics return a single float value (reduce batch mean)
    """
    for shape in [(10, 9, 9, 5, 5, 3), (10, 9, 5, 5, 3)]:
        y_true = K.variable(np.random.random(shape))
        y_pred = K.variable(np.random.random(shape))
        for metric_constr in LF_METRICS:
            metric = metric_constr()
            metric.update_state(y_true, y_pred)
            res = metric.result()
            # Always returns single float value
            assert res.ndim == 0
