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


"""Test lfcnn.models
"""
# Set CPU as device:
from lfcnn.utils.tf_utils import use_cpu
use_cpu()

from tempfile import TemporaryDirectory
from pathlib import Path
from pytest import raises

import numpy as np

from tensorflow.keras.backend import clear_session
from tensorflow.keras import optimizers, Model, Input
from tensorflow.keras.layers import Activation, BatchNormalization

from lfcnn.losses import MeanSquaredError
from lfcnn.metrics import MeanSquaredError as MSE_metric
from lfcnn.metrics import MeanAbsoluteError as MAE_metric
from lfcnn.metrics import get_lf_metrics, PSNR
from lfcnn.models import BaseModel

from lfcnn.generators import LfGenerator
from lfcnn.generators.reshapes import lf_identity
from lfcnn.models.autoencoder import Dummy as AeDummy


class MockModel(BaseModel):

    def __init__(self, **kwargs):
        super(MockModel, self).__init__(**kwargs)

    def set_generator_and_reshape(self):
        self._generator = LfGenerator
        self._reshape_func = lf_identity
        return

    def create_model(self, inputs, augmented_shape=None):
        out = Activation('sigmoid')(inputs)
        out = BatchNormalization(name='light_field')(out)
        return Model(inputs, out, name="MockModel")


def get_model_kwargs(types="dict"):
    optimizer = optimizers.SGD(learning_rate=0.1)

    if types == "none":
        loss = None
        metrics = None
        callbacks = None

    elif types == "single":
        loss = MeanSquaredError()
        metrics = get_lf_metrics()
        callbacks = []

    elif types == "dict":
        loss = dict(light_field=MeanSquaredError())
        metrics = dict(light_field=get_lf_metrics())
        callbacks = []

    else:
        raise ValueError("Incorrect types set.")

    model_kwargs = dict(
        optimizer=optimizer,
        loss=loss,
        metrics=metrics,
        callbacks=callbacks
    )

    return model_kwargs


def get_train_kwargs(generated_shape,
                     input_shape=(9, 9, 36, 36, 3),
                     augmented_shape=(9, 9, 32, 32, 3)):
    dat = np.random.rand(8, *input_shape)
    data = dict(data=dat)
    valid_dat = np.random.rand(8, *input_shape)
    valid_data = dict(data=valid_dat)

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


def get_test_kwargs(generated_shape,
                    input_shape=(9, 9, 36, 36, 3),
                    augmented_shape=(9, 9, 32, 32, 3)):
    dat = np.random.rand(8, *input_shape)
    data = dict(data=dat)

    test_kwargs = dict(data=data,
                        data_key="data",
                        label_keys=[],
                        augmented_shape=augmented_shape,
                        generated_shape=generated_shape,
                        batch_size=1,
                        verbose=0
                        )

    return test_kwargs


def get_eval_kwargs(generated_shape,
                    input_shape=(9, 9, 64, 64, 3),
                    augmented_shape=(9, 9, 64, 64, 3)):
    dat = np.random.rand(4, *input_shape)
    data = dict(data=dat)

    eval__kwargs = dict(data=data,
                        data_key="data",
                        label_keys=[],
                        augmented_shape=augmented_shape,
                        generated_shape=generated_shape,
                        batch_size=1,
                        verbose=0
                        )

    return eval__kwargs


def test_init():

    model_kwargs = get_model_kwargs()
    model = MockModel(**model_kwargs)

    assert isinstance(model.optimizer, optimizers.SGD)
    assert isinstance(model.loss['light_field'], MeanSquaredError)
    assert isinstance(model.metrics['light_field'][0], MAE_metric)
    assert isinstance(model.metrics['light_field'][1], MSE_metric)
    assert isinstance(model.metrics['light_field'][2], PSNR)
    assert model.callbacks == []
    assert model.generator == LfGenerator
    assert model.reshape_func == lf_identity
    assert model.model_crop is None

    clear_session()
    return


