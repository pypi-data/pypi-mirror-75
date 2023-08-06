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


"""Light field 2 output dummy model.
"""
from typing import List

import tensorflow.keras as keras
from tensorflow.keras.layers import Activation, Reshape, Conv2D

from lfcnn.models import BaseModel
from lfcnn.layers import res_block_2d
from lfcnn.generators import CentralAndDisparityGenerator
from lfcnn.generators.reshapes import lf_subaperture_stack


class Dummy(BaseModel):

    def __init__(self, depth=0, **kwargs):

        super(Dummy, self).__init__(**kwargs)
        self._depth = depth

    @property
    def depth(self):
        return self._depth

    def set_generator_and_reshape(self):
        self._generator = CentralAndDisparityGenerator
        self._reshape_func = lf_subaperture_stack
        return

    def create_model(self, inputs: List[keras.Input], augmented_shape) -> keras.Model:
        # Single input model
        x = inputs[0]
        u, v, s, t, ch = augmented_shape

        for i in range(self.depth):
            x = res_block_2d(x, 64)

        x = Activation('relu')(x)


        x1 = Conv2D(filters=ch, kernel_size=1, padding='same')(x)
        x2 = Conv2D(filters=1, kernel_size=1, padding='same')(x)

        central_view = self.final_reshape_central_view(x1, augmented_shape, name='central_view')
        disparity = self.final_reshape_disparity(x2, augmented_shape, name='disparity')

        return keras.Model(inputs, [central_view, disparity], name="Dummy")

    @staticmethod
    def final_reshape_central_view(input, augmented_shape,name='reshape'):
            """Reshape to central view
            """
            u, v, s, t, ch = augmented_shape
            return Reshape((s, t, ch), name=name)(input)

    @staticmethod
    def final_reshape_disparity(input, augmented_shape,name='reshape'):
            """Reshape to disparity
            """
            u, v, s, t, ch = augmented_shape
            return Reshape((s, t, 1), name=name)(input)