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


"""Encoder-decoder network based on 3D convolution for estimating
disparity and a central view from spectrally coded light fields.
"""
from typing import List

import tensorflow.keras as keras

from lfcnn.models import BaseModel
from lfcnn.generators import CentralAndDisparityGenerator
from lfcnn.generators.reshapes import lf_subaperture_channel_stack
from lfcnn.layers import res_block_3d, res_block_2d
from lfcnn.layers import sample_down_3d, sample_up_2d
from lfcnn.layers import reshape_3d_to_2d


class Conv3dDecode2d(BaseModel):

    def __init__(self, **kwargs):
        super(Conv3dDecode2d, self).__init__(**kwargs)

    def set_generator_and_reshape(self):
        self._generator = CentralAndDisparityGenerator
        self._reshape_func = lf_subaperture_channel_stack
        return

    def create_model(self, inputs: List[keras.Input], augmented_shape=None) -> keras.Model:
        # Single input model
        input = inputs[0]

        downsample_strides = 2
        upsample_strides = 2

        kernel_reg = keras.regularizers.l2(1e-4)

        # Encoder
        x = keras.layers.Conv3D(filters=32, kernel_size=3, strides=1, padding='same',
                   kernel_initializer='he_normal',
                   kernel_regularizer=kernel_reg)(input)
        x = sample_down_3d(x, 64, strides=downsample_strides, kernel_regularizer=kernel_reg)
        x = res_block_3d(x, 64, kernel_regularizer=kernel_reg)
        x = sample_down_3d(x, 128, strides=downsample_strides, kernel_regularizer=kernel_reg)
        x = res_block_3d(x, 128, kernel_regularizer=kernel_reg)
        x = sample_down_3d(x, 256, strides=downsample_strides, kernel_regularizer=kernel_reg)
        x = reshape_3d_to_2d(x)

        # Decoder disparity
        x1 = sample_up_2d(x, 256, strides=upsample_strides, kernel_regularizer=kernel_reg)
        x1 = res_block_2d(x1, 256, kernel_regularizer=kernel_reg)
        x1 = sample_up_2d(x1, 128, strides=upsample_strides, kernel_regularizer=kernel_reg)
        x1 = res_block_2d(x1, 128, kernel_regularizer=kernel_reg)
        x1 = sample_up_2d(x1, 64, strides=upsample_strides, kernel_regularizer=kernel_reg)
        x1 = res_block_2d(x1, 64, kernel_regularizer=None)
        x1 = keras.layers.Conv2D(filters=1, kernel_size=1, strides=1,
                                 padding='valid',
                                 kernel_initializer='he_normal',
                                 kernel_regularizer=None,
                                 dtype='float32',  # set explicitly for mixed precision case
                                 name='disparity')(x1)

        # Decoder central_view
        x2 = sample_up_2d(x, 256, strides=upsample_strides, kernel_regularizer=kernel_reg)
        x2 = res_block_2d(x2, 256, kernel_regularizer=kernel_reg)
        x2 = sample_up_2d(x2, 128, strides=upsample_strides, kernel_regularizer=kernel_reg)
        x2 = res_block_2d(x2, 128, kernel_regularizer=kernel_reg)
        x2 = sample_up_2d(x2, 64, strides=upsample_strides, kernel_regularizer=kernel_reg)
        x2 = res_block_2d(x2, 64, kernel_regularizer=kernel_reg)
        x2 = keras.layers.Conv2D(filters=augmented_shape[-1], kernel_size=1, strides=1,
                                 padding='valid',
                                 kernel_initializer='he_normal',
                                 kernel_regularizer=None,
                                 dtype='float32',  # set explicitly for mixed precision case
                                 name='central_view')(x2)

        return keras.Model(input, [x1, x2], name="Conv3dDecode2D")
