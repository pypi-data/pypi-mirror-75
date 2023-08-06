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


"""Disparity estimator based on a 2D residual conv. encoder-decoder network.
"""
from typing import List

import tensorflow.keras as keras

from lfcnn.models import BaseModel
from lfcnn.generators import DisparityGenerator
from lfcnn.generators.reshapes import lf_subaperture_stack
from lfcnn.layers import res_block_2d, sample_down_2d, sample_up_2d


class Conv2dModel(BaseModel):

    def __init__(self, **kwargs):
        super(Conv2dModel, self).__init__(**kwargs)

    def set_generator_and_reshape(self):
        self._generator = DisparityGenerator
        self._reshape_func = lf_subaperture_stack
        return

    def create_model(self, inputs: List[keras.Input], augmented_shape=None) -> keras.Model:
        # Single input model
        input = inputs[0]

        downsample_strides = (2, 2)
        upsample_strides = (2, 2)
        reg = keras.regularizers.l2(1e-4)

        # Encoder
        x = res_block_2d(input, 256, kernel_regularizer=None)
        x = sample_down_2d(x, 288, strides=downsample_strides, kernel_regularizer=reg)
        x = res_block_2d(x, 288)
        x = sample_down_2d(x, 320, strides=downsample_strides, kernel_regularizer=reg)
        x = res_block_2d(x, 320)
        x = sample_down_2d(x, 352, strides=downsample_strides, kernel_regularizer=reg)

        x = res_block_2d(x, 384)

        # Decoder disparity
        x = sample_up_2d(x, 256, strides=upsample_strides, kernel_regularizer=reg)
        x = res_block_2d(x, 256)
        x = sample_up_2d(x, 128, strides=upsample_strides, kernel_regularizer=reg)
        x = res_block_2d(x, 128)
        x = sample_up_2d(x, 64, strides=upsample_strides, kernel_regularizer=reg)
        x = res_block_2d(x, 64, kernel_regularizer=None)
        x = res_block_2d(x, 3, kernel_regularizer=None)
        x = keras.layers.Conv2D(filters=1, kernel_size=1, strides=1,
                                padding='same',
                                kernel_initializer='he_normal',
                                kernel_regularizer=None,
                                name='disparity')(x)

        return keras.Model(input, [x], name="Conv2dDisparityEstimator")
