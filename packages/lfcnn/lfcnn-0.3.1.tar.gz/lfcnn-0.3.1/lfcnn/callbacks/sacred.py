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

"""Callbacks to log metrics and other information to Sacred."""

import time

from tensorflow.keras.callbacks import Callback


class SacredMetricLogger(Callback):
    """Callback that logs all losses and metrics to Sacred."""

    def __init__(self, run):
        super(SacredMetricLogger, self).__init__()
        self.run = run

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}

        for k in logs:
            self.run.log_scalar(k, logs[k], epoch)


class SacredTimeLogger(Callback):
    """Callback that logs times per epoch to Sacred."""
    def __init__(self, run):
        super(SacredTimeLogger, self).__init__()
        self.run = run

    def on_epoch_begin(self, epoch, logs=None):
        self.epoch_time_start = time.time()

    def on_epoch_end(self, epoch, logs=None):
        ep_time = time.time() - self.epoch_time_start
        self.run.log_scalar("epoch_time", ep_time, epoch)


class SacredEpochLogger(Callback):
    """Callback that logs the current epoch to Sacred."""
    def __init__(self, run, epochs):
        super(SacredEpochLogger, self).__init__()
        self.epochs = epochs
        self.run = run

    def on_epoch_begin(self, epoch, logs=None):
        self.run.log_scalar("epoch", f"{epoch+1} / {self.epochs}", epoch)


class SacredLearningRateLogger(Callback):
    """Callback that logs learning rate to Sacred."""

    def __init__(self, run):
        super(SacredLearningRateLogger, self).__init__()
        self.run = run

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        if 'lr' in logs:
                self.run.log_scalar('lr', logs['lr'], epoch)
        if 'momentum' in logs:
                self.run.log_scalar('momentum', logs['momentum'], epoch)
