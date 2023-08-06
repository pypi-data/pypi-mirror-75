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


"""The LFCNN losses module.
"""
from tensorflow.keras.losses import Loss

from .losses import MeanAbsoluteError, MAE
from .losses import MeanSquaredError, MSE
from .losses import Huber
from .losses import PseudoHuber
from .losses import TotalVariation
from .losses import CosineProximity, NormalizedCosineProximity
from .losses import SpectralInformationDivergence, SID
from .losses import StructuralSimilarity, SSIM
from .losses import MultiScaleStructuralSimilarity, MS_SSIM
from .losses import NormalizedStructuralSimilarity, N_SSIM
from .losses import NormalizedMultiScaleStructuralSimilarity, N_MS_SSIM
from .losses import Dummy

from .losses import mean_absolute_error, mae, mae_clipped
from .losses import mean_squared_error, mse, mse_clipped
from .losses import huber_loss
from .losses import pseudo_huber_loss
from .losses import total_variation
from .losses import psnr, psnr_clipped
from .losses import structural_similarity, ssim
from .losses import normalized_structural_similarity, n_ssim
from .losses import multiscale_structural_similarity, ms_ssim
from .losses import normalized_multiscale_structural_similarity, n_ms_ssim
from .losses import cosine_proximity, normalized_cosine_proximity
from .losses import spectral_information_divergence, sid
from .losses import bad_pix_01, bad_pix_03, bad_pix_07
from .losses import dummy

from .combined_losses import CenterLoss, DisparityLoss


def get(loss: str) -> Loss:
    """Given a loss name, returns an lfcnn loss instance.

    Args:
        loss: Name of the loss.

    Returns:
        Loss instance.
    """
    # Available model classes
    classes = {
        "disparityloss": DisparityLoss,
        "centerloss": CenterLoss,
        "meanabsoluteerror": MeanAbsoluteError,
        "meansquarederror": MeanSquaredError,
        "huber": Huber,
        "pseudohuber": PseudoHuber,
        "totalvariation": TotalVariation,
        "cosineproximity": CosineProximity,
        "normalizedcosineproximity": NormalizedCosineProximity,
        "SpectralInformationDivergence": SpectralInformationDivergence,
        "structuralsimilarity": StructuralSimilarity,
        "multiscalestructuralsimilarity": MultiScaleStructuralSimilarity,
        "normalizedstructuralsimilarity": NormalizedStructuralSimilarity,
        "normalizedmultiscalestructuralsimilarity": NormalizedMultiScaleStructuralSimilarity,
        "dummy": Dummy,
        "mae": MAE,
        "mse": MSE,
        "ssim": SSIM,
        "ms_ssim": MS_SSIM,
        "n_ssim": N_SSIM,
        "n_ms_ssim": N_MS_SSIM,
        "sid": SID,
    }
    try:
        return classes[loss.lower()]
    except KeyError:
        raise ValueError(f"Unknown loss '{loss}'.")


def get_func(loss: str) -> callable:
    """Given a loss name, returns a loss function.

    Args:
        loss: Name of the loss.

    Returns:
        Loss function callable.
    """
    # Available loss functions
    classes = {
        "mean_absolute_error": mean_absolute_error,
        "mean_squared_error": mean_squared_error,
        "huber_loss": huber_loss,
        "pseudo_huber_loss": pseudo_huber_loss,
        "total_variation": total_variation,
        "cosine_proximity": cosine_proximity,
        "normalized_cosine_proximity": normalized_cosine_proximity,
        "structural_similarity": structural_similarity,
        "multiscale_structural_similarity": multiscale_structural_similarity,
        "normalized_structural_similarity": normalized_structural_similarity,
        "normalized_multiscale_structural_similarity": normalized_multiscale_structural_similarity,
        "spectral_information_divergence": spectral_information_divergence,
        "mae": mae,
        "mse": mse,
        "ssim": ssim,
        "ms_ssim": ms_ssim,
        "n_ssim": n_ssim,
        "n_ms_ssim": n_ms_ssim,
        "sid": sid,
    }
    try:
        return classes[loss.lower()]
    except KeyError:
        raise ValueError(f"Unknown loss function '{loss}'.")
