

"""LfAttNet attention-based disparity estimator model.

Original implementation released under the MIT License.
See: https://github.com/LIAGM/LFattNet

Tsai, Yu-Ju, et al.
"Attention-based View Selection Networks for Light-field Disparity Estimation."
In: Proceedings of the 34th Conference on Artificial Intelligence (AAAI)
2020
"""
from typing import List

import numpy as np

import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.backend as K
from tensorflow.keras.layers import Activation, BatchNormalization
from tensorflow.keras.layers import Conv2D, Conv3D, AveragePooling2D, Lambda
from tensorflow.keras.layers import GlobalAveragePooling3D
from tensorflow.keras.layers import concatenate, add, multiply

from lfcnn.models import BaseModel
from lfcnn.generators import DisparityGenerator
from lfcnn.generators.reshapes import lf_subaperture_stream


class LfAttNet(BaseModel):

    def __init__(self, **kwargs):
        super(LfAttNet, self).__init__(**kwargs)
        raise NotImplementedError("This model is not yet fully implemented.")

    def set_generator_and_reshape(self):
        self._generator = DisparityGenerator
        self._reshape_func = lf_subaperture_stream
        return

    def create_model(self, inputs: List[keras.Input], augmented_shape=None) -> keras.Model:
        """Multi input network, using u*v subaperture inputs.

        """
        # Get middle features from single input stream, concat results
        mid_features = [self.single_input_block(input, name=f"sai_{i+1}") for i, input in enumerate(inputs)]

        # Cost volume model
        cv = Lambda(_getCostVolume_)(mid_features)

        # Channel attention
        cv, attention = channel_attention(cv)

        # Cost volume regression
        cost = basic(cv)
        cost = Lambda(lambda x: K.permute_dimensions(K.squeeze(x, -1), (0, 2, 3, 1)))(cost)
        disp = Activation('softmax')(cost)

        disp = Lambda(disparityregression, name='disparity')(disp)

        self._model_crop = None

        return keras.Model(inputs, [disp, attention], name="LfAttNet")

    @staticmethod
    def single_input_block(input, name):
        """Processing a single subaperture of the light field."""
        x = conv2d_block(input, 4, 3, 1, 1, name=name)
        x = Activation('relu')(x)
        x = conv2d_block(x, 4, 3, 1, 1)
        x = Activation('relu')(x)

        layer1 = _make_layer(x, 4, 2, 1, 1)
        layer2 = _make_layer(layer1, 8, 8, 1, 1)
        layer3 = _make_layer(layer2, 16, 2, 1, 1)
        layer4 = _make_layer(layer3, 16, 2, 1, 2)

        layer4_size = (layer4.get_shape().as_list()[1], layer4.get_shape().as_list()[2])

        # SPP Module
        branch1 = AveragePooling2D((2, 2), (2, 2), 'same')(layer4)
        branch1 = conv2d_block(branch1, 4, 1, 1, 1)
        branch1 = Activation('relu')(branch1)
        branch1 = upsample_2d(layer4_size)(branch1)

        branch2 = AveragePooling2D((4, 4), (4, 4), 'same')(layer4)
        branch2 = conv2d_block(branch2, 4, 1, 1, 1)
        branch2 = Activation('relu')(branch2)
        branch2 = upsample_2d(layer4_size)(branch2)

        branch3 = AveragePooling2D((8, 8), (8, 8), 'same')(layer4)
        branch3 = conv2d_block(branch3, 4, 1, 1, 1)
        branch3 = Activation('relu')(branch3)
        branch3 = upsample_2d(layer4_size)(branch3)

        branch4 = AveragePooling2D((16, 16), (16, 16), 'same')(layer4)
        branch4 = conv2d_block(branch4, 4, 1, 1, 1)
        branch4 = Activation('relu')(branch4)
        branch4 = upsample_2d(layer4_size)(branch4)

        output_feature = concatenate([layer2, layer4, branch4, branch3, branch2, branch1])
        lastconv = conv2d_block(output_feature, 16, 3, 1, 1)
        lastconv = Activation('relu')(lastconv)
        lastconv = Conv2D(filters=4, kernel_size=1, strides=(1, 1), padding='same', use_bias=False)(lastconv)

        return lastconv


