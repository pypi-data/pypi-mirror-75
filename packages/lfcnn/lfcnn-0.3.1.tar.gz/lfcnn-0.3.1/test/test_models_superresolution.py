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


"""Test lfcnn.models.superresolution
"""
# Set CPU as device:
from lfcnn.utils.tf_utils import use_cpu
use_cpu()

from pytest import raises

import numpy as np

from tensorflow.keras.backend import clear_session
from tensorflow.keras import optimizers
from lfcnn.losses import MeanSquaredError
from lfcnn.metrics import get_lf_metrics

from lfcnn.models.superresolution import get
from lfcnn.models.superresolution import SasConv, Dummy

ALL_SUPERRESOLUTION_MODELS = {
    "Dummy": Dummy,
    "SasConv": SasConv
}


def test_getter():

    for model_name in ALL_SUPERRESOLUTION_MODELS:
        res = get(model_name)
        assert res == ALL_SUPERRESOLUTION_MODELS[model_name]

    # Check nonsense
    with raises(ValueError) as e:
        _ = get("nonsense")
    assert "Unknown superresolution model" in str(e)

    return


def get_model_kwargs():
    optimizer = optimizers.SGD(learning_rate=0.1)
    loss = dict(light_field=MeanSquaredError())
    metrics = dict(light_field=get_lf_metrics())

    model_kwargs = dict(
        optimizer=optimizer,
        loss=loss,
        metrics=metrics,
        callbacks=[]
    )

    return model_kwargs


def get_train_kwargs(generated_shape, channels=3):
    dat = np.random.rand(8, 9, 9, 32, 32, channels)
    data = dict(data=dat)
    dat = np.random.rand(8, 9, 9, 32, 32, channels)
    valid_data = dict(data=dat)

    train_kwargs = dict(data=data,
                        valid_data=valid_data,
                        data_key="data",
                        label_keys=[],
                        augmented_shape=(9, 9, 32, 32, channels),
                        generated_shape=generated_shape,
                        batch_size=2,
                        epochs=1,
                        verbose=0
                        )

    return train_kwargs


def get_test_kwargs(generated_shape, channels=3):
    dat = np.random.rand(8, 9, 9, 32, 32, channels)
    data = dict(data=dat)

    test_kwargs = dict(data=data,
                       data_key="data",
                       label_keys=[],
                       augmented_shape=(9, 9, 32, 32, channels),
                       generated_shape=generated_shape,
                       batch_size=1,
                       verbose=0
                       )

    return test_kwargs


def get_eval_kwargs(generated_shape, channels=3):
    dat = np.random.rand(4, 9, 9, 64, 64, channels)
    data = dict(data=dat)

    eval_kwargs = dict(data=data,
                       data_key="data",
                       label_keys=[],
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
        train_kwargs = get_train_kwargs((16, 16, 9*9*channels), channels)

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
        test_kwargs = get_test_kwargs((16, 16, 9*9*channels), channels)

        model = Dummy(**model_kwargs)
        res = model.test(**test_kwargs)

        assert 'loss' in res.keys()
        clear_session()

    return


def test_evaluate_challenges():

    model_kwargs = get_model_kwargs()

    # Run for different amount of spectral channels
    for channels in [3, 13, 30]:
        train_kwargs = get_train_kwargs((16, 16, 9*9*channels), channels)
        eval_kwargs = get_eval_kwargs((32, 32, 9*9*channels), channels)

        model = Dummy(depth=2, **model_kwargs)
        model.train(**train_kwargs)

        # Set full size metrics for evaluation
        metrics = dict(light_field=get_lf_metrics())
        model._metrics = metrics
        res = model.evaluate_challenges(**eval_kwargs)
        for s in ["metrics", "light_field"]:
            assert s in res
            assert len(res[s]) == 4
        clear_session()

    return


def test_sas_conv():
    model_kwargs = get_model_kwargs()
    model = SasConv(**model_kwargs)
    # Spatial downsampling by 2
    train_kwargs = get_train_kwargs((9*9, 16, 16, 3))
    res = model.train(**train_kwargs)

    assert 'loss' in res.history
    assert 'val_loss' in res.history
    clear_session()

    return
