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


"""Test lfcnn.models.center_and_disparity
"""
# Set CPU as device:
from lfcnn.utils.tf_utils import use_cpu
use_cpu()
# disable_eager()

from pytest import raises

import numpy as np

from tensorflow.keras.backend import clear_session
from tensorflow.keras import optimizers
from lfcnn.losses import MeanSquaredError
from lfcnn.metrics import get_disparity_metrics, get_central_metrics_small

from lfcnn.models.center_and_disparity import get
from lfcnn.models.center_and_disparity import Conv3dDecode3d, Conv3dDecode2d, Dummy

ALL_CENTER_AND_DISP_MODELS = {
    "Dummy": Dummy,
    "Conv3dDecode3d": Conv3dDecode3d,
    "Conv3dDecode2d": Conv3dDecode2d
}


def test_getter():

    for model_name in ALL_CENTER_AND_DISP_MODELS:
        res = get(model_name)
        assert res == ALL_CENTER_AND_DISP_MODELS[model_name]

    # Check nonsense
    with raises(ValueError) as e:
        _ = get("nonsense")
    assert "Unknown central view and disparity estimator model" in str(e)

    return


def get_model_kwargs():
    optimizer = optimizers.SGD(learning_rate=0.1)
    loss = dict(central_view=MeanSquaredError(), disparity=MeanSquaredError())
    metrics = dict(central_view=get_central_metrics_small(), disparity=get_disparity_metrics())

    model_kwargs = dict(
        optimizer=optimizer,
        loss=loss,
        metrics=metrics,
        callbacks=[]
    )

    return model_kwargs


def get_train_kwargs(generated_shape, channels=3):
    dat = np.random.rand(8, 9, 9, 32, 32, channels)
    lbl = np.random.rand(8, 32, 32)
    data = dict(data=dat, disp=lbl)
    dat = np.random.rand(8, 9, 9, 32, 32, channels)
    lbl = np.random.rand(8, 32, 32)
    valid_data = dict(data=dat, disp=lbl)

    train_kwargs = dict(data=data,
                        valid_data=valid_data,
                        data_key="data",
                        label_keys="disp",
                        augmented_shape=(9, 9, 32, 32, channels),
                        generated_shape=generated_shape,
                        batch_size=2,
                        epochs=1,
                        verbose=0
                        )

    return train_kwargs


def get_test_kwargs(generated_shape, channels=3):
    dat = np.random.rand(8, 9, 9, 32, 32, channels)
    lbl = np.random.rand(8, 32, 32)
    data = dict(data=dat, disp=lbl)

    test_kwargs = dict(data=data,
                       data_key="data",
                       label_keys="disp",
                       augmented_shape=(9, 9, 32, 32, channels),
                       generated_shape=generated_shape,
                       batch_size=1,
                       verbose=0
                       )

    return test_kwargs


def get_eval_kwargs(generated_shape, channels=3):
    dat = np.random.rand(4, 9, 9, 64, 64, channels)
    lbl = np.random.rand(4, 64, 64)
    data = dict(data=dat, disp=lbl)

    eval_kwargs = dict(data=data,
                       data_key="data",
                       label_keys="disp",
                       augmented_shape=(9, 9, 64, 64, channels),
                       generated_shape=generated_shape,
                       batch_size=1,
                       verbose=0
                       )

    return eval_kwargs


def test_train():

    model_kwargs = get_model_kwargs()

    # Run for different amount of spectral channels
    for channels in [3, 13, 30]:
        train_kwargs = get_train_kwargs((32, 32, 9*9*channels), channels)

        model = Dummy(**model_kwargs)
        res = model.train(**train_kwargs)

        assert 'loss' in res.history
        assert 'val_loss' in res.history
        clear_session()

    return


def test_test():

    model_kwargs = get_model_kwargs()

    # Run for different amount of spectral channels
    for channels in [3, 13, 30]:
        test_kwargs = get_test_kwargs((32, 32, 9*9*channels), channels)

        model = Dummy(**model_kwargs)
        res = model.test(**test_kwargs)

        assert 'loss' in res.keys()
        clear_session()

    return


def test_evaluate_challenges():

    model_kwargs = get_model_kwargs()

    # Run for different amount of spectral channels
    for channels in [3, 13, 30]:
        train_kwargs = get_train_kwargs((32, 32, 9*9*channels), channels)
        eval_kwargs = get_eval_kwargs((64, 64, 9*9*channels), channels)

        model = Dummy(depth=2, **model_kwargs)
        model.train(**train_kwargs)
        res = model.evaluate_challenges(**eval_kwargs)
        for s in ["metrics", "disparity", "central_view"]:
            assert s in res
            assert len(res[s]) == 4
        clear_session()

    return


def test_conv3d_decode2d():

    model_kwargs = get_model_kwargs()

    # Run for different amount of spectral channels
    for channels in [3, 13, 30]:
        train_kwargs = get_train_kwargs((32, 32, 9*9, channels), channels)

        model = Conv3dDecode2d(**model_kwargs)
        res = model.train(**train_kwargs)

        assert 'loss' in res.history
        assert 'val_loss' in res.history
        clear_session()

    return


def test_conv3d_decode3d():

    model_kwargs = get_model_kwargs()

    # Run for different amount of spectral channels
    for channels in [3, 13, 30]:
        train_kwargs = get_train_kwargs((32, 32, 9*9, channels), channels)

        model = Conv3dDecode3d(**model_kwargs)
        res = model.train(**train_kwargs)

        assert 'loss' in res.history
        assert 'val_loss' in res.history
        clear_session()

    return