def conv2d_block(input, num_filters, kernel_size, stride, dilation, name=None):
    seq = Conv2D(filters=num_filters, kernel_size=kernel_size, strides=stride, padding='same', dilation_rate=dilation,
                 use_bias=False, name=name)(input)
    seq = BatchNormalization()(seq)
    return seq


def conv3d_block(input, num_filters, kernel_size, stride):
    seq = Conv3D(filters=num_filters, kernel_size=kernel_size, strides=stride, padding='same', use_bias=False)(input)
    seq = BatchNormalization()(seq)
    return seq


def res_block(input, num_filters, stride, downsample, dilation):
    x = conv2d_block(input, num_filters, 3, stride, dilation)
    x = Activation('relu')(x)
    x = conv2d_block(x, num_filters, 3, 1, dilation)

    if downsample is not None:
        input = downsample

    return add([x, input])


def _make_layer(input, planes, blocks, stride, dilation):
    inplanes = 4
    downsample = None
    if stride != 1 or inplanes != planes:
        downsample = Conv2D(filters=planes, kernel_size=1, strides=stride, padding='same', use_bias=False)(input)
        downsample = BatchNormalization()(downsample)

    layers = res_block(input, planes, stride, downsample, dilation)
    for i in range(1, blocks):
        layers = res_block(layers, planes, 1, None, dilation)

    return layers


def upsample_2d(size):
    return Lambda(lambda x: tf.image.resize_bilinear(x, size, align_corners=True))


def upsample_3d__helper(x, size):
    shape = K.shape(x)
    x = K.reshape(x, (shape[0] * shape[1], shape[2], shape[3], shape[4]))
    x = tf.image.resize_bilinear(x, size, align_corners=True)
    x = K.reshape(x, (shape[0], shape[1], size[0], size[1], shape[4]))
    return x


def upsample_3d(size):
    return Lambda(lambda x: upsample_3d__helper(x, size))


def _getCostVolume_(inputs):
    shape = K.shape(inputs[0])
    disparity_costs = []
    for d in range(-4, 5):
        if d == 0:
            tmp_list = []
            for i in range(len(inputs)):
                tmp_list.append(inputs[i])
        else:
            tmp_list = []
            for i in range(len(inputs)):
                (v, u) = divmod(i, 9)
                tensor = tf.contrib.image.translate(inputs[i], [d * (u - 4), d * (v - 4)], 'BILINEAR')
                tmp_list.append(tensor)

        cost = K.concatenate(tmp_list, axis=3)
        disparity_costs.append(cost)
    cost_volume = K.stack(disparity_costs, axis=1)
    cost_volume = K.reshape(cost_volume, (shape[0], 9, shape[1], shape[2], 4 * 81))
    return cost_volume


def channel_attention(cost_volume):
    x = GlobalAveragePooling3D()(cost_volume)
    x = Lambda(lambda y: K.expand_dims(K.expand_dims(K.expand_dims(y, 1), 1), 1))(x)
    x = Conv3D(filters=170, kernel_size=1, strides=1, padding='same')(x)
    x = Activation('relu')(x)
    x = Conv3D(filters=15, kernel_size=1, strides=1, padding='same')(x)  # [B, 1, 1, 1, 15]
    x = Activation('sigmoid')(x)

    # 15 -> 25
    # 0  1  2  3  4
    #    5  6  7  8
    #       9 10 11
    #         12 13
    #            14
    #
    # 0  1  2  3  4
    # 1  5  6  7  8
    # 2  6  9 10 11
    # 3  7 10 12 13
    # 4  8 11 13 14

    x = Lambda(lambda y: K.concatenate([y[:, :, :, :, 0:5], y[:, :, :, :, 1:2], y[:, :, :, :, 5:9], y[:, :, :, :, 2:3],
                                        y[:, :, :, :, 6:7], y[:, :, :, :, 9:12], y[:, :, :, :, 3:4], y[:, :, :, :, 7:8],
                                        y[:, :, :, :, 10:11], y[:, :, :, :, 12:14], y[:, :, :, :, 4:5],
                                        y[:, :, :, :, 8:9],
                                        y[:, :, :, :, 11:12], y[:, :, :, :, 13:15]], axis=-1))(x)

    x = Lambda(lambda y: K.reshape(y, (K.shape(y)[0], 5, 5)))(x)
    x = Lambda(lambda y: tf.pad(y, [[0, 0], [0, 4], [0, 4]], 'REFLECT'))(x)
    attention = Lambda(lambda y: K.reshape(y, (K.shape(y)[0], 1, 1, 1, 81)))(x)
    x = Lambda(lambda y: K.repeat_elements(y, 4, -1))(attention)
    return multiply([x, cost_volume]), attention


