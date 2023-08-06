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

"""Leanringrate schedulers to automatically adjust the learning rate during
training.
"""

import numpy as np

from tensorflow.keras.callbacks import LearningRateScheduler


class StepDecay(LearningRateScheduler):
    def __init__(self,
                 lr_init: float,
                 steps: int,
                 decay: float = 0.5):
        """Learning rate is dropped every steps epochs to
        decay*learning_rate starting with the initial learning rate.
        That is, the learning rate is given by
        ```
        lr = lr_init * decay**N
        ```
        where
        ```
        N = epoch // steps
        ```

        Args:
            lr_init: Initial learning rate.

            steps: Decay learning rate every steps epoch.

            decay: Decay factor.
        """
        super(StepDecay, self).__init__(schedule=self.step_decay)
        self.lr_init = lr_init
        self.steps = steps
        self.decay = decay
        self.name = f"StepDecay, decay {decay}"

    def step_decay(self, epoch: int, lr: float) -> float:
        # Correct epoch index start at 0
        n = epoch // self.steps

        return self.lr_init * self.decay**n


class PolynomialDecay(LearningRateScheduler):
    def __init__(self,
                 lr_init: float,
                 max_epoch: int,
                 power: int = 2,
                 lr_min: float = 1e-6):
        """Learning rate decays polynomially from initial learning rate
        to minimal learning rate at max_poch epochs. For epochs larger then
        max_epoch, the learning rate stays constant at lr_min.

        Args:
            lr_init: Initial learning rate.

            max_epoch: Epoch where decay ends. For epochs larger than max_epoch,
                       the learning rate stays constant at lr_min.

            power. Polynomial power.

            lr_init: Minimum learning rate.
        """
        super(PolynomialDecay   , self).__init__(schedule=self.polynomial_decay)
        if type(power) != int:
            raise ValueError("Polynomial decay only works with integer powers.")

        self.power = float(power)
        self.e_max = max_epoch
        self.a = (lr_init - lr_min)/((-max_epoch)**self.power)
        self.b = lr_min
        self.name = f"PolynomialDecay, power {power}"

    def polynomial_decay(self, epoch: int, lr: float) -> float:
        return self.a * min(epoch - self.e_max, 0)**self.power + self.b


class LinearDecay(PolynomialDecay):
    def __init__(self,
                 lr_init: float,
                 max_epoch: int,
                 lr_min: float = 1e-6):
        """Learning rate decays linearly. Corresponds to PolynomialDecay
        with power=1.

        Args:
            lr_init: Initial learning rate.

            max_epoch: Epoch where decay ends. For epochs larger than max_epoch,
                       the learning rate stays constant at lr_min.

            lr_init: Minimum learning rate.
        """
        super(LinearDecay, self).__init__(
            lr_init=lr_init, lr_min=lr_min, power=1, max_epoch=max_epoch)
        self.name = "LinearDecay"


class ExponentialDecay(LearningRateScheduler):
    def __init__(self,
                 lr_init: float,
                 max_epoch: int,
                 alpha: float = 0.02,
                 lr_min: float = 1e-6):
        """Learning rate decays exponentially from inital learning rate
        to minimal learning rate at max_poch epoch. For epochs larger then
        max_epoch, the learning rate stays constant at lr_min.

        Args:
            lr_init: Initial learning rate.

            max_epoch: Epoch where decay ends. For epochs larger than max_epoch,
                       the learning rate stays constant at lr_min.

            power. Polynomial power.

            lr_init: Minimum learning rate.
        """
        super(ExponentialDecay, self).__init__(schedule=self.polynomial_decay)
        self.e_max = max_epoch
        self.alpha = float(alpha)
        self.a = (lr_min - lr_init) / (np.exp(-self.alpha*max_epoch) - 1)
        self.b = lr_init - self.a
        self.name = f"ExponentialDecay, alpha {alpha}"

    def polynomial_decay(self, epoch: int, lr: float) -> float:
        return self.a * np.exp(-self.alpha*min(epoch, self.e_max)) + self.b


class SigmoidDecay(LearningRateScheduler):
    def __init__(self,
                 lr_init: float,
                 max_epoch: int,
                 alpha=0.1,
                 lr_min: float = 1e-6):
        """Sigmoid decay. The sigmoid function is create symmetrically around
        max_epoch // 2.

        Args:
            lr_init: Initial learning rate.

            max_epoch: Epoch where decay ends. For epochs larger than max_epoch,
                       the learning rate stays constant at lr_min.

            alpha. Decay factor tuning the width of the sigmoid.

            lr_init: Minimum learning rate.
        """
        super(SigmoidDecay, self).__init__(schedule=self.sigmoid_decay)
        self.lr_min = lr_min
        self.lr_init = lr_init
        self.alpha = alpha
        self.center = max_epoch // 2
        self.name = f"SigmoidDecay, alpha {alpha}"

    def sigmoid_decay(self, epoch: int, lr: float) -> float:
        return (self.lr_init - self.lr_min) / (1 + np.exp(self.alpha*(epoch - self.center))) + self.lr_min
