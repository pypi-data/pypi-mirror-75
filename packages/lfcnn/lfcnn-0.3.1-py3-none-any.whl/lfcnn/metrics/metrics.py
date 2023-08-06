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

from tensorflow.python.keras.metrics import MeanMetricWrapper

from lfcnn.losses import mean_absolute_error, mean_squared_error
from lfcnn.losses import total_variation, ssim, ms_ssim
from lfcnn.losses import cosine_proximity, spectral_information_divergence
from lfcnn.losses import bad_pix_01, bad_pix_03, bad_pix_07, psnr_clipped


def get_disparity_metrics():
    """Returns metrics used to evaluate disparity maps.

    Returns:
        List of Metric objects containing:
        MeanAbsoluteError, MeanSquaredError, TotalVariation, BadPix01, BadPix03, BadPix07

    """
    return [MeanAbsoluteError(), MeanSquaredError(), TotalVariation(), BadPix01(), BadPix03(), BadPix07()]


def get_central_metrics_fullsize(k1=0.01, k2=0.03, ssim_filter_size=11, ms_ssim_filter_size=11, ms_ssim_power_factors=(0.0448, 0.2856, 0.3001, 0.2363, 0.1333)):
    """Returns metrics used to evaluate multispectral central views.

    The SSIM and MS-SSIM values are set with the values presented in the
    according papers [1, 2]. In particular, the MS-SSIM is calculated on
    5 scales with a filter length of 11. Hence, the input images should
    have a spatial resolution of at least 256 x 256.

    Returns:
        List of Metric instances containing:
        MeanAbsoluteError, MeanSquaredError, PSNR
        StructuralSimilarity, MultiscaleStructuralSimilarity and
        NormalizedCosineProximity

    """
    return [MeanAbsoluteError(),
            MeanSquaredError(),
            PSNR(),
            StructuralSimilarity(k1=k1, k2=k2, filter_size=ssim_filter_size),
            MultiScaleStructuralSimilarity(k1=k1, k2=k2, filter_size=ms_ssim_filter_size, power_factors=ms_ssim_power_factors),
            CosineProximity(),
            SpectralInformationDivergence()]


def get_central_metrics_small():
    """Returns metrics used to evaluate multispectral central views.

    The SSIM and MS-SSIM values are adapted to be used with small sized
    images of spatial resolutions around 32 x 32.
    The SSIM filter size is chosen to be 5.
    The MS-SSIM filter size is chosen to be 3.
    The MS-SSIM is calculated on 3 scales with power factors 0.5, 0.3, 0.2

    Returns:
        List of Metric instances containing:
        MeanAbsoluteError, MeanSquaredError, PSNR
        StructuralSimilarity, MultiscaleStructuralSimilarity and
        NormalizedCosineProximity

    """
    return get_central_metrics_fullsize(k1=0.01, k2=0.03, ssim_filter_size=5, ms_ssim_filter_size=3, ms_ssim_power_factors=(0.5, 0.3, 0.2))


def get_lf_metrics():
    """Returns metrics used to evaluate light fields.

    Returns:
        List of Metric instances containing:
        MeanAbsoluteError, MeanSquaredError, PSNR
    """
    return [MeanAbsoluteError(),
            MeanSquaredError(),
            PSNR()]


class MeanAbsoluteError(MeanMetricWrapper):
    """Computes the mean absolute error of `y_pred` and `y_true`.
    """
    def __init__(self, name='mean_absolute_error', dtype=None):
        super(MeanAbsoluteError, self).__init__(mean_absolute_error, name, dtype=dtype)


class MeanSquaredError(MeanMetricWrapper):
    """Computes the mean squared error of `y_pred` and `y_true`.
    """
    def __init__(self, name='mean_square_error', dtype=None):
        super(MeanSquaredError, self).__init__(mean_squared_error, name, dtype=dtype)


class TotalVariation(MeanMetricWrapper):
    """Computes the total variation of `y_pred`.
    """
    def __init__(self, name='total_variation', dtype=None):
        super(TotalVariation, self).__init__(total_variation, name, dtype=dtype)


class StructuralSimilarity(MeanMetricWrapper):
    """Computes the structural similarity of `y_pred` and `y_true`.
    """
    def __init__(self, name='ssim', dtype=None, **kwargs):
        super(StructuralSimilarity, self).__init__(ssim, name, dtype=dtype, **kwargs)


class MultiScaleStructuralSimilarity(MeanMetricWrapper):
    """Computes the multiscale structural similarity of `y_pred` and `y_true`.
    """
    def __init__(self, name='ms_ssim', dtype=None, **kwargs):
        super(MultiScaleStructuralSimilarity, self).__init__(ms_ssim, name, dtype=dtype, **kwargs)


class CosineProximity(MeanMetricWrapper):
    """Computes the cosine proximity of `y_pred` and `y_true`.
    """
    def __init__(self, name='cosine_proximity', dtype=None):
        super(CosineProximity, self).__init__(cosine_proximity, name, dtype=dtype)


class SpectralInformationDivergence(MeanMetricWrapper):
    """Computes the spectral information divergence of `y_pred` and `y_true`.
    """
    def __init__(self, name='spectral_information_divergence', dtype=None):
        super(SpectralInformationDivergence, self).__init__(spectral_information_divergence, name, dtype=dtype)


class PSNR(MeanMetricWrapper):
    """Computes the PSNR of `y_pred` and `y_true`.
    """
    def __init__(self, name='psnr', dtype=None, max_val=1.0):
        super(PSNR, self).__init__(psnr_clipped, name, dtype=dtype, max_val=max_val)


class BadPix01(MeanMetricWrapper):
    """Calculate the amount of pixels in percent that deviate more than 0.01
    from the true value.
    """
    def __init__(self, name='bad_pix_01', dtype=None):
        super(BadPix01, self).__init__(bad_pix_01, name, dtype=dtype)


class BadPix03(MeanMetricWrapper):
    """Calculate the amount of pixels in percent that deviate more than 0.03
    from the true value.
    """
    def __init__(self, name='bad_pix_03', dtype=None):
        super(BadPix03, self).__init__(bad_pix_03, name, dtype=dtype)


class BadPix07(MeanMetricWrapper):
    """Calculate the amount of pixels in percent that deviate more than 0.07
    from the true value.
    """
    def __init__(self, name='bad_pix_07', dtype=None):
        super(BadPix07, self).__init__(bad_pix_07, name, dtype=dtype)
