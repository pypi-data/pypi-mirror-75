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

from typing import Tuple

from tensorflow.python.keras.utils import losses_utils

from .losses import LossFunctionWrapper
from .losses import n_ms_ssim, huber_loss, normalized_cosine_proximity, total_variation


class CenterLoss(LossFunctionWrapper):

    def __init__(self,
                 mu: float = 0,
                 gamma: float = 0,
                 power_factors: Tuple[float, ...] = (0.5, 0.3, 0.2),
                 filter_size: int = 3,
                 k1: float = 0.03,
                 k2: float = 0.09,
                 reduction=losses_utils.ReductionV2.SUM_OVER_BATCH_SIZE,
                 name='center_loss'):
        """Central view loss function based on the Huber loss with delta=1 and
        two regularization terms based on the multi-scale structural similarity
        and the cosine proximity.

        Note that the default values for the free parameters of SSIM/MS-SSIM
        deviate from the original papers. In particular, we choose
        k1=0.03, k2=0.09 to be three times larger than the original to improve
        the numerical stability for small spatial resolutions.
        Furthermore the filtersize of the mean and standard deviation calculation
        is set to 3 instead of 11 since the compared images will have a low
        spatial resultion. The MS-SSIM is calculated at 3 instead of 5 levels,
        since for a size of 32x32 only 3 meaningful downsampling operations
        are possible in combination with a filter width of 3.

        If you have a different output size than 32x32, these values need to
        be adapted!

        Args:
            mu: Regularization factor of term based on the structural similarity.

            gamma: Regularization factor of term based on cosine proximity.

            power_factors: Scale power factors of the MS-SSIM regularizing term.

            filter_size: Filter size of the averaging filter used to calculate
                         the SSIM at each scale.

            k1: Constant for numerical stability of SSIM and MS_SSIM.

            k2: Constant for numerical stability of SSIM and MS_SSIM.

        """
        super(CenterLoss, self).__init__(
            center_loss, name=name, reduction=reduction, mu=mu, gamma=gamma, power_factors=power_factors, filter_size=filter_size, k1=k1, k2=k2)


def center_loss(y_true, y_pred, mu, gamma, power_factors, filter_size, k1, k2):
    return huber_loss(y_true, y_pred) \
           + mu*n_ms_ssim(y_true, y_pred, max_val=1.0, k1=k1, k2=k2, power_factors=power_factors, filter_size=filter_size) \
           + gamma*normalized_cosine_proximity(y_true, y_pred)


class DisparityLoss(LossFunctionWrapper):

    def __init__(self,
                 mu=0,
                 reduction=losses_utils.ReductionV2.SUM_OVER_BATCH_SIZE,
                 name='disparity_loss'):
        """Disparity loss function based on the Huber loss with delta=1 and a
        total variational regularizer.

        Args:
            mu: Regularization factor. Default: No regularization.

        """
        super(DisparityLoss, self).__init__(
            disparity_loss, name=name, reduction=reduction, mu=mu)


def disparity_loss(y_true, y_pred, mu=0):
    return huber_loss(y_true, y_pred) + mu*total_variation(y_true, y_pred)
