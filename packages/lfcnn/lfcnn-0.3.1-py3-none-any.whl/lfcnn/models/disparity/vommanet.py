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


"""VommaNet disparity estimator model.

CAUTION: The paper does not specify the number of filters in the first
layer of the dilation block. Feel free to play around with
that number.

Ma, Haoxin, et al.
"VommaNet: an End-to-End Network for Disparity Estimation from Reflective and
Texture-less Light Field Images."
arXiv preprint arXiv:1811.07124 (2018).
"""
from typing import List

import tensorflow.keras as keras
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Conv2D, SeparableConv2D
from tensorflow.keras.layers import BatchNormalization, Concatenate, Add

from lfcnn.models import BaseModel
from lfcnn.generators import DisparityGenerator
from lfcnn.generators.reshapes import lf_subaperture_stack


class VommaNet(BaseModel):

    def __init__(self, **kwargs):
        super(VommaNet, self).__init__(**kwargs)

    def set_generator_and_reshape(self):
        self._generator = DisparityGenerator
        self._reshape_func = lf_subaperture_stack
        return

    def create_model(self, inputs: List[keras.Input], augmented_shape=None) -> keras.Model:
        # Single input model
        input = inputs[0]

        x = self.dilation_block(input, num_filters=1, kernel_size=3)
        x = self.concat_block(x, num_filters=256, kernel_size=3)

        for _ in range(8):
            x = self.res_block(x, num_filters=128, kernel_size=3)

        x = self.final_block(x, num_filters=128, kernel_size=3)

        return keras.Model(inputs, x, name="VommaNet")

    @staticmethod
    def dilation_block(input, num_filters, kernel_size):

        x1 = Conv2D(filters=num_filters, kernel_size=kernel_size, dilation_rate=1,
                    padding='same', name='dil_1')(input)
        x2 = Conv2D(filters=num_filters, kernel_size=kernel_size, dilation_rate=2,
                    padding='same', name='dil_2')(input)
        x3 = Conv2D(filters=num_filters, kernel_size=kernel_size, dilation_rate=4,
                    padding='same', name='dil_4')(input)
        x4 = Conv2D(filters=num_filters, kernel_size=kernel_size, dilation_rate=8,
                    padding='same', name='dil_8')(input)
        x5 = Conv2D(filters=num_filters, kernel_size=kernel_size, dilation_rate=16,
                    padding='same', name='dil_16')(input)

        return [x1, x2, x3, x4, x5]

    @staticmethod
    def concat_block(inputs, num_filters, kernel_size):

        x = Concatenate()(inputs)
        x = SeparableConv2D(filters=num_filters, kernel_size=kernel_size,
                            padding='same', name='concat_conv')(x)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)

        return x

    @staticmethod
    def res_block(input, num_filters, kernel_size):

        x1 = SeparableConv2D(filters=num_filters, kernel_size=kernel_size, padding='same')(input)
        x1 = BatchNormalization()(x1)
        x1 = Activation('relu')(x1)

        x1 = SeparableConv2D(filters=num_filters, kernel_size=kernel_size, padding='same')(x1)
        x1 = BatchNormalization()(x1)
        x1 = Activation('relu')(x1)

        x1 = SeparableConv2D(filters=num_filters, kernel_size=kernel_size, padding='same')(x1)
        x1 = BatchNormalization()(x1)

        # Residual connection
        x2 = SeparableConv2D(filters=num_filters, kernel_size=1, padding='same')(input)

        return Add()([x1, x2])


    @staticmethod
    def final_block(input, num_filters, kernel_size):

        x = SeparableConv2D(filters=num_filters, kernel_size=kernel_size, padding='same')(input)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        x = SeparableConv2D(filters=1, kernel_size=1, padding='same', name='disparity')(x)

        return x