def test_model_build():

    model_kwargs = get_model_kwargs()
    model = MockModel(**model_kwargs)

    assert model.keras_model is None

    generated_shape = [(9, 9, 32, 32, 3)]
    model.__build_model__(generated_shape, (9, 9, 32, 32, 3), gpus=1, cpu_merge=False)

    assert isinstance(model.keras_model, Model)
    assert model.keras_model.name == "MockModel"
    assert isinstance(model.optimizer, optimizers.SGD)
    assert isinstance(model.loss['light_field'], MeanSquaredError)
    assert isinstance(model.metrics['light_field'][0], MAE_metric)
    assert isinstance(model.metrics['light_field'][1], MSE_metric)
    assert isinstance(model.metrics['light_field'][2], PSNR)

    # Model is compiled and should be trainable
    data = np.random.rand(8, 9, 9, 32, 32, 3)
    target = data.copy()
    model.keras_model.fit(data, target, batch_size=2, epochs=1, verbose=0)
    clear_session()

    # Update shape and check if rebuild necessary
    model_kwargs = get_model_kwargs()
    model = MockModel(**model_kwargs)

    # Same shape, set model, build not necessary
    generated_shape = [(9, 9, 32, 32, 3)]
    model.__build_model__(generated_shape, (9, 9, 32, 32, 3), gpus=1, cpu_merge=False)
    assert not model.__build_necessary__(generated_shape=generated_shape)

    # Now update shape, and retrain
    generated_shape = [(9, 9, 64, 64, 3)]
    assert model.__build_necessary__(generated_shape=generated_shape)

    model.__build_model__(generated_shape, (9, 9, 64, 64, 3), gpus=1, cpu_merge=False)

    # Model is compiled and should be trainable
    data = np.random.rand(8, 9, 9, 64, 64, 3)
    target = data.copy()
    model.keras_model.fit(data, target, batch_size=2, epochs=1, verbose=0)
    clear_session()

    return


def test_model_build_none():

    model_kwargs = get_model_kwargs(types="none")
    model = MockModel(**model_kwargs)

    assert model.keras_model is None

    generated_shape = [(9, 9, 32, 32, 3)]
    model.__build_model__(generated_shape, (9, 9, 32, 32, 3), gpus=1, cpu_merge=False)

    assert isinstance(model.keras_model, Model)
    assert model.keras_model.name == "MockModel"
    assert model.loss is None
    assert model.metrics is None
    assert model.callbacks is None

    # Cannot fit model without loss/gradients. If loss is None, needs to be
    # set in a specific layer
    clear_session()

    return


def test_model_build_single():

    model_kwargs = get_model_kwargs(types="single")
    model = MockModel(**model_kwargs)

    assert model.keras_model is None

    generated_shape = [(9, 9, 32, 32, 3)]
    model.__build_model__(generated_shape, (9, 9, 32, 32, 3), gpus=1, cpu_merge=False)

    assert isinstance(model.keras_model, Model)
    assert model.keras_model.name == "MockModel"
    assert isinstance(model.optimizer, optimizers.SGD)
    assert isinstance(model.loss, MeanSquaredError)
    assert isinstance(model.metrics[0], MAE_metric)
    assert isinstance(model.metrics[1], MSE_metric)
    assert isinstance(model.metrics[2], PSNR)

    # Model is compiled and should be trainable
    data = np.random.rand(8, 9, 9, 32, 32, 3)
    target = data.copy()
    model.keras_model.fit(data, target, batch_size=2, epochs=1, verbose=0)
    clear_session()

    return


def test_model_train():

    model_kwargs = get_model_kwargs()
    train_kwargs = get_train_kwargs((9, 9, 32, 32, 3))

    model = MockModel(**model_kwargs)
    res = model.train(**train_kwargs)

    assert 'loss' in res.history
    assert 'val_loss' in res.history
    clear_session()
    return


def test_model_test():

    model_kwargs = get_model_kwargs()
    test_kwargs = get_test_kwargs((9, 9, 32, 32, 3))

    model = MockModel(**model_kwargs)
    res = model.test(**test_kwargs)

    assert 'loss' in res.keys()
    clear_session()
    return


def test_model_train_and_test():
    """Check that model weights are correctly transferred when testing after
    training. When testingt after training, it is assumed that no rebuild is
    necessary."""

    model_kwargs = get_model_kwargs()
    train_kwargs = get_train_kwargs((9, 9, 32, 32, 3))
    test_kwargs = get_test_kwargs((9, 9, 32, 32, 3))

    model = MockModel(**model_kwargs)
    model.train(**train_kwargs)
    train_weights = model.keras_model.get_weights()
    res = model.test(**test_kwargs)
    test_weights = model.keras_model.get_weights()

    assert len(train_weights) == len(test_weights)
    for x, y in zip(train_weights, test_weights):
        assert np.array_equal(x, y)

    clear_session()
    return


