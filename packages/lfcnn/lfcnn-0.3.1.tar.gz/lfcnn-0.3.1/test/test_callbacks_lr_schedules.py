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


"""Test lfcnn.callbacks.lr_schedules
"""
from pytest import approx

from lfcnn import callbacks


def test_step_decay():
    lr = callbacks.StepDecay(lr_init=1, decay=0.5, steps=1)
    epochs = range(5)
    lrs_true = [1, 1/2, 1/4, 1/8, 1/16]
    lrs_pred = [lr.schedule(e, 0) for e in epochs]
    assert lrs_pred == lrs_true

    lr = callbacks.StepDecay(lr_init=1, decay=0.5, steps=2)
    epochs = range(10)
    lrs_true = [1, 1, 1/2, 1/2, 1/4, 1/4, 1/8, 1/8, 1/16, 1/16]
    lrs_pred = [lr.schedule(e, 0) for e in epochs]
    assert lrs_pred == lrs_true

    lr = callbacks.StepDecay(lr_init=1, decay=0.5, steps=5)
    epochs = range(25)
    lrs_true = [1, 1, 1, 1, 1,
                1/2, 1/2, 1/2, 1/2, 1/2,
                1/4, 1/4, 1/4, 1/4, 1/4,
                1/8, 1/8, 1/8, 1/8, 1/8,
                1/16, 1/16, 1/16, 1/16, 1/16]
    lrs_pred = [lr.schedule(e, 0) for e in epochs]
    assert lrs_true == lrs_pred

    return


def test_exponential_decay():
    alpha = 2
    lr = callbacks.ExponentialDecay(lr_init=1, max_epoch=10, alpha=alpha, lr_min=1e-6)
    epochs = range(15)
    lrs_true = [1.0,
                0.13533614611912453,
                0.018316618549695154,
                0.0024797476418718226,
                0.00033646023197988025,
                4.6397823304688255e-05,
                7.142145070337043e-06,
                1.8294667378457895e-06,
                1.1104739109730704e-06,
                1.0131688131031582e-06,
                1e-06,
                1e-06,
                1e-06,
                1e-06,
                1e-06]
    lrs_pred = [lr.schedule(e, 0) for e in epochs]
    assert approx(lrs_pred, rel=0.01) == lrs_true

    return


def test_polynomial_decay():
    power = 2
    lr = callbacks.PolynomialDecay(lr_init=1, max_epoch=10, power=power, lr_min=1e-2)
    epochs = range(15)
    lrs_true = [1.0,
                0.8119,
                0.6436,
                0.4951,
                0.3664,
                0.2575,
                0.1684,
                0.0991,
                0.0496,
                0.0199,
                1e-2,
                1e-2,
                1e-2,
                1e-2,
                1e-2]
    lrs_pred = [lr.schedule(e, 0) for e in epochs]
    assert approx(lrs_pred, rel=0.01) == lrs_true

    return


def test_linear_decay():
    lr = callbacks.LinearDecay(lr_init=1, max_epoch=10, lr_min=0)
    epochs = range(15)
    lrs_true = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1,
                0.0, 0.0, 0.0,0.0, 0.0]
    lrs_pred = [lr.schedule(e, 0) for e in epochs]
    assert approx(lrs_pred, rel=0.01) == lrs_true

    return


def test_sigmoid_decay():
    alpha = 2
    lr = callbacks.SigmoidDecay(lr_init=1, max_epoch=10, alpha=alpha, lr_min=1e-4)
    epochs = range(15)
    lrs_true = [1,
                0.9996646834045467,
                0.997527624105681,
                0.9820155886589046,
                0.8808089982700845,
                0.50005,
                0.11929100172991534,
                0.018084411341095348,
                0.002572375894319111,
                0.00043531659545343145,
                0.00014539332891556415,
                0.0001061435601847545,
                0.00010083144487486137,
                0.0001001125239085389,
                0.00010001522845651481]
    lrs_pred = [lr.schedule(e, 0) for e in epochs]
    assert approx(lrs_pred, rel=0.01) == lrs_true

    return
