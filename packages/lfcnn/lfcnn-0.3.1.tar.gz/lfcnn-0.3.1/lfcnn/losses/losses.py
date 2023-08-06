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

import tensorflow as tf
import tensorflow.keras.backend as K

from tensorflow.python.keras.utils import losses_utils
from tensorflow.python.keras.losses import LossFunctionWrapper
from tensorflow.python.keras.losses import huber_loss as huber_loss_keras
from tensorflow.python.keras.losses import mean_squared_error as mean_squared_error_keras
from tensorflow.python.keras.losses import mean_absolute_error as mean_absolute_error_keras

from tensorflow.python.ops.image_ops_impl import ssim as tf_ssim
from tensorflow.python.ops.image_ops_impl import ssim_multiscale as tf_ssim_multiscale
from tensorflow.python.ops.image_ops_impl import total_variation as tf_total_variation

from tensorflow.python.framework import ops as tf_ops
from tensorflow.python.ops import math_ops as tf_math_ops


class MeanAbsoluteError(LossFunctionWrapper):
    """Computes the mean absolute error (MAE) between `y_true` and `y_pred`.

    """
    def __init__(self,
                 reduction=losses_utils.ReductionV2.SUM_OVER_BATCH_SIZE,
                 name='mean_absolute_error'):
        super(MeanAbsoluteError, self).__init__(
            mean_absolute_error, name=name, reduction=reduction)


class MeanSquaredError(LossFunctionWrapper):
    """Computes the mean squared error (MSE) between `y_true` and `y_pred`.

    """
    def __init__(self,
                 reduction=losses_utils.ReductionV2.SUM_OVER_BATCH_SIZE,
                 name='mean_square_error'):
        super(MeanSquaredError, self).__init__(
            mean_squared_error, name=name, reduction=reduction)


class Huber(LossFunctionWrapper):
    """Computes the Huber loss between `y_true` and `y_pred`.

    Given `x = y_true - y_pred`:
    ```
    loss = x^2                  if |x| <= d
    loss = d^2 + d * (|x| - d)  if |x| > d
    ```
    where d is `delta`. See: https://en.wikipedia.org/wiki/Huber_loss
    Note that our definition deviates from the definition on Wikipedia and
    the one used in Keras by a factor of 2. This way, the Huber loss has
    the same scaling as the MSE.
    To acchieve Keras compatible behaviour, specify ver='keras'.

    Arguments:
        delta: A float, the point where the Huber loss function changes from a
            quadratic to linear.
        ver: Optional version argument. If ver='keras', use definition as used in Keras.
             Else, Huber loss is scaled with a factor of two.
        reduction: (Optional) Type of reduction to apply to loss.
        name: Optional name for the object.
    """
    def __init__(self,
                 delta=1.0,
                 ver='lfcnn',
                 reduction=losses_utils.ReductionV2.SUM_OVER_BATCH_SIZE,
                 name='huber_loss'):
        super(Huber, self).__init__(
            huber_loss, name=name, reduction=reduction, delta=delta, ver=ver)


class PseudoHuber(LossFunctionWrapper):
    """Computes the pseudo Huber loss between `y_true` and `y_pred`.
    Given `x = y_true - y_pred`:
    ```
    loss = 2 * d * (sqrt(1 + (x/d)²) - 1)
    ```
    where d is `delta`. See: https://en.wikipedia.org/wiki/Huber_loss
    Note that our definition deviates from the definition on Wikipedia and
    the one used in Keras by a factor of 2. This way, the Huber loss has
    the same scaling as the MSE.

    Arguments:
        delta: A float, the point where the Huber loss function changes from a
            quadratic to linear.
        ver: Optional version argument. If ver='keras', use definition as used in Keras.
             Else, Huber loss is scaled with a factor of two.
        reduction: (Optional) Type of reduction to apply to loss.
        name: Optional name for the object.
    """
    def __init__(self,
                 delta=1.0,
                 ver='lfcnn',
                 reduction=losses_utils.ReductionV2.SUM_OVER_BATCH_SIZE,
                 name='pseudo_huber_loss'):
        super(PseudoHuber, self).__init__(
            pseudo_huber_loss, name=name, reduction=reduction, delta=delta, ver=ver)