def test_model_evaluate_challenges():

    train_gen_shape = (32, 32, 9*9*3)
    train_augmented_shape = (9, 9, 32, 32, 3)
    train_input_shape = (9, 9, 36, 36, 3)

    eval_gen_shape = (256, 256, 9*9*3)
    eval_augmented_shape = (9, 9, 256, 256, 3)
    eval_input_shape = (9, 9, 256, 256, 3)

    model_kwargs = get_model_kwargs()
    train_kwargs = get_train_kwargs(generated_shape=train_gen_shape,
                                    input_shape=train_input_shape,
                                    augmented_shape=train_augmented_shape)
    eval_kwargs = get_eval_kwargs(generated_shape=eval_gen_shape,
                                  input_shape=eval_input_shape,
                                  augmented_shape=eval_augmented_shape)

    model = AeDummy(depth=2, **model_kwargs)
    model.train(**train_kwargs)
    train_weights = model.keras_model.get_weights()

    res = model.evaluate_challenges(**eval_kwargs)
    eval_weights = model.keras_model.get_weights()

    # Check weight lists equality
    assert len(train_weights) == len(eval_weights)
    for x, y in zip(train_weights, eval_weights):
        assert np.array_equal(x, y)

    for s in ["metrics", "light_field"]:
        assert s in res
        assert len(res[s]) == 4

    clear_session()
    return


def test_model_evaluate_challenges_fails():

    train_gen_shape = (32, 32, 9*9*3)
    train_augmented_shape = (9, 9, 32, 32, 3)
    train_input_shape = (9, 9, 36, 36, 3)

    eval_gen_shape = (256, 256, 9*9*3)
    eval_augmented_shape = (9, 9, 256, 256, 3)
    eval_input_shape = (9, 9, 256, 256, 3)

    model_kwargs = get_model_kwargs()
    train_kwargs = get_train_kwargs(generated_shape=train_gen_shape,
                                    input_shape=train_input_shape,
                                    augmented_shape=train_augmented_shape)
    eval_kwargs = get_eval_kwargs(generated_shape=eval_gen_shape,
                                  input_shape=eval_input_shape,
                                  augmented_shape=eval_augmented_shape)

    model = AeDummy(depth=2, **model_kwargs)
    model.train(**train_kwargs)
    train_weights = model.keras_model.get_weights()

    with TemporaryDirectory() as tmp_dir:
        # Save training weights
        weights_path = Path(tmp_dir) / "train_weights.h5"
        weights_path = str(weights_path)
        model.keras_model.save_weights(weights_path)

        # Reset model
        model._keras_model = None

        # Test error when no weight path is given
        with raises(ValueError) as e:
            _ = model.evaluate_challenges(**eval_kwargs)
        assert "'model_weights' need to be specified" in str(e)

        # Rebuild model from saved weights
        # Add weight path to eval kwargs
        eval_kwargs['model_weights'] = weights_path
        res = model.evaluate_challenges(**eval_kwargs)
        eval_weights = model.keras_model.get_weights()

        # Check weight lists equality
        assert len(train_weights) == len(eval_weights)
        for x, y in zip(train_weights, eval_weights):
            assert np.array_equal(x, y)

        for s in ["metrics", "light_field"]:
            assert s in res
            assert len(res[s]) == 4

    clear_session()
    return


def test_model_save_load_weights():

    model_kwargs = get_model_kwargs()
    train_kwargs = get_train_kwargs((9, 9, 32, 32, 3))

    model = MockModel(**model_kwargs)

    # Check error message
    with TemporaryDirectory() as tmp_dir:
        save_path = Path(tmp_dir) / "weights.h5"
        with raises(ValueError) as e:
            model.save_weights(save_path)
        assert "Model has not been created yet." in str(e)

    # Build and train model
    res = model.train(**train_kwargs)

    with TemporaryDirectory() as tmp_dir:
        # Test both h5 and TF format save
        for ext in [".h5", ".chkpt"]:
            save_path = Path(tmp_dir) / "weights"
            save_path = str(save_path.with_suffix(ext))

            model.save_weights(save_path)
            clear_session()

            new_model = MockModel(**model_kwargs)
            new_model.load_weights(save_path,
                                   generated_shape=(9, 9, 36, 36, 3),
                                   augmented_shape=(9, 9, 32, 32, 3))

            assert np.array_equal(model.keras_model.get_weights(),
                                  new_model.keras_model.get_weights())

    clear_session()
    return


def test_model_save_load():

    model_kwargs = get_model_kwargs()
    train_kwargs = get_train_kwargs((9, 9, 32, 32, 3))

    model = MockModel(**model_kwargs)
    res = model.train(**train_kwargs)

    # Check error message
    with TemporaryDirectory() as tmp_dir:
        save_path = Path(tmp_dir) / "model"
        save_path = str(save_path)

        with raises(NotImplementedError) as e:
            model.save(save_path)
        assert "Saving and loading of the full model state is not yet supported." in str(e)

        clear_session()

        with raises(NotImplementedError) as e:
            new_model = MockModel(**model_kwargs)
            new_model.load(save_path)
        assert "Saving and loading of the full model state is not yet supported." in str(e)

    clear_session()
    return