def channel_attention_free(cost_volume):
    x = GlobalAveragePooling3D()(cost_volume)
    x = Lambda(lambda y: K.expand_dims(K.expand_dims(K.expand_dims(y, 1), 1), 1))(x)
    x = Conv3D(filters=170, kernel_size=1, strides=1, padding='same')(x)
    x = Activation('relu')(x)
    x = Conv3D(filters=81, kernel_size=1, strides=1, padding='same')(x)
    x = Activation('sigmoid')(x)
    attention = Lambda(lambda y: K.reshape(y, (K.shape(y)[0], 1, 1, 1, 81)))(x)
    x = Lambda(lambda y: K.repeat_elements(y, 4, -1))(attention)
    return multiply([x, cost_volume]), attention


def channel_attention_mirror(cost_volume):
    x = GlobalAveragePooling3D()(cost_volume)
    x = Lambda(lambda y: K.expand_dims(K.expand_dims(K.expand_dims(y, 1), 1), 1))(x)
    x = Conv3D(filters=170, kernel_size=1, strides=1, padding='same')(x)
    x = Activation('relu')(x)
    x = Conv3D(filters=25, kernel_size=1, strides=1, padding='same')(x)
    x = Activation('sigmoid')(x)
    x = Lambda(lambda y: K.reshape(y, (K.shape(y)[0], 5, 5)))(x)
    x = Lambda(lambda y: tf.pad(y, [[0, 0], [0, 4], [0, 4]], 'REFLECT'))(x)
    attention = Lambda(lambda y: K.reshape(y, (K.shape(y)[0], 1, 1, 1, 81)))(x)
    x = Lambda(lambda y: K.repeat_elements(y, 4, -1))(attention)
    return multiply([x, cost_volume]), attention


def basic(cost_volume):
    feature = 2 * 75
    dres0 = conv3d_block(cost_volume, feature, 3, 1)
    dres0 = Activation('relu')(dres0)
    dres0 = conv3d_block(dres0, feature, 3, 1)
    cost0 = Activation('relu')(dres0)

    dres1 = conv3d_block(cost0, feature, 3, 1)
    dres1 = Activation('relu')(dres1)
    dres1 = conv3d_block(dres1, feature, 3, 1)
    cost0 = add([dres1, cost0])

    dres4 = conv3d_block(cost0, feature, 3, 1)
    dres4 = Activation('relu')(dres4)
    dres4 = conv3d_block(dres4, feature, 3, 1)
    cost0 = add([dres4, cost0])

    classify = conv3d_block(cost0, feature, 3, 1)
    classify = Activation('relu')(classify)
    cost = Conv3D(filters=1, kernel_size=3, strides=1, padding='same', use_bias=False)(classify)

    return cost


def disparityregression(input):
    shape = K.shape(input)
    disparity_values = np.linspace(-4, 4, 9)
    x = K.constant(disparity_values, shape=[9])
    x = K.expand_dims(K.expand_dims(K.expand_dims(x, 0), 0), 0)
    x = tf.tile(x, [shape[0], shape[1], shape[2], 1])
    out = K.sum(multiply([input, x]), -1)
    return out
