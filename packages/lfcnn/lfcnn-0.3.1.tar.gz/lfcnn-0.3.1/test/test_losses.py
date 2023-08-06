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

from lfcnn import losses

ALL_LOSSES = [losses.dummy,
              losses.mean_absolute_error,
              losses.mean_squared_error,
              losses.huber_loss,
              losses.pseudo_huber_loss,
              losses.total_variation,
              losses.psnr, losses.psnr_clipped,
              losses.cosine_proximity, losses.normalized_cosine_proximity,
              losses.spectral_information_divergence,
              losses.bad_pix_01, losses.bad_pix_03, losses.bad_pix_07]

SSIM_LOSSES = [losses.structural_similarity,
               losses.normalized_structural_similarity,
               losses.multiscale_structural_similarity,
               losses.normalized_multiscale_structural_similarity]

LF_LOSSES = [losses.mean_absolute_error,
             losses.mean_squared_error,
             losses.huber_loss,
             losses.pseudo_huber_loss,
             losses.psnr, losses.psnr_clipped,
             losses.cosine_proximity, losses.normalized_cosine_proximity,
             losses.spectral_information_divergence]


def test_shape_ssim():
    """Test that all losses return a single float value (reduce batch mean)
    """
    # MS SSIM needs larger shape
    for shape in [(10, 256, 256, 3), (10, 256, 256, 1)]:
        y_true = K.variable(np.random.random(shape))
        y_pred = K.variable(np.random.random(shape))
        for loss in SSIM_LOSSES:
            res = loss(y_true, y_pred)
            # Always returns single float value
            assert res.ndim == 0


def test_shape_images():
    """Test that all losses return a single float value (reduce batch mean)
    """
    for shape in [(10, 5, 5), (10, 5, 5, 3)]:
        y_true = K.variable(np.random.random(shape))
        y_pred = K.variable(np.random.random(shape))
        for loss in ALL_LOSSES:
            res = loss(y_true, y_pred)
            # Always returns single float value
            assert res.ndim == 0


def test_shape_lightfield():
    """Test that all losses return a single float value (reduce batch mean)
    """
    for shape in [(10, 9, 9, 5, 5, 3), (10, 9, 5, 5, 3)]:
        y_true = K.variable(np.random.random(shape))
        y_pred = K.variable(np.random.random(shape))
        for loss in LF_LOSSES:
            res = loss(y_true, y_pred)
            # Always returns single float value
            assert res.ndim == 0


def test_mae():
    loss_inst = losses.MeanAbsoluteError()
    loss = losses.mean_absolute_error

    # Identical true, pred
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = y_true.copy()

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert K.eval(loss(y_true, y_pred)) == 0
    assert K.eval(loss_inst.call(y_true, y_pred)) == 0

    # Opposite true, pred
    y_true = np.ones((10, 3, 3, 7))
    y_pred = np.zeros((10, 3, 3, 7))

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert K.eval(loss(y_true, y_pred)) == 1
    assert K.eval(loss_inst.call(y_true, y_pred)) == 1

    # 2 batches, one identical, one opposite
    y_true = np.zeros((2, 1, 1, 1))
    y_true[1, ...] = 1
    y_pred = np.zeros((2, 1, 1, 1))

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert K.eval(loss(y_true, y_pred)) == 0.5
    assert K.eval(loss_inst.call(y_true, y_pred)) == 0.5

    return


def test_mse():
    loss_inst = losses.MeanSquaredError()
    loss = losses.mean_squared_error

    # Identical true, pred
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = y_true.copy()

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert K.eval(loss(y_true, y_pred)) == 0
    assert K.eval(loss_inst.call(y_true, y_pred)) == 0

    # Opposite true, pred
    y_true = np.ones((10, 3, 3, 7))
    y_pred = np.zeros((10, 3, 3, 7))

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert K.eval(loss(y_true, y_pred)) == 1
    assert K.eval(loss_inst.call(y_true, y_pred)) == 1

    # 2 batches, one identical, one opposite
    y_true = np.zeros((2, 1, 1, 1))
    y_true[1, ...] = 1
    y_pred = np.zeros((2, 1, 1, 1))

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert K.eval(loss(y_true, y_pred)) == 0.5
    assert K.eval(loss_inst.call(y_true, y_pred)) == 0.5

    return


