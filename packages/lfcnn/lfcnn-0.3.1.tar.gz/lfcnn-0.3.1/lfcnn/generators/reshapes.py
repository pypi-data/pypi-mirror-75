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

from typing import List, Tuple

import numpy as np


def lf_identity(lf_batch: any,
                labels: List[any]) -> Tuple[any, List[any]]:
    """Returns the input batch and labels.

    Returns:
        lf_batch, labels

    """
    return lf_batch, labels


def lf_subaperture_stream(lf_batch: any,
                          labels: List[any]) -> Tuple[any, List[any]]:
    """The light field subapertures are used for a multi-input stream.
    I.e., the generated input is a list of the light field's subapertures
    corresponding to a transformation/reshape from

    (batchsize, u, v, s, t, lambda)
    to
    [(batchsize, s, t, lambda), ..., (batchsize, s, t, lambda)]
    with u*v elements.


    Returns:
        Tuple of lf_batch_reshaped, labels
    """
    b, u, v, s, t, num_ch = lf_batch.shape
    # Create list of subaperture views by iterating over u*v
    sais =[i for i in lf_batch.reshape(b, u*v, s, t, num_ch).swapaxes(0, 1)]

    return {f"input_{i+1}": sai for i, sai in enumerate(sais)}, labels


def lf_subaperture_stack(lf_batch: any,
                         labels: List[any]) -> Tuple[any, List[any]]:
    """The light field subapertures are stacked together with color/spectrum channels.
    The light fields are reshaped from

    (batchsize, u, v, s, t, lambda)
    to
    (batchsize, s, t, u*v*lambda).

    Returns:
        Tuple of lf_batch_reshaped, labels
    """
    b, u, v, s, t, num_ch = lf_batch.shape
    lf_output = lf_batch.transpose((0, 3, 4, 1, 2, 5)).reshape(
        (b, s, t, u * v * num_ch))

    return lf_output, labels


def lf_subaperture_channel_stack(lf_batch: any,
                                 labels: List[any]) -> Tuple[any, List[any]]:
    """The light field subapertures are stacked retaining color/spectrum channels.
    This can be used for pseudo 3D convolutional networks.
    The light fields are reshaped from

    (batchsize, u, v, s, t, lambda)
    to
    (batchsize, s, t, u*v, lambda).

    Returns:
        Tuple of lf_batch_reshaped, labels
    """
    b, u, v, s, t, num_ch = lf_batch.shape
    lf_output = lf_batch.transpose((0, 3, 4, 1, 2, 5)).reshape(
        (b, s, t, u * v, num_ch))

    return lf_output, labels


def lf_distributed(lf_batch: any,
                   labels: List[any]) -> Tuple[any, List[any]]:
    """The labels are the original light field in its original shape.
    The light field subapertures are contained in the first non-batch axis.
    This can be used for pseudo 4D convolutional networks.

    (batchsize, u, v, s, t, lambda)
    to
    (batchsize, u*v, s, t, lambda).

    Returns:
        Tuple of lf_batch_reshaped, labels
    """
    b, u, v, s, t, num_ch = lf_batch.shape
    lf_output = lf_batch.reshape((b, u * v, s, t, num_ch))

    return lf_output, labels


def lf_crosshair(lf_batch: any,
                 labels: List[any]) -> Tuple[dict, List[any]]:
    """Generates a crosshair view of the light field.
    Strictly speaking, this is not a pure reshape, but generates a list of
    output views.

    (batchsize, u, v, s, t, lambda)
    to
    [(batchsize, v, s, t, lambda),                        # horizontal
    (batchsize, u, s, t, lambda),                         # vertical
    (batchsize, sqrt(u**2 + v**2), s, t, lambda),         # lr-ud diagonal
    (batchsize, sqrt(u**2 + v**2), s, t, lambda),]        # lr-du diagonal


    Returns:
        Tuple of dict(lf_batch_reshaped), labels
    """
    b, u, v, s, t, num_ch = lf_batch.shape

    u_cent, v_cent = u // 2, v // 2

    lf_output = dict(input_1=lf_batch[:, u_cent, :, :, :, :],
                     input_2=lf_batch[:, :, v_cent, :, :, :],
                     input_3=np.diagonal(lf_batch, axis1=1, axis2=2).transpose((0, 4, 1, 2, 3)),
                     input_4=np.diagonal(np.flip(lf_batch, axis=1), axis1=1, axis2=2).transpose((0, 4, 1, 2, 3)))

    return lf_output, labels


def lf_crosshair_stacked(lf_batch: any,
                         labels: List[any]) -> Tuple[dict, List[any]]:
    """Generates a stacked crosshair view of the light field as for example used
    by the Epinet disparity estimator. Strictly speaking, this is not a pure
    reshape, but generates a list of output views.

    (batchsize, u, v, s, t, lambda)
    to
    [(batchsize, s, t, u*lambda),                        # horizontal
    (batchsize, s, t, v*lambda),                         # vertical
    (batchsize, s, t, sqrt(u**2 + v**2)*lambda),         # lr-ud diagonal
    (batchsize, s, t, sqrt(u**2 + v**2)*lambda)]        # lr-du diagonal


    Returns:
        Tuple of dict(lf_batch_reshaped), labels
    """
    b, u, v, s, t, num_ch = lf_batch.shape
    d = min(u, v)

    u_cent, v_cent = u // 2, v // 2

    horz = lf_batch[:, u_cent, :, :, :, :].transpose((0, 2, 3, 1, 4)).reshape(b, s, t, u*num_ch)
    vert = lf_batch[:, :, v_cent, :, :, :].transpose(0, 2, 3, 1, 4).reshape(b, s, t, v * num_ch)
    diag1 = np.diagonal(lf_batch, axis1=1, axis2=2).transpose((0, 4, 1, 2, 3)).transpose((0, 2, 3, 1, 4)).reshape(b, s, t, d * num_ch)
    diag2 = np.diagonal(np.flip(lf_batch, axis=1), axis1=1, axis2=2).transpose((0, 4, 1, 2, 3)).transpose((0, 2, 3, 1, 4)).reshape(b, s, t, d * num_ch)

    return dict(input_1=horz, input_2=vert, input_3=diag1, input_4=diag2), labels
