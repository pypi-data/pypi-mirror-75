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


"""lfcnn tensorflow utils
"""
from typing import Union

import tensorflow as tf
from tensorflow.keras.optimizers import Optimizer


def list_visible_devices(type=None):
    return tf.config.list_logical_devices(type if type is None else type.upper())


def list_physical_devices(type=None):
    return tf.config.list_physical_devices(type if type is None else type.upper())


def use_cpu():
    """Set CPU as visible tf device.
    This effectively hides all available GPUs.
    """
    # Set CPU
    cpus = tf.config.list_physical_devices('CPU')
    tf.config.set_visible_devices(cpus[0], 'CPU')
    # Hide GPU
    tf.config.set_visible_devices([], 'GPU')


def use_gpu(index=None):
    """Set GPU as visible tf device.

    Args:
        index: Set index of visible GPU. If None, all GPUs are visible to TF.

    """
    gpus = tf.config.list_physical_devices('GPU')
    gpus = gpus if index is None else gpus[index]

    if gpus:
        try:
            tf.config.experimental.set_visible_devices(gpus, 'GPU')
        except RuntimeError or IndexError as e:
            print(e)


def disable_eager():
    """Disables TF eager execution.
    By default in TF >= 2.0, eager execution is enabled."""
    return tf.compat.v1.disable_eager_execution()


def set_mixed_precision_keras(policy: str = 'mixed_float16',
                              loss_scale: Union[float, str] = 'dynamic'):
    """Set to use the Keras mixed precision api.
    Simply call at the beginning of your script.

    See Also:
        https://www.tensorflow.org/guide/mixed_precision

    Args:
        policy: Mixed precision dtype policy. Default: 'mixed_float16'.
                See tf.keras.mixed_precision.experimental.Policy for available
                dtype policies.

        loss_scale: : Loss scale value or loss scale method. Default: 'dynamic'.

    """
    from tensorflow.keras.mixed_precision import experimental as mixed_precision
    pol = mixed_precision.Policy(policy, loss_scale)
    mixed_precision.set_policy(pol)
    print(f'Mixed Precision: Using compute dtype: {pol.compute_dtype}')
    print(f'Mixed Precision: Using variable dtype: {pol.variable_dtype}')
    print(f'Mixed Precision: Using loss scale: {pol.loss_scale}')

    return


def mixed_precision_graph_rewrite(opt: Optimizer,
                                  loss_scale: str = 'dynamic') -> Optimizer:
    """Using a graph rewrite to enable mixed precision training.
    Use with care. The Keras API :func:`.set_mixed_precision_keras` is
    the prefered method for mixed precision training.
    See Also:
        https://www.tensorflow.org/api_docs/python/tf/train/experimental/enable_mixed_precision_graph_rewrite

    Args:
        opt: Keras optimizer instance.

        loss_scale: Lass scale method. Default: 'dynamic'.

    Returns:
        Optimizer with mixed precision graph rewrite enabled.
    """
    return tf.train.experimental.enable_mixed_precision_graph_rewrite(opt, loss_scale)