def test_huber():
    for ver in ['fcnn', 'keras']:
        delta = 1
        loss_inst = losses.Huber(delta=delta, ver=ver)
        loss = losses.huber_loss

        # Identical true, pred
        y_true = np.random.rand(10, 3, 3, 7)
        y_pred = y_true.copy()

        y_true = convert_to_tensor(y_true)
        y_pred = convert_to_tensor(y_pred)
        assert K.eval(loss(y_true, y_pred, delta=delta, ver=ver)) == 0
        assert K.eval(loss_inst.call(y_true, y_pred)) == 0

    # Test Keras compatible version
    delta = 1
    loss_inst = losses.Huber(delta=delta, ver='keras')
    loss = losses.huber_loss

    # Opposite true, pred
    y_true = np.ones((10, 3, 3, 7))
    y_pred = np.zeros((10, 3, 3, 7))

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert K.eval(loss(y_true, y_pred, delta=delta, ver='keras')) == 0.5
    assert K.eval(loss_inst.call(y_true, y_pred)) == 0.5

    # 2 batches, one identical, one opposite
    y_true = np.zeros((2, 1, 1, 1))
    y_true[1, ...] = 1
    y_pred = np.zeros((2, 1, 1, 1))

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert K.eval(loss(y_true, y_pred, delta=delta, ver='keras')) == 0.25
    assert K.eval(loss_inst.call(y_true, y_pred)) == 0.25

    # Test scaled version
    delta = 1
    loss_inst = losses.Huber(delta=delta)
    loss = losses.huber_loss

    # Opposite true, pred
    y_true = np.ones((10, 3, 3, 7))
    y_pred = np.zeros((10, 3, 3, 7))

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert K.eval(loss(y_true, y_pred, delta=delta)) == 1
    assert K.eval(loss_inst.call(y_true, y_pred)) == 1

    # 2 batches, one identical, one opposite
    y_true = np.zeros((2, 1, 1, 1))
    y_true[1, ...] = 1
    y_pred = np.zeros((2, 1, 1, 1))

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert K.eval(loss(y_true, y_pred, delta=delta)) == 0.5
    assert K.eval(loss_inst.call(y_true, y_pred)) == 0.5

    return


