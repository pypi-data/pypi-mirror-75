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


"""The LFCNN metrics module.
"""
from tensorflow.keras.metrics import Metric

from .metrics import get_lf_metrics
from .metrics import get_disparity_metrics
from .metrics import get_central_metrics_small, get_central_metrics_fullsize

from .metrics import MeanAbsoluteError, MeanSquaredError
from .metrics import StructuralSimilarity, MultiScaleStructuralSimilarity
from .metrics import TotalVariation
from .metrics import PSNR
from .metrics import CosineProximity, SpectralInformationDivergence
from .metrics import BadPix01, BadPix03, BadPix07


def get(metric: str) -> Metric:
    """Given a metric name, returns an keras Metric instance.

    Args:
        metric: Name of the metric.

    Returns:
        Metric instance.
    """
    # Available metric classes
    classes = {
        "meanabsoluteerror": MeanAbsoluteError,
        "meansquarederror": MeanSquaredError,
        "psnr": PSNR,
        "totalvariation": TotalVariation,
        "cosineproximity": CosineProximity,
        "SpectralInformationDivergence": SpectralInformationDivergence,
        "structuralsimilarity": StructuralSimilarity,
        "multiscalestructuralsimilarity": MultiScaleStructuralSimilarity,
        "badpix01": BadPix01,
        "badpix03": BadPix03,
        "badpix07": BadPix07,
        "mar": MeanAbsoluteError,
        "mse": MeanSquaredError,
        "ssim": StructuralSimilarity,
        "ms_ssim": MultiScaleStructuralSimilarity,
        "sid": SpectralInformationDivergence,
    }
    try:
        return classes[metric.lower()]
    except KeyError:
        raise ValueError(f"Unknown metric '{metric}'.")
