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


"""Light field superresolution model using Spatial-Angular Separable (SAS)
Convolution.

See:

Yeung, Henry Wing Fung, et al.
"Light field spatial super-resolution using deep efficient spatial-angular
separable convolution."
IEEE Transactions on Image Processing 28.5 (2018): 2319-2330.
"""
from typing import List

import tensorflow.keras as keras
import tensorflow.keras.backend as K
from tensorflow.keras.layers import TimeDistributed, Permute, Reshape, Add
from tensorflow.keras.layers import Conv2D, Conv2DTranspose
from tensorflow.keras.layers import LeakyReLU

from lfcnn.models import BaseModel
from lfcnn.generators import LfDownSampleGenerator
from lfcnn.generators.reshapes import lf_distributed


class SasConv(BaseModel):

    def __init__(self, L=3, **kwargs):
        """

        Args:
            L: Number of SAS layers.
        """
        super(SasConv, self).__init__(**kwargs)
        self.L = L

    def set_generator_and_reshape(self):
        self._generator = LfDownSampleGenerator
        self._reshape_func = lf_distributed
        return

    def create_model(self, inputs: List[keras.Input], augmented_shape=None) -> keras.Model:
        # Single input model
        input = inputs[0]

        # SAS path
        x = TimeDistributed(
            Conv2D(filters=64, kernel_size=3, strides=1,
                   padding='same', name=f"spatial_feature_extr"))(input)
        x = LeakyReLU()(x)
        x = self.sas_block(x)
        x = TimeDistributed(
            Conv2DTranspose(filters=64, kernel_size=3, strides=2,  padding='same'))(x)
        x = TimeDistributed(Conv2D(filters=1, kernel_size=3,  padding='same'))(x)

        # Residual path
        y = TimeDistributed(
            Conv2DTranspose(filters=1, kernel_size=4, strides=2,  padding='same'))(input)

        # Add
        out = Add()([x, y])
        out = self.final_reshape(out, name="light_field")

        return keras.Model(inputs, out, name="SAS")

    def sas_block(self, x):
        """
        Input shape (u*v, s, t, F)
        Output shape (u*v, s, t, F')
        """
        for i in range(self.L):
            x = TimeDistributed(
                Conv2D(filters=64, kernel_size=3, strides=1,
                       padding='same', name=f"sas_spat_conv_{i}"))(x)
            x = LeakyReLU()(x)
            x = self.spatial2angular(x)
            x = TimeDistributed(
                Conv2D(filters=64, kernel_size=3, strides=1,
                       padding='same', name=f"sas_ang_conv_{i}"))(x)
            x = LeakyReLU()(x)
            x = self.angular2spatial(x)
        return x

    @staticmethod
    def final_reshape(input, name='light_field'):
        """Spatial to angular reshape a time distributed tensor of shape
        (b, u*v, s, t, ch) to (b, u, v, s, t, ch)
        Only works when u==v.
        """
        (b, uv, s, t, c) = K.int_shape(input)
        uv = int(uv**0.5)
        return Reshape((uv, uv, s, t, c), name=name)(input)

    @staticmethod
    def spatial2angular(input):
        """Spatial to angular reshape a time distributed tensor of shape
        (b, u*v, s, t, ch) to (b, s*t, u, v, ch)
        Only works when u==v.
        """
        (b, uv, s, t, c) = K.int_shape(input)
        x = Permute([2, 3, 1, 4])(input)
        uv = int(uv**0.5)
        return Reshape((s * t, uv, uv, c))(x)

    @staticmethod
    def angular2spatial(input):
        """Angular to spatial reshape a time distributed tensor of shape
        (b, s*t, u, v, ch) to (b, u*v, s, t, ch)
        Only works when s==t.
        """
        (b, st, u, v, c) = K.int_shape(input)
        x = Permute([2, 3, 1, 4])(input)
        st = int(st**0.5)
        return Reshape((u * v, st, st, c))(x)
