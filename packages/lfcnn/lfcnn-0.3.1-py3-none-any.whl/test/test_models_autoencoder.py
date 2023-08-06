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


"""Test lfcnn.models.autoencoder
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

from lfcnn.models.autoencoder import get
from lfcnn.models.autoencoder import Conv3dModel, EpiVolumeEncoder, Dummy

ALL_AUTOENCODER_MODELS = {
    "EpiVolumeEncoder": EpiVolumeEncoder,
    "Conv3dModel": Conv3dModel,
    "Dummy": Dummy
}


def test_getter():

    for model_name in ALL_AUTOENCODER_MODELS:
        res = get(model_name)
        assert res == ALL_AUTOENCODER_MODELS[model_name]

    # Check nonsense
    with raises(ValueError) as e:
        _ = get("nonsense")
    assert "Unknown autoencoder model" in str(e)

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


def get_train_kwargs(generated_shape, augmented_shape=(9, 9, 32, 32, 3)):
    dat = np.random.rand(8, 9, 9, 32, 32, 3)
    data = dict(data=dat)
    dat = np.random.rand(8, 9, 9, 32, 32, 3)
    valid_data = dict(data=dat)

    train_kwargs = dict(data=data,
                        valid_data=valid_data,
                        data_key="data",
                        label_keys=[],
                        augmented_shape=augmented_shape,
                        generated_shape=generated_shape,
                        batch_size=2,
                        epochs=1,
                        verbose=0
                        )

    return train_kwargs


def test_epi_volume_encoder():
    model_kwargs = get_model_kwargs()
    model = EpiVolumeEncoder(**model_kwargs)

    train_kwargs = get_train_kwargs((32, 32, 9, 3), augmented_shape=(1, 9, 32, 32, 3))
    res = model.train(**train_kwargs)

    assert 'loss' in res.history
    assert 'val_loss' in res.history
    clear_session()

    return


def test_conv3d():
    model_kwargs = get_model_kwargs()
    model = Conv3dModel(**model_kwargs)

    train_kwargs = get_train_kwargs((32, 32, 9*9, 3))
    res = model.train(**train_kwargs)

    assert 'loss' in res.history
    assert 'val_loss' in res.history
    clear_session()

    return


def test_dummy_model():
    model_kwargs = get_model_kwargs()
    model = Dummy(**model_kwargs)

    train_kwargs = get_train_kwargs((32, 32, 9*9*3))
    res = model.train(**train_kwargs)

    assert 'loss' in res.history
    assert 'val_loss' in res.history
    clear_session()

    return
