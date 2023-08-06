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


"""Abstract base class definitions.
"""
from typing import Union, Dict, List, Optional, Tuple, Callable
from contextlib import contextmanager

import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.losses import Loss as Loss
from tensorflow.keras.metrics import Metric
from tensorflow.keras.optimizers import Optimizer
from tensorflow.keras.callbacks import Callback

from lfcnn.generators.utils import shape_wrapper
from lfcnn.utils.tf_utils import list_visible_devices


class BaseModel(object):

    def __init__(self,
                 optimizer: Optimizer,
                 loss: Optional[Union[Loss, Dict[str, Loss]]],
                 metrics: Optional[Union[Metric, Dict[str, Metric], Dict[str, List[Metric]]]],
                 callbacks: Optional[Callback]):

        self._optimizer = optimizer
        self._loss = loss
        self._metrics = metrics
        self._callbacks = callbacks

        self._keras_model: Union[keras.Model, None] = None
        self.output_names = None
        self._model_crop = None

        self._generator = None
        self._reshape_func = None
        self.set_generator_and_reshape()
        if self.generator is None or self.reshape_func is None:
            raise ValueError("Generator or reshape not set. Set them in the "
                             "model's set_generator_and_reshape method.")

        return

    def __build_necessary__(self, generated_shape: List[tuple]) -> bool:
        """Check whether building of the keras model is necessary.

        Args:
            generated_shape: List of generated shape by generator, i.e.
                             input shapes of model.

        Returns:
            True if build is necessary, else False.
        """

        res = True

        # If model is set and shapes are correct, no build necessary
        if self.keras_model is not None:
            input_shape = [layer.get_input_shape_at(0)[1:] for layer in self.keras_model._input_layers]
            if input_shape == generated_shape:
                res = False

        return res

    def __build_model__(self,
                        generated_shape: List[tuple],
                        augmented_shape: Optional[Tuple[int, int, int, int, int]],
                        gpus: Union[int, List[int]] = 1,
                        cpu_merge: bool = False):
        """Create the Keras model as defined by the derived class,
        sets the keras_module attribute and compile it with the specified
        optimizer, loss and metrics.

        TODO: Refactor strategies. The OndeDeviceStrategy and the
        MirroredStrategy in same instances show deadlocks when using
        multiprocessing for the data generators. Currently, the workaround
        is using a DummyStrategy with an empty scope() context manager.

        See Also:
            :func:`create_model`
        """

        # Create inputs from shapes
        inputs = [keras.Input(shape) for shape in generated_shape]

        gpus_avail = list_visible_devices("gpu")
        if gpus == 0 or not gpus_avail:
            print("Created LFCNN model for CPU.")
            # strategy = tf.distribute.OneDeviceStrategy("/cpu:0")
            strategy = DummyStrategy()

        elif gpus == 1 or len(gpus_avail) == 1:
            print("Created LFCNN model for single GPU.")
            # strategy = tf.distribute.OneDeviceStrategy("/gpu:0")
            strategy = DummyStrategy()

        elif gpus > 1:
            print("Created LFCNN model for multi GPU.")
            strategy = tf.distribute.MirroredStrategy()

        else:
            raise ValueError("Specified GPU option needs to be a zero or positive integer.")

        with strategy.scope():
            # TODO: Refactor to only pass callables of
            #  optimizer, loss and metric and init them here

            # Re-instantiate optimizer, loss and metrics in new strategy scope
            optimizer = self._optimizer.__class__.from_config(self._optimizer.get_config())

            if self._loss is None:
                loss = None
            elif type(self._loss) == dict:
                loss = {i: self._loss[i].__class__.from_config(self._loss[i].get_config()) for i in self._loss}
            else:
                loss = self._loss.__class__.from_config(self._loss.get_config())

            if self._metrics is None:
                metrics = None
            elif type(self._metrics) == dict:
                metrics = {i: [j.__class__.from_config(j.get_config()) for j in self._metrics[i]] for i in self._metrics}
            elif type(self._metrics) == list:
                metrics = [i.__class__.from_config(i.get_config()) for i in self._metrics]
            else:
                metrics = self._metrics.__class__.from_config(self._metrics.get_config())

            # Update instances
            self._optimizer = optimizer
            self._loss = loss
            self._metrics = metrics

            # Create and compile
            self._keras_model = self.create_model(inputs, augmented_shape)
            self.keras_model.compile(optimizer=self._optimizer,
                                     loss=self._loss,
                                     metrics=self._metrics)
            self.output_names = [layer.name for layer in self.keras_model._output_layers]
        return

    def set_generator_and_reshape(self):
        raise NotImplementedError("This needs to be implemented by the derived class.")

    def create_model(self,
                     inputs: List[keras.Input],
                     augmented_shape: Optional[Tuple[int, int, int, int, int]]) -> keras.Model:
        """Create the Keras model.
        Needs to be implemented by the derived class to define the network topology.

        Args:
            inputs: List of Keras Inputs. Single or multi inputs supported.

            augmented_shape: The augmented shape as generated by the generator.
                             Can be used to obtain the original light field's
                             shape, for example the number of subapertures
                             or the number of spectral channels.
        """
        raise NotImplementedError("This needs to be implemented by the derived class.")

    @property
    def optimizer(self) -> Optimizer:
        return self._optimizer

    @property
    def loss(self) -> Loss:
        return self._loss

    @property
    def metrics(self) -> Metric:
        return self._metrics

    def set_metrics(self, metric: Metric):
        """Set metrics after model instantiation.
        This is useful, e.g. when evaluating the model on full-sized light fields.
        In that case, MS-SSIM can be used with more scales."""
        self._metrics = metric
        return

    @property
    def callbacks(self) -> Callback:
        return self._callbacks

    @property
    def generator(self):
        return self._generator

    @property
    def reshape_func(self) -> Callable:
        return self._reshape_func

    @property
    def model_crop(self) -> tuple:
        return self._model_crop

    @property
    def keras_model(self) -> keras.Model:
        return self._keras_model

    def train(self,
              data,
              valid_data,
              data_key,
              label_keys,
              augmented_shape,
              generated_shape,
              batch_size,
              valid_data_key=None,
              valid_label_keys=None,
              valid_batch_size=None,
              data_percentage=1.0,
              valid_percentage=1.0,
              range_data=None,
              range_labels=None,
              range_valid_data=None,
              range_valid_labels=None,
              augment=True,
              shuffle=True,
              use_mask=False,
              fix_seed=False,
              gpus: Union[int, List[int]] = 1,
              cpu_merge: bool = False,
              gen_kwargs: Optional[dict] = None,
              **kwargs) -> keras.callbacks.History:
        """Train and validate the model.

        Args:
            data: Data dictionary or path to training data .h5 file.

            valid_data: Data dictionary or path to validation data .h5 file.

            data_key:  Key of light field data in training data file or dictionary.

            label_keys:  Keys of label in training data file or dictionary.

            valid_data_key: Key of light field data in validation data file or dictionary.

            valid_label_keys: Keys of labels in validation data file or dictionary.

            augmented_shape: Shape after augmentation.
                             (Indirectly defines angular and spatial crop,
                             when smaller than input shapes)

            generated_shape: Generated shape or list of generated shapes in
                             case of multi input models.

            batch_size: Batch size.

            data_percentage: Percentage of training data to use.
                             Can be used to test a training on a smaller set.

            valid_percentage: Percentage of validation data to use.
                              Can be used to test a training on a smaller set.

            valid_batch_size: Batch size used for validation.

            range_data: Dynamic range of input light field data.
                        Used to normalize the input data to a range [0, 1].
                        If no normalization is necessary, specify None.

            range_labels: Dynamic range of input label data.
                          May be used to normalize the input data to a range [0, 1].
                          If no normalization is necessary, specify None.
                          If a list of labels is used, specify ranges as list,
                          e.g. [255, None, None]

            range_valid_data: Dynamic range of input light field validation data.
                              Used to normalize the input data to a range [0, 1].
                              If no normalization is necessary, specify None.

            range_valid_labels: Dynamic range of input label validation data.
                                May be used to normalize the input data to a range [0, 1].
                                If no normalization is necessary, specify None.
                                If a list of labels is used, specify ranges as list,
                                e.g. [255, None, None]

            augment: Whether to perform online augmentation.
                     Cropping to augmented_shape is always performed.

            shuffle: Whether to shuffle data between epochs.

            use_mask: Whether to use a color coding mask.

            fix_seed: Whether to use a constant seed for random augments during
                      training. The seed for validation is always fixed.

            gpus: Integer or list of integers specifying the number of GPUs
                  or GPU IDs to use for training. Defaults to 1. If more than
                  one GPU is used, the model will be distributed across
                  multiple GPUs, i.e. the batch will be split up across
                  the GPUs.

            cpu_merge: Used when gpus > 1. Whether to force merging model
                       weights under the scope of the CPU or not.
                       Defaults to False (recommended for NV-Link)

            gen_kwargs: Passed to generator instantiation.

            **kwargs: Passed to :func:`tensorflow.keras.model.fit()`.

        Returns:
            hist
            A History object.
            The attribute hist.history contains the logged values.
        """
        # For single input models, wrap shape in list
        generated_shape = shape_wrapper(generated_shape)

        # Create and build model if necessary
        if self.__build_necessary__(generated_shape):
            self.__build_model__(generated_shape,
                                 augmented_shape=augmented_shape,
                                 gpus=gpus,
                                 cpu_merge=cpu_merge)

        # Use reshape as defined by model
        reshape_func = self.reshape_func

        # Init Generators
        gen_kwargs = gen_kwargs or {}
        train_gen_kwargs = dict(data=data,
                                data_key=data_key,
                                label_keys=label_keys,
                                augmented_shape=augmented_shape,
                                generated_shape=generated_shape,
                                reshape_func=reshape_func,
                                model_crop=self.model_crop,
                                batch_size=batch_size,
                                range_data=range_data,
                                range_labels=range_labels,
                                data_percentage=data_percentage,
                                augment=augment,
                                shuffle=shuffle,
                                use_mask=use_mask,
                                fix_seed=fix_seed,
                                **gen_kwargs)

        # By default, use same data/label keys as for training data
        if valid_data_key is None:
            valid_data_key = data_key

        if valid_label_keys is None:
            valid_label_keys = label_keys

        if valid_batch_size is None:
            valid_batch_size = batch_size

        if range_valid_data is None and range_data is not None:
            import warnings
            warnings.warn(
                "You specified a data range for the training data but not for "
                "the validation data. Hence, the validation data will not be "
                "normalized. You can ignore this, if this is intended.")

        # For validation, fix seed and do not shuffle nor use augmentation
        valid_gen_kwargs = dict(data=valid_data,
                                data_key=valid_data_key,
                                label_keys=valid_label_keys,
                                augmented_shape=augmented_shape,
                                generated_shape=generated_shape,
                                reshape_func=reshape_func,
                                model_crop=self.model_crop,
                                batch_size=valid_batch_size,
                                range_data=range_valid_data,
                                range_labels=range_valid_labels,
                                data_percentage=valid_percentage,
                                augment=False,
                                shuffle=False,
                                use_mask=use_mask,
                                fix_seed=True,
                                **gen_kwargs)

        generator = self.generator(**train_gen_kwargs)
        if valid_data is not None:
            valid_generator = self.generator(**valid_gen_kwargs)
        else:
            valid_generator = None

        # Fit model using the data generator and the validation generator
        # Note that shuffling is performed in the generator.
        hist = self.keras_model.fit(generator,
                                    validation_data=valid_generator,
                                    callbacks=self._callbacks,
                                    shuffle=False,
                                    **kwargs)
        return hist

    def test(self,
             data,
             data_key,
             label_keys,
             augmented_shape,
             generated_shape,
             batch_size,
             data_percentage=1.0,
             range_data=None,
             range_labels=None,
             use_mask=False,
             gpus: Union[int, List[int]] = 1,
             cpu_merge: bool = False,
             gen_kwargs: Optional[dict] = None,
             **kwargs) -> dict:
        """Evaluate the model using a test dataset.

        Args:
            data: Data dictionary or path to test data .h5 file.

            data_key:  Key of light field data in test data file or dictionary.

            label_keys:  Keys of label in test data file or dictionary.

            augmented_shape: Shape after augmentation.
                             (Indirectly defines angular and spatial crop,
                             when smaller than input shapes)

            generated_shape: Generated shape or list of generated shapes in
                             case of multi input models.

            batch_size: Batch size.

            data_percentage: Percentage of testing data to use.

            range_data: Dynamic range of input light field data.
                        Used to normalize the input data to a range [0, 1].
                        If no normalization is necessary, specify None.

            range_labels: Dynamic range of input label data.
                          May be used to normalize the input data to a range [0, 1].
                          If no normalization is necessary, specify None.
                          If a list of labels is used, specify ranges as list,
                          e.g. [255, None, None]

            use_mask: Whether to use a color coding mask.

            gpus: Integer or list of integers specifying the number of GPUs
                  or GPU IDs to use for training. Defaults to 1. If more than
                  one GPU is used, the model will be distributed across
                  multiple GPUs, i.e. the batch will be split up across
                  the GPUs.

            cpu_merge: Used when gpus > 1. Whether to force merging model
                       weights under the scope of the CPU or not.
                       Defaults to False (recommended for NV-Link)

            gen_kwargs: Passed to generator instantiation.

            **kwargs: Passed to :func:`tensorflow.keras.model.evaluate()`.

        Returns:
            Dictionary containing loss and metric test scores.
        """
        # For single input models, wrap shape in list
        generated_shape = shape_wrapper(generated_shape)

        # Create and build model if necessary
        if self.__build_necessary__(generated_shape):
            self.__build_model__(generated_shape,
                                 augmented_shape=augmented_shape,
                                 gpus=gpus,
                                 cpu_merge=cpu_merge)

        reshape_func = self.reshape_func

        # Init Generator
        gen_kwargs = gen_kwargs or {}
        test_gen_kwargs = dict(data=data,
                               data_key=data_key,
                               label_keys=label_keys,
                               augmented_shape=augmented_shape,
                               generated_shape=generated_shape,
                               reshape_func=reshape_func,
                               model_crop=self.model_crop,
                               batch_size=batch_size,
                               range_data=range_data,
                               range_labels=range_labels,
                               data_percentage=data_percentage,
                               augment=False,
                               shuffle=False,
                               use_mask=use_mask,
                               fix_seed=True,
                               **gen_kwargs)

        test_gen = self.generator(**test_gen_kwargs)

        # Evaluate on test dataset.
        test_vals = self.keras_model.evaluate(test_gen, **kwargs)

        # Create dict with metric=test_value pairs
        test_res = {key: val for key, val in zip(self.keras_model.metrics_names, test_vals)}

        return test_res

    def evaluate_challenges(self,
                            data,
                            data_key,
                            label_keys,
                            augmented_shape,
                            generated_shape,
                            range_data=None,
                            range_labels=None,
                            use_mask=False,
                            gen_kwargs: Optional[dict] = None,
                            model_weights: Optional[str] = None,
                            **kwargs) -> dict:
        """Evaluate dataset challenges.
        Challenges are full-sized inputs with ground truth labels that
        are used to test/evaluate a model in more depth and full-sized.

        Args:
            data: Data dictionary or path to test data .h5 file.

            data_key:  Key of light field data in test data file or dictionary..

            label_keys:  Keys of label in test data file or dictionary..

            augmented_shape: Shape after augmentation.
                             (Indirectly defines angular and spatial crop,
                             when smaller than input shapes)

            generated_shape: Generated shape or list of generated shapes in
                             case of multi input models.
            range_data: Dynamic range of input light field data.
                        Used to normalize the input data to a range [0, 1].
                        If no normalization is necessary, specify None.

            range_labels: Dynamic range of input label data.
                          May be used to normalize the input data to a range [0, 1].
                          If no normalization is necessary, specify None.
                          If a list of labels is used, specify ranges as list,
                          e.g. [255, None, None]

            use_mask: Whether to use a color coding mask.

            gen_kwargs: Passed to generator instantiation.

            model_weights: Optional path to saved model weights. If no path is
                           specified, and model has been previously trained,
                           use existing model weights.

            **kwargs: Passed to :func:`tensorflow.keras.model.predict()`.

        Returns:
            A dictionary containing a list of predictions (the keys are set
            corresponding to the output layer(s) name(s) and the
            corresponding list of metrics.
        """

        # For single input models, wrap shape in list
        generated_shape = shape_wrapper(generated_shape)

        if model_weights is None:
            if self.keras_model is not None:
                model_weights = self.keras_model.get_weights()
                put_weights = "set_weights"
            else:
                raise ValueError("'model_weights' need to be specified when "
                                 "model is not instantiated/trained yet.")
        else:
            put_weights = "load_weights"

        # Create and build model if necessary
        if self.__build_necessary__(generated_shape):
            self.__build_model__(generated_shape,
                                 augmented_shape=augmented_shape,
                                 gpus=1,
                                 cpu_merge=True)

        # Load weights either from previous model or from file
        if put_weights == "set_weights":
            self.keras_model.set_weights(model_weights)
        elif put_weights == "load_weights":
            self.keras_model.load_weights(model_weights)

        reshape_func = self.reshape_func

        # Init Generator
        gen_kwargs = gen_kwargs or {}
        pred_gen_kwargs = dict(data=data,
                               data_key=data_key,
                               label_keys=label_keys,
                               augmented_shape=augmented_shape,
                               generated_shape=generated_shape,
                               reshape_func=reshape_func,
                               model_crop=self.model_crop,
                               batch_size=1,
                               range_data=range_data,
                               range_labels=range_labels,
                               data_percentage=1,
                               augment=False,
                               shuffle=False,
                               use_mask=use_mask,
                               fix_seed=True,
                               **gen_kwargs)

        pred_gen = self.generator(**pred_gen_kwargs)

        # Predict on challenges, wrap in dict with output names
        pred_res = self.keras_model.predict(pred_gen, **kwargs)
        if type(pred_res) is not list:
            pred_res = [pred_res]
        pred_res = {name: [v for v in val] for name, val in zip(self.output_names, pred_res)}

        # Calculate metric scores for every challenge separately
        eval_res = [dict() for i in range(len(pred_gen))]
        for i in range(len(pred_gen)):

            lf_batch, labels = pred_gen.__getitem__(i)

            for output in self.output_names:
                for metric in self.metrics[output]:
                    y_pred = pred_res[output][i]
                    y_true = labels[output][0]  # batch_size = 1
                    metric.reset_states()
                    metric.update_state(y_true, y_pred)
                    res = metric.result().numpy()
                    eval_res[i][metric.name] = res

        return {**pred_res, "metrics": eval_res}

    def save(self, filepath, save_format="tf", overwrite=True, include_optimizer=True):
        """Save the full model, including optimizer, loss, etc.

        TODO: For this, the custom loss and metric functions need to implement
              proper deserialization via from_config and get_config.

        Args:
            filepath: Path to save the model

            save_format: Format of saving, either "tf" or "h5"

            overwrite: Whether to possible overwrite existing path.

            include_optimizer: Whether to include the optimizer upon saving.

        """

        # if self.keras_model is None:
        #     raise ValueError("Model has not been created yet. "
        #                      "Load or train the model first.")
        #
        # return self.keras_model.save(filepath,
        #                              save_format=save_format,
        #                              overwrite=overwrite,
        #                              include_optimizer=include_optimizer)

        raise NotImplementedError(
            "Saving and loading of the full model state is not yet supported. "
            "In the meantime, use save_weights or load_weights.")

    def load(self, filepath, compile=True):
        """Load the full model, including optimizer, loss, etc.

        TODO: For this, the custom loss and metric functions need to implement
              proper deserialization via from_config and get_config.

        Args:
            filepath: Path to save the model.

            compile: Whether to compile the loaded model.

        Returns:
            A LFCNN model with properly loaded Keras model instance.

        """

        # if self.keras_model is not None:
        #     raise ValueError("Model already loaded.")
        #
        # self._keras_model = keras.models.load_model(filepath, compile=False)
        # if compile:
        #     self.keras_model.compile(optimizer=self._optimizer,
        #                              loss=self._loss,
        #                              metrics=self._metrics)
        # return

        raise NotImplementedError(
            "Saving and loading of the full model state is not yet supported. "
            "In the meantime, use save_weights or load_weights.")

    def save_weights(self, filepath, overwrite=True):

        if self.keras_model is None:
            raise ValueError("Model has not been created yet. "
                             "Load or train the model first.")

        return self.keras_model.save_weights(filepath, overwrite)

    def load_weights(self, filepath, generated_shape, augmented_shape, **kwargs):
        # For single input models, wrap shape in list
        generated_shape = shape_wrapper(generated_shape)

        # Build model, if not set
        if self.__build_necessary__(generated_shape):
            self.__build_model__(generated_shape=generated_shape,
                                 augmented_shape=augmented_shape)

        return self.keras_model.load_weights(filepath, **kwargs)


class DummyStrategy:
    """This class provides a dummy strategy with a scope() context manager.

    When using single device training, avoids the use of TF
    distributed strategies which are necessary for multi GPU training.

    TODO: Is there a nicer solution to this?
    """

    def __init__(self):
        return

    @contextmanager
    def scope(self):
        yield None
