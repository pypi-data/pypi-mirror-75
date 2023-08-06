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


"""Light field autoencoder using 3d convolution.
This model is mostly analogous to the autoencoder path of the encoder-decoder
network proposed by [1] but instead of using to EPI volumes, we use the full
light field as the networks input. Also, we perform one less downsampling
and upsampling operation.

[1] Alperovich, Anna, et al.
"Light field intrinsics with a deep encoder-decoder network."
IEEE Conference on Computer Vision and Pattern Recognition.
2018.
"""
from typing import List

import tensorflow.keras as keras
import tensorflow.keras.backend as K
from tensorflow.keras.layers import Activation, Add, BatchNormalization, Reshape
from tensorflow.keras.layers import Conv3D, Conv3DTranspose

from lfcnn.models import BaseModel
from lfcnn.generators import LfGenerator
from lfcnn.generators.reshapes import lf_subaperture_channel_stack


class Conv3dModel(BaseModel):

    def __init__(self, **kwargs):

        super(Conv3dModel, self).__init__(**kwargs)

    def set_generator_and_reshape(self):
        self._generator = LfGenerator
        self._reshape_func = lf_subaperture_channel_stack
        return

    def create_model(self, inputs: List[keras.Input], augmented_shape=None) -> keras.Model:
        # Single input model
        x = inputs[0]

        # Encoder
        x = self.res_block_3d(x, num_filters=24)
        x = self.res_block_3d(x, num_filters=24)
        x = self.res_block_3d(x, num_filters=24, strides=(2, 2, 3))

        x = self.res_block_3d(x, num_filters=32)
        x = self.res_block_3d(x, num_filters=32)
        x = self.res_block_3d(x, num_filters=32, strides=(2, 2, 3))

        x = self.res_block_3d(x, num_filters=64)
        x = self.res_block_3d(x, num_filters=64)
        x = self.res_block_3d(x, num_filters=64, strides=(2, 2, 3))

        # Decoder
        x = self.res_block_3d_transposed(x, num_filters=64, strides=(2, 2, 3))
        x = self.res_block_3d(x, num_filters=64)
        x = self.res_block_3d(x, num_filters=64)

        x = self.res_block_3d_transposed(x, num_filters=32, strides=(2, 2, 3))
        x = self.res_block_3d(x, num_filters=32)
        x = self.res_block_3d(x, num_filters=32)

        x = self.res_block_3d_transposed(x, num_filters=24, strides=(2, 2, 3))
        x = self.res_block_3d(x, num_filters=24)
        x = self.res_block_3d(x, num_filters=24)

        x = Conv3D(filters=3, kernel_size=3, padding='same')(x)
        x = self.final_reshape(x, augmented_shape, name='light_field')

        return keras.Model(inputs, x, name="Conv3dAutoEncoder")

    @staticmethod
    def res_block_3d(x, num_filters, kernel_size=(3, 3, 3), strides=(1, 1, 1),
                     kernel_regularizer=None, name=None):
        # Convolutional path
        x1 = Conv3D(filters=num_filters, kernel_size=kernel_size,
                    padding='same', kernel_initializer='he_normal',
                    kernel_regularizer=kernel_regularizer)(x)
        x1 = BatchNormalization()(x1)
        x1 = Activation('relu')(x1)
        x1 = Conv3D(filters=num_filters, kernel_size=kernel_size,
                    padding='same', strides=strides,
                    kernel_initializer='he_normal',  kernel_regularizer=kernel_regularizer)(x1)
        x1 = BatchNormalization()(x1)

        # Residual connection
        x2 = Conv3D(filters=num_filters, kernel_size=(1, 1, 1), padding='same',
                    strides=strides, kernel_initializer='he_normal',
                    kernel_regularizer=kernel_regularizer)(x)
        return Add(name=name)([x1, x2])


    @staticmethod
    def res_block_3d_transposed(x, num_filters, kernel_size=(3, 3, 3), strides=(2, 2, 3),
                                kernel_regularizer=None, name=None):
        # Convolutional path
        x1 = Conv3DTranspose(filters=num_filters, kernel_size=kernel_size,
                             strides=strides,
                             padding='same', kernel_initializer='he_normal',
                             kernel_regularizer=kernel_regularizer)(x)
        x1 = BatchNormalization()(x1)
        x1 = Activation('relu')(x1)
        x1 = Conv3D(filters=num_filters, kernel_size=kernel_size, padding='same',
                    kernel_initializer='he_normal',
                    kernel_regularizer=kernel_regularizer)(x1)
        x1 = BatchNormalization()(x1)

        # Residual connection
        x2 = Conv3DTranspose(filters=num_filters, kernel_size=(1, 1, 1), padding='same',
                             strides=strides, kernel_initializer='he_normal',
                             kernel_regularizer=kernel_regularizer)(x)
        return Add(name=name)([x1, x2])

    @staticmethod
    def final_reshape(input, augmented_shape, name='light_field'):
        """Spatial to light field reshape.
        Only works when u==v.
        """
        u, v, s, t, ch = augmented_shape
        return Reshape((u, v, s, t, ch), name=name)(input)
