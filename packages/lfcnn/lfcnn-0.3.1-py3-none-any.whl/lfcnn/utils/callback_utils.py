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

"""Utilities to be used with LearningRateSchedulers and MomentumSchedulers.
Requires the matplotlib library."""

import matplotlib.pyplot as plt


def plot_scheduler(schedulers, max_epoch, log=False):
    """Plot one ore more learning rate or momentum schedulers for visual
    comparison.
    Uses the matplotlib library.

    Args:
        schedulers: Single instance or list of scheduler instances.
                    Scheduler instance cann be either a LearningRateScheduler
                    or a MomentumScheduler instance

        max_epoch: Maximum epoch to plot.

        log: Whether to scale the y-axis logarithmically.
    """

    if type(schedulers) != list:
        lr_schedulers = [schedulers]

    epochs = range(max_epoch)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for scheduler in schedulers:
        lrs = [scheduler.schedule(epoch, 0) for epoch in epochs]
        ax.plot(epochs, lrs, label=scheduler.name)

    if log:
        ax.set_yscale('log')
    plt.legend()
    plt.show()

    return
