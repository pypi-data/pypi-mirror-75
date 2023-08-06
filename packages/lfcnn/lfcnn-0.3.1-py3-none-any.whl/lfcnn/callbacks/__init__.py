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


"""The LFCNN callbacks module.
"""

from .sacred import SacredMetricLogger, SacredTimeLogger, SacredEpochLogger, SacredLearningRateLogger

from .lr_finder import LearningRateFinder

from .lr_schedules import PolynomialDecay, LinearDecay, ExponentialDecay
from .lr_schedules import SigmoidDecay, StepDecay

from .cyclic_learning import OneCycle, OneCycleCosine
from .cyclic_learning import OneCycleMomentum, OneCycleCosineMomentum


def get(callback: str):
    """Given a callback name, returns an Keras callback instance.

    Args:
        callback: Name of the callback.

    Returns:
        Callback instance.
    """
    # Available callback classes
    classes = {
        "sacredmetriclogger": SacredMetricLogger,
        "sacredtimelogger": SacredTimeLogger,
        "sacredepochlogger": SacredEpochLogger,
        "sacredlearningratelogger": SacredLearningRateLogger,
        "polynomialdecay": PolynomialDecay,
        "lineardecay": LinearDecay,
        "exponentialdecay": ExponentialDecay,
        "sigmoiddecay": SigmoidDecay,
        "stepdecay": StepDecay,
        "onecycle": OneCycle,
        "onecyclemomentum": OneCycleMomentum,
        "onecyclecosine": OneCycleCosine,
        "onecyclecosinemomentum":OneCycleCosineMomentum,
        "learningratefinder": LearningRateFinder,
    }
    try:
        return classes[callback.lower()]
    except KeyError:
        raise ValueError(f"Unknown callback '{callback}'.")