def test_pseudo_huber():
    for ver in ['fcnn', 'keras']:
        delta = 1
        loss_inst = losses.PseudoHuber(delta=delta, ver=ver)
        loss = losses.pseudo_huber_loss

        # Identical true, pred
        y_true = np.random.rand(10, 3, 3, 7)
        y_pred = y_true.copy()

        y_true = convert_to_tensor(y_true)
        y_pred = convert_to_tensor(y_pred)
        abs = 1e-4
        assert approx(K.eval(loss(y_true, y_pred, delta=delta, ver=ver)), abs=1e-6) == 0
        assert approx(K.eval(loss_inst.call(y_true, y_pred)), abs=1e-6) == 0

    delta = 1
    loss_inst = losses.PseudoHuber(delta=delta, ver='keras')
    loss = losses.pseudo_huber_loss

    # Opposite true, pred
    y_true = convert_to_tensor(np.ones((10, 3, 3, 7)))
    y_pred = convert_to_tensor(np.zeros((10, 3, 3, 7)))

    assert approx(K.eval(loss(y_true, y_pred, delta=delta, ver='keras')), abs=abs) == 0.4142
    assert approx(K.eval(loss_inst.call(y_true, y_pred)), abs=abs) == 0.4142

    # 2 batches, one identical, one opposite
    y_true = np.zeros((2, 1, 1, 1))
    y_true[1, ...] = 1
    y_pred = np.zeros((2, 1, 1, 1))

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert approx(K.eval(loss(y_true, y_pred, delta=delta, ver='keras')), abs=abs) == 0.5*0.4142
    assert approx(K.eval(loss_inst.call(y_true, y_pred)), abs=abs) == 0.5*0.4142

    delta = 1
    loss_inst = losses.PseudoHuber(delta=delta, ver='lfcnn')
    loss = losses.pseudo_huber_loss

    # Opposite true, pred
    y_true = convert_to_tensor(np.ones((10, 3, 3, 7)))
    y_pred = convert_to_tensor(np.zeros((10, 3, 3, 7)))

    assert approx(K.eval(loss(y_true, y_pred, delta=delta, ver='lfcnn')), abs=abs) == 2*0.4142
    assert approx(K.eval(loss_inst.call(y_true, y_pred)), abs=abs) == 2*0.4142

    # 2 batches, one identical, one opposite
    y_true = np.zeros((2, 1, 1, 1))
    y_true[1, ...] = 1
    y_pred = np.zeros((2, 1, 1, 1))

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert approx(K.eval(loss(y_true, y_pred, delta=delta, ver='lfcnn')), abs=abs) == 0.4142
    assert approx(K.eval(loss_inst.call(y_true, y_pred)), abs=abs) == 0.4142

    return


def test_total_variation():
    loss_inst = losses.TotalVariation()
    loss = losses.total_variation

    # y_true is ignored
    y_true = K.variable(np.random.rand(10, 3, 3, 3))

    for c in [0, 0.25, 0.5, 1]:
        y = K.variable(c*np.ones((10, 3, 3, 3)))
        assert K.eval(loss(y_true, y)) == 0
        assert K.eval(loss_inst.call(y_true, y)) == 0

    y = np.zeros((5, 10, 10, 1))
    y[:, 5:, 5:] = 1
    y = K.variable(y)
    assert K.eval(loss(y_true, y)) == 10
    assert K.eval(loss_inst.call(y_true, y)) == 10

    y = np.zeros((10, 10, 3))
    y[5:, 5:, :] = 1
    y = K.variable(y)
    assert K.eval(loss(y_true, y)) == 30
    assert K.eval(loss_inst.call(y_true, y)) == 30

    y = np.zeros((5, 10, 10, 3))
    y[:, 5:, 5:, :] = 1
    y = K.variable(y)
    assert K.eval(loss(y_true, y)) == 30
    assert K.eval(loss_inst.call(y_true, y)) == 30

    return


def test_cosine_proximity():

    loss_inst = losses.CosineProximity()
    loss = losses.cosine_proximity

    # Identical true, pred, scaling invariant, 0 degrees
    for c in [0.5, 1, 1.5]:
        y_true = np.random.rand(10, 3, 3, 7)
        y_pred = c*y_true.copy()

        y_true = K.variable(y_true)
        y_pred = K.variable(y_pred)
        assert K.eval(loss(y_true, y_pred)) == 1
        assert K.eval(loss_inst.call(y_true, y_pred)) == 1

    # Opposite true, pred, 90 degrees
    y_true = np.zeros((10, 3, 3, 7))
    y_pred = np.ones((10, 3, 3, 7))

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert K.eval(loss(y_true, y_pred)) == 0
    assert K.eval(loss_inst.call(y_true, y_pred)) == 0

    # 45 degrees true, pred
    y_true = np.asarray([1, 0])
    y_pred = np.asarray([1, 1])

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert approx(K.eval(loss(y_true, y_pred)), abs=1e-4) == np.cos(0.25*np.pi)
    assert approx(K.eval(loss_inst.call(y_true, y_pred)), abs=1e-4) == np.cos(0.25*np.pi)

    return


