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
from tensorflow.keras.callbacks import Callback

import numpy as np


class LearningRateFinder(Callback):

    def __init__(self,
                 lr_min: float,
                 lr_max: float,
                 num_batches: int,
                 sweep: str = "exponential",
                 beta: float = 0.95,
                 verbose: bool = False):
        """Learning rate finder according to Leslie Smith.
        Starting from a small learning rate, the learning rate is increased
        after each **batch** up to the maximum learning rate.
        The corresponding training loss (per batch) is logged.
        The optimal learning rate corresponds to the point, where the
        training loss has the steepest slope.
        For OneCycle learning rate schedulers, the maximum and minimum
        learning rates can be found using this LearningRateFinder.

        See: Smith, Leslie N.
        "A disciplined approach to neural network hyper-parameters:
        Part 1--learning rate, batch size, momentum, and weight decay."
        arXiv preprint arXiv:1803.09820 (2018).

        See Also:
        Blog post by Sylvain Gugger of fastai
        https://sgugger.github.io/how-do-you-find-a-good-learning-rate.html

        Args:
            lr_min: Minimum learning rate, start point.

            lr_max: Maximum learning rate, end point.

            num_batches: Number of batches per single epoch.

            sweep: Whether to perform a linear increase of the learning rate
                   (sweep = "linear") or an exponential one
                   (sweep = "exponential", default).

            beta: Smoothing factor for logged loss_avg.

            verbose: Whether to log verbose info.
        """
        super(LearningRateFinder, self).__init__()
        self._beta = beta
        self._lr_min = lr_min
        self._lr_max = lr_max

        self._lr_steps = None
        if "lin" in sweep.lower():
            self._lr_steps = np.linspace(lr_min, lr_max, num_batches, endpoint=True)
        elif "exp" in sweep.lower():
            self._lr_steps = np.geomspace(lr_min, lr_max, num_batches, endpoint=True)
        else:
            raise ValueError(f"Unknown sweep '{sweep}'")

        self.verbose = verbose
        self.lrs = []
        self.losses = []
        self.avg_losses = []
        self.avg_loss = 0
        self.mses = []
        self.avg_mses = []
        self.avg_mse = 0

    def schedule(self, batch: int, lr: float) -> float:
        pass

    def on_batch_begin(self, batch, logs=None):

        # Increase the learning rate for the current batch
        lr = self._lr_steps[batch]
        K.set_value(self.model.optimizer.learning_rate, lr)

        if self.verbose > 0:
            print(f'\nBatch {batch + 1}: LearningRateFinder setting learning '
                  f'rate to {lr}')

    def on_batch_end(self, batch, logs=None):
        # Log the learning rate
        lr = K.get_value(self.model.optimizer.learning_rate)
        self.lrs.append(lr)

        # Log the loss
        logs = logs or {}
        loss = logs['loss']
        self.losses.append(loss)
        self.avg_loss = self._beta * self.avg_loss + (1 - self._beta) * loss
        self.avg_losses.append(self.avg_loss)
        logs['avg_loss'] = self.avg_loss

        # Try to also log metric as loss may include kernel regularizer
        try:
            mse = logs['mean_square_error']
            self.mses.append(mse)
            self.avg_mse = self._beta * self.avg_mse + (1 - self._beta) * mse
            self.avg_mses.append(self.avg_mse)
            logs['avg_mse'] = self.avg_mse
        except KeyError:
            pass
