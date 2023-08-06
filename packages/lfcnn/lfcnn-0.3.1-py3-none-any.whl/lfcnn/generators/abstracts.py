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

from pathlib import Path
from typing import Optional, Union, Tuple, List, Callable

import tensorflow.keras as keras
import numpy as np
import h5py

from .utils import _to_list, AUGMENTATIONS, shape_wrapper
from .utils import lf_batch_code, model_crop_spatial


class BaseGenerator(keras.utils.Sequence):

    def __init__(self,
                 data: Union[str, dict],
                 data_key: str,
                 label_keys: Optional[Union[str, List[str]]],
                 augmented_shape: Tuple[int, int, int, int, int],
                 generated_shape: List[Tuple[int, ...]],
                 reshape_func: Callable,
                 batch_size: int,
                 range_data: Optional[Union[float, int]] = None,
                 range_labels: Optional[Union[float, List[Union[float, None]]]] = None,
                 data_percentage: float = 1.0,
                 model_crop: Optional[tuple] = None,
                 augment: Union[bool, dict] = False,
                 shuffle: bool = False,
                 use_mask: bool = False,
                 fix_seed: bool = False):
        """

        Args:
            data:            Either a system path to a dataset .h5 file or
                             an already loaded dictionary containing data and
                             possibly labels. The data needs to be in the shape
                             (N, u, v, s, t, num_ch), where N is the total
                             number of available data, (u, v) is the
                             angular, (s, t) the spatial and (num_ch) the
                             spectral shape of the light field.

            data_key:        Key of the data in the .h5 file.

            label_keys:      Key or list of keys of the corresponding label(s).
                             Specify None, if no label is read from the .h5 file.

            augmented_shape: Shape of the light field after augmentation.
                             Must be of form (u, v, s, t, lambda).
                             Here, (u, v) is the angular, (s, t) the spatial
                             and lambda the color or spectral component.
                             The angular component should be odd-valued.
                             This guarantees the existence of a well-defined
                             central view.

            generated_shape: List of Shapes of the light field that the generator
                             generates. Can be a single element list for
                             single input models.

            reshape_func:    A reshape function. Reshapes the light field
                             (and possibly the labels) into the final,
                             desired shape. Performs the transformation
                             from augmented_shape to generated_shape.

            batch_size:      Size of the batches to generate.
                             Depending on the amount of data, the very last
                             batch of an epoch might be smaller.

            num_labels:      Number of labels that the generator generates.
                             This can be more than the length of label_keys,
                             for example when labels are created dynamically.

            range_data:      Dynamic range of the input data. If not None,
                             the data is normalized (divided by range_data).

            range_labels:    List of dynamic ranges of the input labels.
                             If not None, the corresponding label is
                             normalized (divided by range_label[i]).
                             Length of the list has to match num_labels.

            data_percentage: Decimal percentage of data to use.

            model_crop:      For models with spatial cropping, e.g. due to
                             'valid' padding, specify the crop (c_s, c_t)
                             that is cropped from the spatial borders.

            augment:         Whether to perform online augmentation.
                             Either a single bool, or dictionary of bool values
                             for every available augmentation key, see
                             lfcnn.generator.utils.AUGMENTATIONS

            shuffle:         Whether to shuffle the indices.
                             The current epoch is used as a seed to be reproducible
                             and to guarantee that the same shuffle across multiple
                             processes when multiprocessing is used.
                             Note that shuffling decreases the reading speed
                             (in particular when reading from a file) and might
                             limit the training performance.

            use_mask:        Whether to apply a random coding mask to the
                             input data.

            fix_seed:      Whether to use a constant seed for random ops.
                             Can be set to obtain reproducible results,
                             most importantly for validation and testing
                             generators.
        """
        # Prepare data
        self._data = data
        self._data_key = data_key
        self._range_data = range_data
        self._label_keys = _to_list(label_keys) if label_keys is not None else label_keys
        self._data_percentage = data_percentage

        # Label names should be used for multi-label outputs and
        # should be set by a specific generator
        self._label_names = None
        self._range_labels = _to_list(range_labels) if range_labels is not None else range_labels
        self._input_shape = None
        self._total_len = None

        # Depending on input type, read data from .h5 file or dict
        if type(self.data) == dict:
            self.read_curr_data = self.read_curr_data_dict
            self._total_len = int(data[self.data_key].shape[0] * self.data_percentage)
            self._input_shape = data[self.data_key][0].shape

        elif type(self.data) == str or issubclass(type(self.data), Path):
            self.read_curr_data = self.read_curr_data_path
            # Get data length
            with h5py.File(self.data, 'r', libver='latest', swmr=False) as hf:
                # Calculate total number of data points and get input shape
                self._total_len = int(hf[self.data_key].shape[0] * self.data_percentage)
                self._input_shape = hf[self.data_key][0].shape

        else:
            raise TypeError("Data needs to be a dict or file system path (str or Path).")

        if self.input_shape is None or self.total_len is None:
            raise ValueError("Something went wrong reading the data file.")

        self._augmented_shape = augmented_shape
        self._generated_shape = shape_wrapper(generated_shape)
        self._model_crop = model_crop

        self._reshape = reshape_func
        self._batch_size = batch_size

        if data_percentage > 1.0:
            raise ValueError("Found data_percentage > 1.0. Use a value between 0 and 1.")

        if type(augment) == bool:
            self._augment = {key: augment for key in AUGMENTATIONS}
        else:
            unknown = [k for k in augment if k not in AUGMENTATIONS]
            missing = [k for k in AUGMENTATIONS if k not in augment]

            if len(missing) > 0:
                raise ValueError(f"Missing augmentation key(s) {missing}")

            if len(unknown) > 0:
                raise ValueError(f"Unknown augmentation key(s) {unknown}")

            self._augment = augment

        self._shuffle = shuffle
        self._use_mask = use_mask
        self._fix_seed = fix_seed

        # Create array of indices of full dataset
        self._indices = np.arange(self.total_len)
        self._epoch = 1

        # Check that there is enough data
        if self.total_len < self.batch_size:
            raise ValueError(f"Insufficient number of data points. Found "
                             f"{self.total_len} for a batch size of {self.batch_size}.")

        # Check that augmented shape and input shape are compatible
        if not all(x <= y for x, y in zip(self.augmented_shape, self.input_shape)):
            raise ValueError(f"Incompatible augmented shape {self.augmented_shape} "
                             f"and input shape {self.input_shape}.")

        # Shuffle now and at the end of each epoch.
        if self.shuffle:
            self.shuffle_idx()
        return

    def __len__(self):
        """Denotes the number of batches per epoch. """
        return int(self.total_len / self.batch_size)

    def __getitem__(self, index):
        """Generate one batch of data and label(s)

        Returns:
            Tuple data, dict(label_name=label, ...) where multi-label
            outputs are passed as a dictionary.
        """

        # Create batch_size indices for current batch
        curr_indices = list(self.indices[index * self.batch_size:(index + 1) * self.batch_size])

        # If data is shuffled, use list of ints for reading
        if self.shuffle:
            # Indices must be in ascending order for fancy indexing
            curr_indices.sort()
            indices_read = curr_indices

        # Otherwise, use a slice to increase reading/processing performance
        else:
            indices_read = slice(index*self.batch_size, (index + 1)*self.batch_size)

        # Read sample and labels from .h5 file
        lf_batch, labels = self.read_curr_data(indices_read)

        # Normalize using specified ranges
        if self.range_data is not None:
            lf_batch /= self.range_data

        num_labels = len(labels)

        if self.range_labels is not None:

            if len(self.range_labels) != num_labels:
                raise ValueError(f"Expected {num_labels} range_labels, got {len(self.range_labels)}.")

            for i, range_label in enumerate(self.range_labels):
                if range_label is not None:
                    # In-place division might not be possible for integer types
                    labels[i] = labels[i].astype(np.float32) / range_label

        # Process sample and labels. Note that the length of labels can change here
        lf_batch, labels = self.process_data(lf_batch, labels, curr_indices)

        # Code light field batch
        if self.use_mask:
            lf_batch = lf_batch_code(lf_batch=lf_batch,
                                     curr_indices=curr_indices,
                                     fix_seed=self.fix_seed)

        # Finally, reshape the data and labels
        # Supports multi input, multi output
        lf_batch, labels = self.reshape_data(lf_batch, labels)

        # Safety check for output shape, lf_batch is list of input batches
        if type(lf_batch) != dict:
            if not lf_batch.shape[1:] == self.generated_shape[0]:
                raise ValueError("The generated data does not have the desired shape. "
                                 f"Found {lf_batch.shape[1:]}, expected {self.generated_shape[0]}.")
        else:
            for lf_b, shape in zip(lf_batch.values(), self.generated_shape):
                if not lf_b.shape[1:] == shape:
                    raise ValueError("The generated data does not have the desired shape. "
                                     f"Found {lf_b.shape[1:]}, expected {shape}.")

        # If specified, crop labels according to model_crop
        # This is useful for models with 'valid' padding that change the shape
        if self.model_crop is not None:
            labels = model_crop_spatial(labels, self.model_crop)

        # Return a dictionary of labelname/label pairs.
        # Create default label names, if not set.
        num_labels = len(labels)
        if self.label_names is None:
            self._label_names = ["output_" + str(i) for i in range(num_labels)]
        elif len(self.label_names) != num_labels:
            raise ValueError(f"Expected {num_labels} label_names, got {len(self.label_names)}.")

        return lf_batch, {name: label for (name, label) in zip(self.label_names, labels)}

    def on_epoch_end(self):
        """Is called by Keras at the end of each epoch."""
        self._epoch += 1
        if self.shuffle:
            self.shuffle_idx()

    @property
    def data(self):
        return self._data

    @property
    def data_key(self):
        return self._data_key

    @property
    def label_keys(self):
        return self._label_keys

    @property
    def label_names(self):
        return self._label_names

    @property
    def range_data(self):
        return self._range_data

    @property
    def range_labels(self):
        return self._range_labels

    @property
    def input_shape(self):
        return self._input_shape

    @property
    def augmented_shape(self):
        return self._augmented_shape

    @property
    def generated_shape(self) -> list:
        return self._generated_shape

    @property
    def total_len(self):
        return self._total_len

    @property
    def indices(self):
        return self._indices

    @property
    def batch_size(self):
        return self._batch_size

    @property
    def model_crop(self):
        return self._model_crop

    @property
    def epoch(self):
        return self._epoch

    @property
    def data_percentage(self):
        return self._data_percentage

    @property
    def augment(self):
        return self._augment

    @property
    def shuffle(self):
        return self._shuffle

    @property
    def use_mask(self):
        return self._use_mask

    @property
    def fix_seed(self):
        return self._fix_seed

    def read_curr_data_path(self,
                            indices_read: Union[List[int], slice]) -> Tuple[any, List[any]]:
        """Read a batch of sample and label(s) from .h5 file.

    Args:
        indices_read: List of indices or slice to read.

        Returns:
            sample: A batch of data (light fields) read from the .h5 file.
            labels: A list of labels read from the .h5 file.
        """

        with h5py.File(self.data, 'r', libver='latest', swmr=False) as hf:
            lf_batch = hf[self.data_key][indices_read].astype('float32')

            if self.label_keys is not None:
                labels = [hf[label_key][indices_read]for label_key in self.label_keys]
            else:
                labels = []

        return lf_batch, labels

    def read_curr_data_dict(self,
                            indices_read: Union[List[int], slice]) -> Tuple[any, List[any]]:
        """Read a batch of sample and label(s) from a data dictionary.

    Args:
        indices_read: List of indices or slice to read.

        Returns:
            sample: A batch of data (light fields) read from the data dict.
            labels: A list of labels read from the data dict.
        """

        lf_batch = self.data[self.data_key][indices_read].astype('float32')

        if self.label_keys is not None:
            labels = [self.data[label_key][indices_read] for label_key in self.label_keys]
        else:
            labels = []

        return lf_batch, labels

    def process_data(self,
                     lf_batch: any,
                     labels: List[any],
                     curr_indices: List[int]) -> Tuple[any, List[any]]:
        """Processes a batch of sample and labels.

        Args:

            lf_batch: Batch of light fields.

            labels: Batch of corresponding labels.

            curr_indices: List of current sample indices.

        Returns:
            Tuple of lf_batch, labels.
            The number of labels returned does not have to match the number
            of input labels, for example when labels are created from the
            light field batch itself (such as using the central view or the
            full light field as a label for an auto-encoder).
        """
        raise NotImplementedError("This needs to be implemented by a derived class.")

    def reshape_data(self,
                     lf_batch: any,
                     labels: List[any]) -> Tuple[any, List[any]]:
        """Reshape a batch of light fields and labels.

        Args:
            lf_batch: Batch of light fields.

            labels: Batch of corresponding labels.

        Returns:
            Tuple of reshaped light field batch, labels.
        """
        return self._reshape(lf_batch, labels)

    def shuffle_idx(self):
        # Set epoch number as seed for same shuffle across multiple processes
        np.random.seed(self.epoch)
        np.random.shuffle(self._indices)
        # Reset seed
        np.random.seed(None)
        return