def test_normalized_cosine_proximity():

    loss_inst = losses.NormalizedCosineProximity()
    loss = losses.normalized_cosine_proximity

    # Identical true, pred, scaling invariant, 0 degrees
    for c in [0.5, 1, 1.5]:
        y_true = np.random.rand(10, 3, 3, 7)
        y_pred = c*y_true.copy()

        y_true = K.variable(y_true)
        y_pred = K.variable(y_pred)
        assert K.eval(loss(y_true, y_pred)) == 0
        assert K.eval(loss_inst.call(y_true, y_pred)) == 0

    # Opposite true, pred, 90 degrees
    y_true = np.zeros((10, 3, 3, 7))
    y_pred = np.ones((10, 3, 3, 7))

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert K.eval(loss(y_true, y_pred)) == 0.5
    assert K.eval(loss_inst.call(y_true, y_pred)) == 0.5

    # Identical true, pred, scaling invariant, 180 degrees
    for c in [-0.5, -1, -1.5]:
        y_true = np.random.rand(10, 3, 3, 7)
        y_pred = c*y_true.copy()

        y_true = K.variable(y_true)
        y_pred = K.variable(y_pred)
        assert K.eval(loss(y_true, y_pred)) == 1
        assert K.eval(loss_inst.call(y_true, y_pred)) == 1

    return


def test_spectral_information_divergence():

    loss_inst = losses.SpectralInformationDivergence()
    loss = losses.spectral_information_divergence

    # Opposite true, pred, 90 degrees
    y_true = np.zeros((10, 3, 3, 7))
    y_pred = np.ones((10, 3, 3, 7))

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert K.eval(loss(y_true, y_pred)) == 0
    assert K.eval(loss_inst.call(y_true, y_pred)) == 0

    # Identical true, pred, scaling invariant, 0 degrees
    for c in [0.25, 0.5, 1]:
        y_true = np.random.rand(10, 3, 3, 7)
        y_pred = c*y_true.copy()

        y_true = K.variable(y_true)
        y_pred = K.variable(y_pred)
        assert K.eval(loss(y_true, y_pred)) == 0
        assert K.eval(loss_inst.call(y_true, y_pred)) == 0

    return


def test_psnr():
    loss = losses.psnr

    # Opposite true, pred, 90 degrees
    y_true = np.zeros((10, 3, 3, 7))
    y_pred = np.ones((10, 3, 3, 7))

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert approx(K.eval(loss(y_true, y_pred)), abs=1e-4) == 0

    # 20 dB
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = y_true.copy() - 0.1

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert approx(K.eval(loss(y_true, y_pred)), abs=1e-2) == 20

    # 40 dB
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = y_true.copy() - 0.01

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert approx(K.eval(loss(y_true, y_pred)), abs=1e-2) == 40

    # 60 dB
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = y_true.copy() - 0.001

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert approx(K.eval(loss(y_true, y_pred)), abs=2) == 60

    return


def test_psnr_clipped():
    loss = losses.psnr_clipped

    # Opposite true, pred, 90 degrees
    y_true = np.zeros((10, 3, 3, 7))
    y_pred = np.ones((10, 3, 3, 7))

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert approx(K.eval(loss(y_true, y_pred)), abs=1e-4) == 0

    # 20 dB
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = y_true.copy() - 0.1

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert approx(K.eval(loss(y_true, y_pred)), abs=1e-2) == K.eval(losses.psnr(y_true, K.clip(y_pred, 0, 1)))

    return


def test_mae_clipped():
    loss = losses.mae_clipped

    # Opposite true, pred, 90 degrees
    y_true = np.zeros((10, 3, 3, 7))
    y_pred = np.ones((10, 3, 3, 7))

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert approx(K.eval(loss(y_true, y_pred)), abs=1e-4) == 1

    # Identical true, pred, 90 degrees
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = y_true.copy()

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert approx(K.eval(loss(y_true, y_pred)), abs=1e-4) == 0

    # Random
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = np.random.rand(10, 3, 3, 7)

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert approx(K.eval(loss(y_true, y_pred)), abs=1e-2) == K.eval(losses.mae(y_true, K.clip(y_pred, 0, 1)))

    return