class TotalVariation(LossFunctionWrapper):
    """Computes the total variation of a predicted tensor.

    """

    def __init__(self,
                 reduction=losses_utils.ReductionV2.SUM_OVER_BATCH_SIZE,
                 name='total_variation'):
        super(TotalVariation, self).__init__(
            total_variation, name=name, reduction=reduction)


class CosineProximity(LossFunctionWrapper):
    """Computes the cosine proximity (CP) of two tensors
    along the last axis.

    If the last axis is a spectral axis, this measures the spectral similarity
    of two multispectral or hyperspectral tensors (resp. light fields).

    Maximum similarity corresponds to a value of CP = 1.

    ```
    CP = cos(alpha) = <y_pred, y_true> / (||y_pred|| * ||y_true||)
    ```
    """

    def __init__(self,
                 reduction=losses_utils.ReductionV2.SUM_OVER_BATCH_SIZE,
                 name='cosine_proximity'):
        super(CosineProximity, self).__init__(
            cosine_proximity, name=name, reduction=reduction)


class NormalizedCosineProximity(LossFunctionWrapper):
    """Computes the normalized cosine proximity (N-CP) of two tensors
    along the last axis. The N-CP can directly be used for loss minimization.

    If the last axis is a spectral axis, this measures the spectral similarity
    of two multispectral or hyperspectral tensors (resp. light fields).

    Maximum similarity corresponds to a value of N-CP = 0.

    ```
    N-CP = 0.5*(1.0 - cos(alpha))
    ```

    where

    ```
    cos(alpha) = <y_pred, y_true> / (||y_pred|| * ||y_true||)
    ```

    """

    def __init__(self,
                 reduction=losses_utils.ReductionV2.SUM_OVER_BATCH_SIZE,
                 name='normalized_cosine_proximity'):
        super(NormalizedCosineProximity, self).__init__(
            normalized_cosine_proximity, name=name, reduction=reduction)


class SpectralInformationDivergence(LossFunctionWrapper):
    """Computes the spectral information divergence (SID)
    between predicted and true tensor. SID is basically a symmetrized
    Kullback-Leibler divergence if the pixel spectra are interpreted as a
    probability distribution.

    Original Paper:
    Chein-I Chang, "An information-theoretic approach to spectral variability,
    similarity, and discrimination for hyperspectral image analysis,"
    in IEEE Transactions on Information Theory,
    vol. 46, no. 5, pp. 1927-1932, Aug. 2000.

    """

    def __init__(self,
                 reduction=losses_utils.ReductionV2.SUM_OVER_BATCH_SIZE,
                 name='sid'):
        super(SpectralInformationDivergence, self).__init__(
            spectral_information_divergence, name=name, reduction=reduction)


class StructuralSimilarity(LossFunctionWrapper):
    """Computes the structural similarity index metric (SSIM)
    between predicted and true tensor.

    """

    def __init__(self,
                 reduction=losses_utils.ReductionV2.SUM_OVER_BATCH_SIZE,
                 name='ssim'):
        super(StructuralSimilarity, self).__init__(
            structural_similarity, name=name, reduction=reduction)


class NormalizedStructuralSimilarity(LossFunctionWrapper):
    """Computes the normalized structural similarity index metric (SSIM)
    between predicted and true tensor with

    ```
    N-SSIM = 0.5 * ( 1.0 - SSIM(y_true, y_pred) )
    ```

    That is, the N-MS-SSIM is ranged in [0, 1] where
    0 corresponds to a maximal similarity.
    """

    def __init__(self,
                 reduction=losses_utils.ReductionV2.SUM_OVER_BATCH_SIZE,
                 name='n_ssim'):
        super(NormalizedStructuralSimilarity, self).__init__(
            normalized_structural_similarity, name=name, reduction=reduction)


