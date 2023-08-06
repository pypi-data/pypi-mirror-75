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

import tensorflow.keras.backend as K
from tensorflow.keras.layers import Conv2D, Conv2DTranspose, Conv3D, Conv3DTranspose
from tensorflow.keras.layers import Activation, Reshape, BatchNormalization
from tensorflow.keras.layers import Add


def res_block_3d(x, num_filters, kernel_size=(3, 3, 3), kernel_regularizer=None, name=None):
    # Convolutional path
    x1 = Conv3D(filters=num_filters, kernel_size=kernel_size, padding='same',
                kernel_initializer='he_normal', kernel_regularizer=kernel_regularizer)(x)
    x1 = BatchNormalization()(x1)
    x1 = Activation('relu')(x1)
    x1 = Conv3D(filters=num_filters, kernel_size=kernel_size, padding='same',
                kernel_initializer='he_normal', kernel_regularizer=kernel_regularizer)(x1)
    x1 = BatchNormalization()(x1)

    # Residual connection
    x2 = Conv3D(filters=num_filters, kernel_size=(1, 1, 1), padding='same',
                kernel_initializer='he_normal', kernel_regularizer=kernel_regularizer)(x)
    return Add(name=name)([x1, x2])


def res_block_2d(x, num_filters, kernel_size=(3, 3), kernel_regularizer=None, name=None):
    # Convolutional path
    x1 = Conv2D(filters=num_filters, kernel_size=kernel_size, strides=1, padding='same',
                kernel_initializer='he_normal', kernel_regularizer=kernel_regularizer)(x)
    x1 = BatchNormalization()(x1)
    x1 = Activation('relu')(x1)
    x1 = Conv2D(filters=num_filters, kernel_size=kernel_size, strides=1, padding='same',
                kernel_initializer='he_normal', kernel_regularizer=kernel_regularizer)(x1)
    x1 = BatchNormalization()(x1)

    # Residual connection
    x2 = Conv2D(filters=num_filters, kernel_size=(1, 1), strides=1, padding='same',
                kernel_initializer='he_normal', kernel_regularizer=kernel_regularizer)(x)
    return Add(name=name)([x1, x2])


def sample_down_2d(x, num_filters, kernel_size=(3, 3), strides=(2, 2), kernel_regularizer=None):
    x = Conv2D(filters=num_filters, kernel_size=kernel_size, strides=strides, padding='same',
               kernel_initializer='he_normal', kernel_regularizer=kernel_regularizer)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    return x


def sample_down_3d(x, num_filters, kernel_size=(3, 3, 3), strides=(2, 2, 2), kernel_regularizer=None):
    x = Conv3D(filters=num_filters, kernel_size=kernel_size, strides=strides, padding='same',
               kernel_initializer='he_normal', kernel_regularizer=kernel_regularizer)(x)
    x = Activation('relu')(x)
    x = BatchNormalization()(x)
    return x


def sample_up_2d(x, num_filters, kernel_size=(3, 3), strides=(2, 2), kernel_regularizer=None):
    x = Conv2DTranspose(filters=num_filters, kernel_size=kernel_size, strides=strides,
                        padding='same', kernel_initializer='he_normal',
                        kernel_regularizer=kernel_regularizer)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    return x


def sample_up_3d(x, num_filters, kernel_size=(3, 3, 3), strides=(2, 2, 2), kernel_regularizer=None):
    x = Conv3DTranspose(filters=num_filters, kernel_size=kernel_size, strides=strides,
                        padding='same', kernel_initializer='he_normal',
                        kernel_regularizer=kernel_regularizer)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    return x


def reshape_3d_to_2d(x):
    _, w, h, s, t = K.int_shape(x)
    return Reshape((w, h, s * t))(x)
