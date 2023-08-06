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
from lfcnn.callbacks.cyclic_learning import MomentumScheduler


def get_train_kwargs(generated_shape):
    dat = np.random.rand(8, 9, 9, 32, 32, 3)
    data = dict(data=dat)
    dat = np.random.rand(8, 9, 9, 32, 32, 3)
    valid_data = dict(data=dat)

    train_kwargs = dict(data=data,
                        valid_data=valid_data,
                        data_key="data",
                        label_keys=[],
                        augmented_shape=(9, 9, 32, 32, 3),
                        generated_shape=generated_shape,
                        batch_size=2,
                        epochs=1,
                        verbose=0
                        )

    return train_kwargs


def test_momentum_scheduler():

    optimizer = optimizers.SGD(learning_rate=0.1)
    loss = dict(light_field=MeanSquaredError())
    metrics = dict(light_field=get_lf_metrics())
    callbacks = [MomentumScheduler(schedule=lambda x, y: y*x)]

    model = Dummy(optimizer=optimizer,
                  loss=loss,
                  metrics=metrics,
                  callbacks=callbacks)

    train_kwargs = get_train_kwargs((32, 32, 9*9*3))
    res = model.train(**train_kwargs)

    assert 'loss' in res.history
    assert 'val_loss' in res.history
    clear_session()

    # Test optimizer without momentum attribute
    optimizer = optimizers.RMSprop(learning_rate=0.1)
    loss = dict(light_field=MeanSquaredError())
    metrics = dict(light_field=get_lf_metrics())
    callbacks = [MomentumScheduler(schedule=lambda x, y: y*x)]
    model = Dummy(optimizer=optimizer,
                  loss=loss,
                  metrics=metrics,
                  callbacks=callbacks)
    train_kwargs = get_train_kwargs((32, 32, 9*9*3))

    with raises(ValueError) as e:
        res = model.train(**train_kwargs)
    assert "Optimizer does not support momentum scheduling." in str(e)
    clear_session()

    return


def test_one_cycle():
    lr = callbacks.OneCycle(lr_min=0.1, lr_max=1, lr_final=0.001, cycle_epoch=10, max_epoch=15)
    epochs = range(20)
    lrs_pred = [lr.schedule(e, 0) for e in epochs]
    assert approx(lrs_pred[0], rel=0.01) == 0.1
    assert approx(lrs_pred[5], rel=0.01) == 1
    assert approx(lrs_pred[10], rel=0.01) == 0.1
    assert approx(lrs_pred[14], rel=0.01) == 0.001
    assert approx(lrs_pred[15], rel=0.01) == 0.001
    assert approx(lrs_pred[19], rel=0.01) == 0.001

    return


def test_one_cycle_cosine():
    lr = callbacks.OneCycleCosine(lr_min=0.1, lr_max=1, lr_final=0.001, phase_epoch=5, max_epoch=15)
    epochs = range(20)
    lrs_pred = [lr.schedule(e, 0) for e in epochs]

    assert approx(lrs_pred[0], rel=0.01) == 0.1
    assert approx(lrs_pred[5], rel=0.01) == 1
    assert approx(lrs_pred[10], rel=0.01) == 0.5005
    assert approx(lrs_pred[15], rel=0.01) == 0.001
    assert approx(lrs_pred[19], rel=0.01) == 0.001

    return


def test_one_cycle_momentum():
    ms = callbacks.OneCycleMomentum(m_max=1, m_min=0.5, cycle_epoch=10)
    epochs = range(15)
    m_pred = [ms.schedule(e, 0) for e in epochs]
    m_true = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1, 1, 1, 1]

    assert approx(m_pred, rel=0.01) == m_true

    return


def test_one_cycle_cosine_momentum():
    lr = callbacks.OneCycleCosineMomentum(m_min=0.1, m_max=1, phase_epoch=5, max_epoch=15)
    epochs = range(20)
    lrs_pred = [lr.schedule(e, 0) for e in epochs]

    print(lrs_pred)
    assert approx(lrs_pred[0], rel=0.01) == 1
    assert approx(lrs_pred[5], rel=0.01) == 0.1
    assert approx(lrs_pred[10], rel=0.01) == 0.55
    assert approx(lrs_pred[15], rel=0.01) == 1
    assert approx(lrs_pred[19], rel=0.01) == 1

    return