class MultiScaleStructuralSimilarity(LossFunctionWrapper):
    """Computes the multiscale structural similarity index metric (SSIM)
    between predicted and true tensor.
    """

    def __init__(self,
                 reduction=losses_utils.ReductionV2.SUM_OVER_BATCH_SIZE,
                 name='ms_ssim'):
        super(MultiScaleStructuralSimilarity, self).__init__(
            multiscale_structural_similarity, name=name, reduction=reduction)


class NormalizedMultiScaleStructuralSimilarity(LossFunctionWrapper):
    """Computes the normalized multiscale structural similarity index metric
    (SSIM) between predicted and true tensor. Here,

    ```
    N-MS-SSIM = 0.5 * ( 1.0 - MS-SSIM(y_true, y_pred) )
    ```

    That is, the N-MS-SSIM is ranged in [0, 1] where
    0 corresponds to a maximal similarity.
    """

    def __init__(self,
                 reduction=losses_utils.ReductionV2.SUM_OVER_BATCH_SIZE,
                 name='n_ms_ssim'):
        super(NormalizedMultiScaleStructuralSimilarity, self).__init__(
            normalized_structural_similarity, name=name, reduction=reduction)


class Dummy(LossFunctionWrapper):
    """Dummy loss that does not compute anything.
    Can be used when benchmarking training time performance.
    """

    def __init__(self,
                 reduction=losses_utils.ReductionV2.SUM_OVER_BATCH_SIZE,
                 name='dummy'):
        super(Dummy, self).__init__(dummy, name=name, reduction=reduction)


# Define actual loss functions
# We calculate the mean everywhere so we can easily add losses together
def mean_squared_error(y_true, y_pred):
    """Calculate the mean square error between true and predicted tensor.
    """
    return K.mean(mean_squared_error_keras(y_true, y_pred))


def mean_absolute_error(y_true, y_pred):
    """Calculate the mean absolute error between true and predicted tensor.
    """
    return K.mean(mean_absolute_error_keras(y_true, y_pred))


def huber_loss(y_true, y_pred, delta=1.0, ver='lfcnn'):
    """Calculate the Huber loss between true and predicted tensor.
    """

    if ver == 'keras':
        mult = tf_ops.convert_to_tensor_v2(1, dtype=K.floatx())
    else:
        mult = tf_ops.convert_to_tensor_v2(2, dtype=K.floatx())

    delta = tf_ops.convert_to_tensor_v2(delta, dtype=K.floatx())

    return K.mean(mult * huber_loss_keras(y_true, y_pred, delta))


def pseudo_huber_loss(y_true, y_pred, delta=1.0, ver='lfcnn'):
    """Calculated the pseudo Huber loss between y_true and y_pred.
    The pseudo Huber loss function is a smooth approximation of the Huber loss,
    i.e. all derivatives exist and are continuous.

    Arguments:
        delta: The point where the pseudo Huber loss function changes from
               quadratic to linear behaviour.

    See Also:
        https://en.wikipedia.org/wiki/Huber_loss

    """

    if ver == 'keras':
        mult = tf_ops.convert_to_tensor_v2(1, dtype=K.floatx())
    else:
        mult = tf_ops.convert_to_tensor_v2(2, dtype=K.floatx())

    y_pred = tf_math_ops.cast(y_pred, dtype=K.floatx())
    y_true = tf_math_ops.cast(y_true, dtype=K.floatx())
    delta = tf_ops.convert_to_tensor_v2(delta, dtype=K.floatx())
    delta_inv_sq = 1.0 / (delta*delta)
    return K.mean(mult * delta * (K.sqrt(1 + delta_inv_sq * K.square(y_pred - y_true)) - 1))


def structural_similarity(y_true, y_pred, max_val=1.0, k1=0.01, k2=0.03, **kwargs):
    """Calculate the structural Similarity (SSIM) between true and predicted
    tensor.
    """
    return K.mean(tf_ssim(y_true, y_pred, max_val=max_val, k1=k1, k2=k2, **kwargs))


