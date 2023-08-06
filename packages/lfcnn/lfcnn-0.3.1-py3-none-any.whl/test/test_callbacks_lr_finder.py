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


"""Test lfcnn.callbacks.cyclic_learning
"""
# Set CPU as device:
from lfcnn.utils.tf_utils import use_cpu
use_cpu()

from pytest import approx, raises

from tensorflow import keras
from tensorflow.keras.backend import clear_session
import numpy as np

from lfcnn import callbacks
from lfcnn.models.autoencoder import Dummy
from lfcnn.losses import MeanSquaredError
from lfcnn.metrics import get_lf_metrics


def get_model_kwargs(cb=[]):
    optimizer = keras.optimizers.SGD(learning_rate=0.1)
    loss = dict(light_field=MeanSquaredError())
    metrics = dict(light_field=get_lf_metrics())

    model_kwargs = dict(
        optimizer=optimizer,
        loss=loss,
        metrics=metrics,
        callbacks=cb
    )

    return model_kwargs


def get_train_kwargs(generated_shape):
    dat = np.random.rand(256, 9, 9, 32, 32, 3)
    lbl = np.random.rand(256, 32, 32)
    data = dict(data=dat, disp=lbl)
    dat = np.random.rand(256, 9, 9, 32, 32, 3)
    lbl = np.random.rand(256, 32, 32)
    valid_data = dict(data=dat, disp=lbl)

    train_kwargs = dict(data=data,
                        valid_data=valid_data,
                        data_key="data",
                        label_keys="disp",
                        augmented_shape=(9, 9, 32, 32, 3),
                        generated_shape=generated_shape,
                        batch_size=1,
                        epochs=1,
                        verbose=0
                        )

    return train_kwargs


def test_lr_finder():

    lr_min = 1e-4
    lr_max = 1e0
    num_batches = 256

    # Test LrFinder with linear sweep
    lrfinder = callbacks.LearningRateFinder(lr_min=lr_min, lr_max=lr_max,
                                            num_batches=num_batches, sweep="linear")
    lr_gt = np.linspace(lr_min, lr_max, num_batches, endpoint=True)

    model_kwargs = get_model_kwargs(cb=[lrfinder])
    model = Dummy(**model_kwargs)

    train_kwargs = get_train_kwargs((32, 32, 9 * 9 * 3))
    model.train(**train_kwargs)

    assert (len(lrfinder.losses)) == 256
    assert (len(lrfinder.avg_losses)) == 256
    assert (len(lrfinder.mses)) == 256
    assert (len(lrfinder.avg_mses)) == 256
    assert approx(np.min(lrfinder.lrs)) == lr_min
    assert approx(np.max(lrfinder.lrs)) == lr_max
    assert np.allclose(lrfinder.lrs, lr_gt)
    clear_session()

    # Test LrFinder with exponential sweep
    lrfinder = callbacks.LearningRateFinder(lr_min=lr_min, lr_max=lr_max,
                                            num_batches=num_batches,
                                            sweep="exponential")
    lr_gt = np.geomspace(lr_min, lr_max, num_batches, endpoint=True)

    model_kwargs = get_model_kwargs(cb=[lrfinder])
    model = Dummy(**model_kwargs)

    train_kwargs = get_train_kwargs((32, 32, 9 * 9 * 3))
    model.train(**train_kwargs)

    assert (len(lrfinder.losses)) == 256
    assert (len(lrfinder.avg_losses)) == 256
    assert approx(np.min(lrfinder.lrs)) == lr_min
    assert approx(np.max(lrfinder.lrs)) == lr_max
    assert np.allclose(lrfinder.lrs, lr_gt)
    clear_session()

    # Test invalid sweep
    with raises(ValueError) as e:
        callbacks.LearningRateFinder(lr_min=lr_min, lr_max=lr_max,
                                     num_batches=num_batches,
                                     sweep="nonsense")
    assert "Unknown sweep" in str(e)

    clear_session()

    return
