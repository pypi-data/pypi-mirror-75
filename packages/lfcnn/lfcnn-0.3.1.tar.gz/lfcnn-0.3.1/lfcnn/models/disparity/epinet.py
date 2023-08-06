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


"""EPINET disparity estimator model.

Shin, Changha, et al.
"Epinet: A fully-convolutional neural network using epipolar geometry
for depth from light field images."
Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition.
2018.
"""
from typing import List

import tensorflow.keras as keras
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import BatchNormalization, Concatenate

from lfcnn.models import BaseModel
from lfcnn.generators import DisparityGenerator
from lfcnn.generators.reshapes import lf_crosshair_stacked


class Epinet(BaseModel):

    def __init__(self, **kwargs):
        super(Epinet, self).__init__(**kwargs)

    def set_generator_and_reshape(self):
        self._generator = DisparityGenerator
        self._reshape_func = lf_crosshair_stacked
        return

    def create_model(self, inputs: List[keras.Input], augmented_shape=None) -> keras.Model:
        horz, vert, diag1, diag2 = inputs

        mid1 = Epinet.base_block(horz, kernel_size=2, num_filters=70, reps=3, name='horz')
        mid2 = Epinet.base_block(vert, kernel_size=2, num_filters=70, reps=3, name='vert')
        mid3 = Epinet.base_block(diag1, kernel_size=2, num_filters=70, reps=3, name='diag1')
        mid4 = Epinet.base_block(diag2, kernel_size=2, num_filters=70, reps=3, name='diag2')

        out = Concatenate(axis=-1, name='mid_merged')([mid1, mid2, mid3, mid4])
        out = Epinet.base_block(out, kernel_size=2, num_filters=280, reps=8, name='merge')

        out = Conv2D(filters=1, kernel_size=2, strides=1, padding='valid', name='last_conv1')(out)
        out = Activation('relu', name='last_relu')(out)
        out = Conv2D(filters=1, kernel_size=2, strides=1, padding='valid', name='disparity')(out)

        input_shape = horz.get_shape().as_list()
        output_shape = out.get_shape().as_list()
        self._model_crop = (input_shape[1] - output_shape[1])//2, (input_shape[2] - output_shape[2])//2

        return keras.Model(inputs, out, name="Epinet")

    @staticmethod
    def base_block(input, kernel_size, num_filters, reps, name):
        x = input
        for i in range(reps):
            x = Conv2D(filters=num_filters, kernel_size=kernel_size, strides=1,
                       padding='valid', name=name + f"_convA_{i}")(x)
            x = Activation('relu', name=name + f"_reluA_{i}")(x)
            x = Conv2D(filters=num_filters, kernel_size=kernel_size, strides=1,
                       padding='valid', name=name + f"_convB_{i}")(x)
            x = BatchNormalization(name=name + f"_bn_{i}")(x)
            x = Activation('relu', name=name + f"_reluB_{i}")(x)
        return x
