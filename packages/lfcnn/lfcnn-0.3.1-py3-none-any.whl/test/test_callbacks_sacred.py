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


"""Test lfcnn.callbacks.sacred
"""
from pytest import approx, fixture
import time

from sacred import Experiment

from lfcnn import callbacks

@fixture()
def ex():
    return Experiment("Test experiment")


def test_sacred_metrics_logger(ex):
    messages = {}
    epochs = 10

    @ex.main
    def main_function(_run):

        callback = callbacks.SacredMetricLogger(_run)

        for i in range(epochs):
            logs = {"loss": i, "val_loss": i*i}
            callback.on_epoch_end(i, logs)
        messages["messages"] = ex.current_run._metrics.get_last_metrics()

    ex.run()
    assert ex.current_run is not None
    messages = messages["messages"]
    loss_log = [m.value for m in messages if m.name == "loss"]
    val_loss_log = [m.value for m in messages if m.name == "val_loss"]

    assert len(loss_log) == epochs
    assert len(val_loss_log) == epochs
    assert loss_log == [i for i in range(epochs)]
    assert val_loss_log == [i*i for i in range(epochs)]


def test_sacred_epoch_logger(ex):
    messages = {}
    epochs = 10

    @ex.main
    def main_function(_run):

        callback = callbacks.SacredEpochLogger(_run, epochs)

        for i in range(epochs):
            logs = {"loss": i, "val_loss": i*i}
            callback.on_epoch_begin(i, logs)
        messages["messages"] = ex.current_run._metrics.get_last_metrics()

    ex.run()
    assert ex.current_run is not None
    messages = messages["messages"]
    loss_log = [m.value for m in messages if m.name == "epoch"]

    assert len(loss_log) == epochs
    assert loss_log == [f"{i+1} / {epochs}" for i in range(epochs)]


def test_sacred_lr_logger(ex):
    messages = {}
    epochs = 10

    @ex.main
    def main_function(_run):

        callback = callbacks.SacredLearningRateLogger(_run)

        for i in range(epochs):
            logs = {"momentum": i, "lr": i*i}
            callback.on_epoch_end(i, logs)

        messages["messages"] = ex.current_run._metrics.get_last_metrics()

    ex.run()
    assert ex.current_run is not None
    messages = messages["messages"]
    lr_log = [m.value for m in messages if m.name == "lr"]
    momentum_log = [m.value for m in messages if m.name == "momentum"]

    assert len(lr_log) == epochs
    assert len(momentum_log) == epochs
    assert lr_log == [i*i for i in range(epochs)]
    assert momentum_log == [i for i in range(epochs)]


def test_sacred_time_logger(ex):
    messages = {}
    epochs = 10

    @ex.main
    def main_function(_run):

        callback = callbacks.SacredTimeLogger(_run)

        for i in range(epochs):
            callback.on_epoch_begin(i)
            time.sleep((i + 1)*0.1)
            callback.on_epoch_end(i)

        messages["messages"] = ex.current_run._metrics.get_last_metrics()

    ex.run()
    assert ex.current_run is not None
    messages = messages["messages"]
    time_log = [m.value for m in messages if m.name == "epoch_time"]

    assert len(time_log) == epochs
    assert approx(time_log, rel=0.05) == [(i + 1)*0.1 for i in range(epochs)]