def multiscale_structural_similarity(y_true, y_pred, max_val=1.0, k1=0.01, k2=0.03, **kwargs):
    """Calculate the multiscale structural similarity (MS-SSIM) between true
    and predicted tensor.
    """
    return K.mean(tf_ssim_multiscale(y_true, y_pred, max_val=max_val, k1=k1, k2=k2, **kwargs))


def normalized_structural_similarity(y_true, y_pred, **kwargs):
    """Calculates a normalized structural similiarity (N-SSIM)

    ```
    0.5*(1 - SSIM(y_true, y_pred)).
    ```

    That is, the N-SSIM is ranged in [0, 1] where
    0 corresponds to a maximal similarity.
    """
    return 0.5*(1.0 - structural_similarity(y_true, y_pred, **kwargs))


def normalized_multiscale_structural_similarity(y_true, y_pred, **kwargs):
    """Calculates a normalized multiscale structural similiarity (N-MS-SSIM)

    ```
    0.5*(1 - MS-SSIM(y_true, y_pred)).
    ```

    That is, the N-MS-SSIM is ranged in [0, 1] where
    0 corresponds to a maximal similarity.

    """
    return 0.5*(1.0 - multiscale_structural_similarity(y_true, y_pred, **kwargs))


def total_variation(y_true, y_pred):
    """Calculate the total variation of a tensor.
    """
    return K.mean(tf_total_variation(y_pred))


def cosine_proximity(y_true, y_pred, axis=-1):
    """Calculate the cosine proximity between true and predicted tensor.
    """
    y_pred = tf_math_ops.cast(y_pred, dtype=K.floatx())
    y_true = tf_math_ops.cast(y_true, dtype=K.floatx())

    y_true_normed = K.l2_normalize(y_true, axis=axis)
    y_pred_normed = K.l2_normalize(y_pred, axis=axis)
    return K.mean(K.sum(y_true_normed * y_pred_normed, axis=axis))


def normalized_cosine_proximity(y_true, y_pred, axis=-1):
    """Calculates a normalized cosine proximity

    ```
    0.5*(1-cos(alpha)),
    ```

    where

    ```
    cos(alpha) = <y_true, y_pred> / (||y_true|| * ||y_pred||),
    ```

    where the scalar product is taken along the specified axis.
    That is, the normalized cosine proximity is ranged in [0, 1] where
    0 corresponds to a maximal similarity.

    """
    return 0.5*(1.0 - cosine_proximity(y_true, y_pred, axis=axis))


def spectral_information_divergence(y_true, y_pred, k=0):
    """Calculate the mean spectral information divergence (SID) which
    is basically a symmetrized Kullback-Leibler divergence if the pixel
    spectra are interpreted as a probability distribution.

    Original Paper:
    Chein-I Chang, "An information-theoretic approach to spectral variability,
    similarity, and discrimination for hyperspectral image analysis,"
    in IEEE Transactions on Information Theory,
    vol. 46, no. 5, pp. 1927-1932, Aug. 2000.

    Args:
        y_true: True tensor.
        y_pred: Predicted tensor.
        k: Factor for numerical stability.

    Returns:
        Spectral Information Divergence of y_true and y_pred.
    """
    y_pred = tf_math_ops.cast(y_pred, dtype=K.floatx())
    y_true = tf_math_ops.cast(y_true, dtype=K.floatx())

    p = K.clip(y_true, K.epsilon(), 1)
    q = K.clip(y_pred, K.epsilon(), 1)

    p = p / (K.sum(p, axis=-1, keepdims=True) + k)
    q = q / (K.sum(q, axis=-1, keepdims=True) + k)

    return K.mean(K.sum(p * K.log(p / q), axis=-1) + K.sum(q * K.log(q / p), axis=-1))