def test_mse_clipped():
    loss = losses.mse_clipped

    # Opposite true, pred, 90 degrees
    y_true = np.zeros((10, 3, 3, 7))
    y_pred = np.ones((10, 3, 3, 7))

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert approx(K.eval(loss(y_true, y_pred)), abs=1e-4) == 1

    # Identical true, pred, 90 degrees
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = y_true.copy()

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert approx(K.eval(loss(y_true, y_pred)), abs=1e-4) == 0

    # Random
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = np.random.rand(10, 3, 3, 7)

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert approx(K.eval(loss(y_true, y_pred)), abs=1e-2) == K.eval(losses.mse(y_true, K.clip(y_pred, 0, 1)))

    return


def test_bad_pix():

    for c in [0, 0.011, 0.033, 0.077]:
        # Identical values, manipulate singles
        y_true = np.random.rand(1, 10, 10)
        y_pred = y_true.copy()
        y_pred[0, 0, 0] += c

        y_true = K.variable(y_true)
        y_pred = K.variable(y_pred)

        if c > 0.01:
            assert K.eval(losses.bad_pix_01(y_true, y_pred)) == 1.0
        else:
            assert K.eval(losses.bad_pix_01(y_true, y_pred)) == 0.0
        if c > 0.03:
            assert K.eval(losses.bad_pix_03(y_true, y_pred)) == 1.0
        else:
            assert K.eval(losses.bad_pix_03(y_true, y_pred)) == 0.0
        if c > 0.07:
            assert K.eval(losses.bad_pix_07(y_true, y_pred)) == 1.0
        else:
            assert K.eval(losses.bad_pix_07(y_true, y_pred)) == 0.0

        y_true = np.random.rand(1, 10, 10)
        y_pred = y_true.copy()
        y_pred[0, 0, 0] += c
        y_pred[0, 5, 5] += c

        y_true = K.variable(y_true)
        y_pred = K.variable(y_pred)

        if c > 0.01:
            assert K.eval(losses.bad_pix_01(y_true, y_pred)) == 2.0
        else:
            assert K.eval(losses.bad_pix_01(y_true, y_pred)) == 0.0
        if c > 0.03:
            assert K.eval(losses.bad_pix_03(y_true, y_pred)) == 2.0
        else:
            assert K.eval(losses.bad_pix_03(y_true, y_pred)) == 0.0
        if c > 0.07:
            assert K.eval(losses.bad_pix_07(y_true, y_pred)) == 2.0
        else:
            assert K.eval(losses.bad_pix_07(y_true, y_pred)) == 0.0

        y_true = np.random.rand(1, 10, 10)
        y_pred = y_true.copy()
        y_pred += c

        y_true = K.variable(y_true)
        y_pred = K.variable(y_pred)

        if c > 0.01:
            assert K.eval(losses.bad_pix_01(y_true, y_pred)) == 100.0
        else:
            assert K.eval(losses.bad_pix_01(y_true, y_pred)) == 0.0
        if c > 0.03:
            assert K.eval(losses.bad_pix_03(y_true, y_pred)) == 100.0
        else:
            assert K.eval(losses.bad_pix_03(y_true, y_pred)) == 0.0
        if c > 0.07:
            assert K.eval(losses.bad_pix_07(y_true, y_pred)) == 100.0
        else:
            assert K.eval(losses.bad_pix_07(y_true, y_pred)) == 0.0

    return


def test_dummy():
    loss_inst = losses.Dummy()
    loss = losses.dummy

    # Identical true, pred
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = np.random.rand(10, 3, 3, 7)

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert K.eval(loss(y_true, y_pred)) == 1.0
    assert K.eval(loss_inst.call(y_true, y_pred)) == 1.0

    return
