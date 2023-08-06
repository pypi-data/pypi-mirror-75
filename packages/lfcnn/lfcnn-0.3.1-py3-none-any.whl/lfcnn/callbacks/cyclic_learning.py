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

"""Callbacks used for cyclic learning.

For details on cyclic learning (cyclic learning rate, cyclic momentum
and learning rate finder) see the original article and references within:

Smith, Leslie N.
"Cyclical learning rates for training neural networks."
2017 IEEE Winter Conference on Applications of Computer Vision (WACV)
2017.

For a broader overview, see:

Smith, Leslie N.
"A disciplined approach to neural network hyper-parameters:
Part 1--learning rate, batch size, momentum, and weight decay."
arXiv preprint arXiv:1803.09820 (2018).
"""

import tensorflow.keras.backend as K
from tensorflow.keras.callbacks import LearningRateScheduler, Callback

from tensorflow.keras import optimizers
from tensorflow.keras.mixed_precision.experimental import LossScaleOptimizer

import numpy as np

# List of optimizers with momentum that can be used with MomentumScheduler
OPTIMIZERS_WITH_MOMENTUM = [optimizers.SGD]


class OneCycle(LearningRateScheduler):
    def __init__(self,
                 lr_min: float,
                 lr_max: float,
                 lr_final: float,
                 cycle_epoch: int,
                 max_epoch: int):
        """The 1cycle learning rate scheduler as proposed by Smith.
        The learning rate starts at the minimal learning rate,
        increases linearly to the maximal learning rate and
        decreases linearly to the minimal learning rate.
        This cycle takes cycle_epoch steps.
        Finally, the learning rate decays linearly to the final learning
        rate at max_epoch.

        See: Smith, Leslie N.
        "A disciplined approach to neural network hyper-parameters:
        Part 1--learning rate, batch size, momentum, and weight decay."
        arXiv preprint arXiv:1803.09820 (2018).

        Args:
            lr_min: Minimum learning rate. This is the initial learning rate.

            lr_max: Maximum learning rate.

            lr_final: Final learning rate.

            cycle_epoch: Number of epochs one cycle takes, starting from
                         the minimal learning rate to toe maximal learning
                         rate, back to the minimal learning rate.

            max_epoch: Epoch where decay ends. For epochs larger than max_epoch,
                       the learning rate stays constant at lr_final.

        """
        super(OneCycle, self).__init__(schedule=self.one_cycle)
        self.lr_max = lr_max
        self.lr_min = lr_min
        self.lr_final = lr_final
        self.cycle_epoch = cycle_epoch
        self.max_epoch = max_epoch
        if not max_epoch > cycle_epoch:
            raise ValueError("max_epoch needs to be larger than cycle_epoch.")

        self.m1 = (lr_max - lr_min) / (float(cycle_epoch // 2))
        self.m2 = (lr_min - lr_final) / (float(max_epoch - 1 - cycle_epoch))

        self.name = f"1cycle"

    def one_cycle(self, epoch: int, lr: float) -> float:
        # First, linear increase to lr_max
        if epoch <= self.cycle_epoch // 2:
            return self.m1 * epoch + self.lr_min

        # Second, linear decrease back to lr_min
        elif epoch <= self.cycle_epoch:
            return -self.m1 * (epoch - self.cycle_epoch) + self.lr_min

        # Final, linear decrease to lr_final
        elif epoch < self.max_epoch:
            return -self.m2 * (epoch - self.cycle_epoch) + self.lr_min

        # For even larger epochs, stay at lr_min
        else:
            return self.lr_final


class OneCycleCosine(LearningRateScheduler):
    def __init__(self,
                 lr_min: float,
                 lr_max: float,
                 lr_final: float,
                 phase_epoch: int,
                 max_epoch: int):
        """This adaption (proposed by fastAI) of the 1cycle policy uses the
        cosine to increase and decrease the learning rate.
        The learning rate update consists of only two phases:
        1. increasing from lr_min to lr_max
        2. decreasing from lr_max to lr_final.

        See: https://sgugger.github.io/the-1cycle-policy.html

        Args:
            lr_min: Minimum learning rate. This is the initial learning rate.

            lr_max: Maximum learning rate.

            lr_final: Final learning rate.

            phase_epoch: Epoch where maximum learning rate is achieved.

            max_epoch: Epoch where decay ends. For epochs larger than max_epoch,
                       the learning rate stays constant at lr_final.

        """
        super(OneCycleCosine, self).__init__(schedule=self.one_cycle_cosine)
        self.lr_max = lr_max
        self.lr_min = lr_min
        self.lr_final = lr_final
        self.phase_epoch = phase_epoch
        self.max_epoch = max_epoch
        if not max_epoch > phase_epoch:
            raise ValueError("max_epoch needs to be larger than phase_epoch.")

        # Period of increasing and decreasing cosines
        t0 = 2 * phase_epoch
        t1 = 2 * (max_epoch - phase_epoch)

        self.f1 = 1.0 / t0
        self.f2 = 1.0 / t1
        self.a1 = 0.5*(lr_max - lr_min)
        self.a2 = 0.5*(lr_max - lr_final)
        self.name = f"1cycle cosine"

    def one_cycle_cosine(self, epoch: int, lr: float) -> float:
        # First, linear increase to lr_max
        if epoch <= self.phase_epoch:
            return self.a1 * (- np.cos(2*np.pi*self.f1*epoch) + 1) + self.lr_min

        # Second, linear decrease back to lr_min
        elif epoch < self.max_epoch:
            return self.a2 * (np.cos(2*np.pi*self.f2*(epoch - self.phase_epoch)) + 1) + self.lr_final

        # For even larger epochs, stay at lr_min
        else:
            return self.lr_final


class MomentumScheduler(Callback):

    def __init__(self, schedule, verbose=0):
        """A callback to schedule optimizer momentum.
        This is based on Keras' LearningRateScheduler implementation.
        The momentum is logged to logs.

        Args:
            schedule: Schedule function.

            verbose: Whether to print verbose output.
        """
        super(MomentumScheduler, self).__init__()
        self.schedule = schedule
        self.verbose = verbose
        self._optimizer = None

    def set_optimizer(self):
        """Set optimizer attribute.

        This is a bit ugly, but is necessary when using mixed precision
        training with loss scaling. Internally, when using loss scaling,
        the optimizer is wrapped in a LossScaleOptimizer which does not
        expose the momentum directly.
        """
        if self._optimizer is None:
            self._optimizer = self.model.optimizer._optimizer \
                if type(self.model.optimizer) == LossScaleOptimizer \
                else self.model.optimizer

        if type(self._optimizer) not in OPTIMIZERS_WITH_MOMENTUM:
            raise ValueError("Optimizer does not support momentum scheduling. "
                             f"Use one of {OPTIMIZERS_WITH_MOMENTUM}.")

    def on_train_begin(self, logs=None):
        self.set_optimizer()

    def on_epoch_begin(self, epoch, logs=None):
        momentum = float(K.get_value(self._optimizer.momentum))
        momentum = self.schedule(epoch, momentum)
        K.set_value(self._optimizer.momentum, momentum)
        if self.verbose:
            print(f'\nEpoch {epoch + 1}: OneCycleMomentum setting momentum '
                  f'to {momentum}.')

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        logs['momentum'] = K.get_value(self._optimizer.momentum)


class OneCycleMomentum(MomentumScheduler):

    def __init__(self, cycle_epoch, m_min=0.85, m_max=0.95, verbose=0):
        """The 1cycle momentum scheduler as proposed by Smith.
        Should be used in combination with OneCycle learning rate scheduler
        when training with SGD or another optimizer that has a momentum
        attribute.

        The momentum starts at the maximum value (when the learning rate is
        small) and decreases to a minimum value (when the learning rate is
        large). Finally, the momentum stays at the maximum value for the rest
        of the training.

        See: Smith, Leslie N.
        "A disciplined approach to neural network hyper-parameters:
        Part 1--learning rate, batch size, momentum, and weight decay."
        arXiv preprint arXiv:1803.09820 (2018).

        Args:
            cycle_epoch: Number of epochs one cycle takes. Should be the same
                         as for the OneCycle learning rate scheduler.

            m_min: Minimum momentum.

            m_max: Maximum momentum.

        """
        super(OneCycleMomentum, self).__init__(self.one_cycle)
        self.m_min = m_min
        self.m_max = m_max
        self.cycle_epoch = cycle_epoch

        self.m = (m_max - m_min) / (float(cycle_epoch // 2))
        self.name = "1cycle momentum"
        return

    def one_cycle(self, epoch: int, momentum: float) -> float:
        if epoch <= self.cycle_epoch // 2:
            return -self.m * epoch + self.m_max
        elif epoch < self.cycle_epoch:
            return self.m * (epoch - self.cycle_epoch // 2) + self.m_min
        else:
            return self.m_max


class OneCycleCosineMomentum(MomentumScheduler):

    def __init__(self, phase_epoch, max_epoch, m_min=0.85, m_max=0.95, verbose=0):
        """This adaption (proposed by fastAI) of the 1cycle policy uses the
        cosine to adapt the momentum.

        It should be used with the OneCycleCosine learning rate scheduler
        with the same phase_epoch and max_epoch settings.

        The momentum update consists of only two phases:
        1. decreasing from m_max to m_min
        2. increasing from m_min to m_max.

        Args:
            phase_epoch: Epoch where minimum momentum is achieved.

            max_epoch: Epoch where schedule ends. For epochs larger than
                       max_epoch, the momentum stays constant at m_max.

            m_min: Minimum momentum.

            m_max: Maximum momentum.

        """
        super(OneCycleCosineMomentum, self).__init__(self.one_cycle_cosine)
        self.m_min = m_min
        self.m_max = m_max
        self.phase_epoch = phase_epoch
        self.max_epoch = max_epoch
        if not max_epoch > phase_epoch:
            raise ValueError("max_epoch needs to be larger than phase_epoch.")

        self.name = "1cycle cosine momentum"

        # Period of decreasing and increasing cosines
        t0 = 2 * phase_epoch
        t1 = 2 * (max_epoch - phase_epoch)

        self.f1 = 1.0 / t0
        self.f2 = 1.0 / t1
        self.a = -0.5*(m_max - m_min)
        return

    def one_cycle_cosine(self, epoch: int, lr: float) -> float:
        # First, linear increase to lr_max
        if epoch <= self.phase_epoch:
            return self.a * (- np.cos(2*np.pi*self.f1*epoch) + 1) + self.m_max

        # Second, linear decrease back to lr_min
        elif epoch < self.max_epoch:
            return self.a * (np.cos(2*np.pi*self.f2*(epoch - self.phase_epoch)) + 1) + self.m_max

        # For even larger epochs, stay at lr_min
        else:
            return self.m_max