def bad_pix(y_true, y_pred, val):
    """Calculate the amount of pixels in percent that deviate more than val
    from the true value.
    """
    y_pred = tf_math_ops.cast(y_pred, dtype=K.floatx())
    y_true = tf_math_ops.cast(y_true, dtype=K.floatx())

    diff = K.abs(y_true - y_pred) > val
    return 100 * K.sum(tf_math_ops.cast(diff, dtype=K.floatx())) / tf_math_ops.cast(tf.size(diff), dtype=K.floatx())


def bad_pix_01(y_true, y_pred):
    """Calculate the amount of pixels in percent that deviate more than 0.01
    from the true value.
    """
    return bad_pix(y_true, y_pred, 0.01)


def bad_pix_03(y_true, y_pred):
    """Calculate the amount of pixels in percent that deviate more than 0.03
    from the true value.
    """
    return bad_pix(y_true, y_pred, 0.03)


def bad_pix_07(y_true, y_pred):
    """Calculate the amount of pixels in percent that deviate more than 0.07
    from the true value.
    """
    return bad_pix(y_true, y_pred, 0.07)


def psnr(y_true, y_pred, max_val=1.0):
    """Calculates the peak signal-to-noise ratio (PSNR) in dB of
    y_pred with respect to y_true.

    Args:
        y_true: True image.
        y_pred: Predicted image.
        max_val: Dynamic range of image. For float images: 1, for uint8: 255, etc.

    Returns:
        PSNR value in decibel.

    """
    y_pred = tf_math_ops.cast(y_pred, dtype=K.floatx())
    y_true = tf_math_ops.cast(y_true, dtype=K.floatx())

    # Note that K.log calculates the natural logarithm, so we need to divide by ln(10) = 2.30258501
    return (10.0 * K.log((max_val*max_val) / (K.mean(K.square(y_pred - y_true)) + K.epsilon()))) / 2.30258501


def psnr_clipped(y_true, y_pred, max_val=1.0):
    """Calculates peak signal-to-noise ratio (PSNR) of y_pred with respect to y_true, but clips
    y_pred with max_val before psnr calculation.
    """
    y_pred = tf_math_ops.cast(y_pred, dtype=K.floatx())
    y_true = tf_math_ops.cast(y_true, dtype=K.floatx())
    return psnr(y_true, K.clip(y_pred, 0, max_val), max_val)


def mse_clipped(y_true, y_pred, max_val=1.0):
    """Calculates mean square error (MSE) of y_pred with respect to y_true, but clips
    y_pred with max_val before MSE calculation.
    """
    y_pred = tf_math_ops.cast(y_pred, dtype=K.floatx())
    y_true = tf_math_ops.cast(y_true, dtype=K.floatx())
    return mean_squared_error(y_true, K.clip(y_pred, 0, max_val))


def mae_clipped(y_true, y_pred, max_val=1.0):
    """Calculates mean absolute error (MAE) of y_pred with respect to y_true, but clips
    y_pred with max_val before MAE calculation.
    """
    y_pred = tf_math_ops.cast(y_pred, dtype=K.floatx())
    y_true = tf_math_ops.cast(y_true, dtype=K.floatx())
    return mean_absolute_error(y_true, K.clip(y_pred, 0, max_val))


def dummy(y_true, y_pred):
    """Dummy loss not performing any calculation. Always returns 1
    """
    return tf_math_ops.cast(1.0, dtype=K.floatx())


# Define Aliases
MAE = MeanAbsoluteError
MSE = MeanSquaredError
SSIM = StructuralSimilarity
MS_SSIM = MultiScaleStructuralSimilarity
N_SSIM = NormalizedStructuralSimilarity
N_MS_SSIM = NormalizedMultiScaleStructuralSimilarity
SID = SpectralInformationDivergence

mae = mean_absolute_error
mse = mean_squared_error
ssim = structural_similarity
ms_ssim = multiscale_structural_similarity
n_ssim = normalized_structural_similarity
n_ms_ssim = normalized_multiscale_structural_similarity
sid = spectral_information_divergence
