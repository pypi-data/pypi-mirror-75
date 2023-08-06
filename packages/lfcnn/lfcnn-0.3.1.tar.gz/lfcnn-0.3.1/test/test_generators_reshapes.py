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


"""Test lfcnn.generator
"""
import numpy as np

from lfcnn.generators.reshapes import lf_identity
from lfcnn.generators.reshapes import lf_subaperture_stream
from lfcnn.generators.reshapes import lf_subaperture_stack
from lfcnn.generators.reshapes import lf_subaperture_channel_stack
from lfcnn.generators.reshapes import lf_distributed
from lfcnn.generators.reshapes import lf_crosshair
from lfcnn.generators.reshapes import lf_crosshair_stacked

ALL_RESHAPES = [lf_identity,
                lf_subaperture_stream,
                lf_subaperture_stack,
                lf_subaperture_channel_stack,
                lf_distributed,
                lf_crosshair,
                lf_crosshair_stacked]


def test_reshape_functions():

    # Test mono LF
    lf = np.random.rand(32, 9, 9, 32, 32, 1)
    labels = ["string", np.random.rand(32, 32, 32)]

    for reshape in ALL_RESHAPES:
        lf_r, labels_r = reshape(lf, labels)
        # Check that labels are unaltered
        assert labels_r == labels

    # Test RGB LF
    lf = np.random.rand(32, 9, 9, 32, 32, 3)
    labels = ["string", np.random.rand(32, 32, 32)]

    for reshape in ALL_RESHAPES:
        lf_r, labels_r = reshape(lf, labels)
        # Check that labels are unaltered
        assert labels_r == labels

    # Test multispectral LF
    lf = np.random.rand(32, 9, 9, 32, 32, 30)
    labels = ["string", np.random.rand(32, 32, 32)]

    for reshape in ALL_RESHAPES:
        lf_r, labels_r = reshape(lf, labels)
        # Check that labels are unaltered
        assert labels_r == labels

    return


def test_lf_identiy():

    lf = np.random.rand(32, 9, 9, 32, 32, 3)
    labels = []

    lf_r, _ = lf_identity(lf, labels)
    assert np.array_equal(lf_r, lf)

    return


def test_lf_subaperture_stream():
    # Generates list of subapertures

    lf = np.random.rand(32, 3, 3, 32, 32, 3)
    labels = []

    lf_r, _ = lf_subaperture_stream(lf, labels)

    sai1 = lf_r['input_1']
    sai2 = lf_r['input_2']
    sai3 = lf_r['input_3']
    sai4 = lf_r['input_4']
    sai5 = lf_r['input_5']
    sai6 = lf_r['input_6']
    sai7 = lf_r['input_7']
    sai8 = lf_r['input_8']
    sai9 = lf_r['input_9']

    assert np.array_equal(sai1, lf[:, 0, 0])
    assert np.array_equal(sai2, lf[:, 0, 1])
    assert np.array_equal(sai3, lf[:, 0, 2])
    assert np.array_equal(sai4, lf[:, 1, 0])
    assert np.array_equal(sai5, lf[:, 1, 1])
    assert np.array_equal(sai6, lf[:, 1, 2])
    assert np.array_equal(sai7, lf[:, 2, 0])
    assert np.array_equal(sai8, lf[:, 2, 1])
    assert np.array_equal(sai9, lf[:, 2, 2])

    return


def test_lf_subaperture_stack():
    # Reshapes (b, u, v, s, t, ch) -> (b, s, t, u*v*ch)

    lf = np.random.rand(32, 3, 3, 32, 32, 3)
    labels = []

    lf_r, _ = lf_subaperture_stack(lf, labels)

    assert np.array_equal(lf_r[:, :, :, 0], lf[:, 0, 0, :, :, 0])
    assert np.array_equal(lf_r[:, :, :, 1], lf[:, 0, 0, :, :, 1])
    assert np.array_equal(lf_r[:, :, :, 2], lf[:, 0, 0, :, :, 2])
    assert np.array_equal(lf_r[:, :, :, 3], lf[:, 0, 1, :, :, 0])
    assert np.array_equal(lf_r[:, :, :, 4], lf[:, 0, 1, :, :, 1])
    assert np.array_equal(lf_r[:, :, :, 5], lf[:, 0, 1, :, :, 2])
    assert np.array_equal(lf_r[:, :, :, 6], lf[:, 0, 2, :, :, 0])
    assert np.array_equal(lf_r[:, :, :, 7], lf[:, 0, 2, :, :, 1])
    assert np.array_equal(lf_r[:, :, :, 8], lf[:, 0, 2, :, :, 2])
    assert np.array_equal(lf_r[:, :, :, 9], lf[:, 1, 0, :, :, 0])
    assert np.array_equal(lf_r[:, :, :, 10], lf[:, 1, 0, :, :, 1])
    assert np.array_equal(lf_r[:, :, :, 11], lf[:, 1, 0, :, :, 2])
    assert np.array_equal(lf_r[:, :, :, 12], lf[:, 1, 1, :, :, 0])
    assert np.array_equal(lf_r[:, :, :, 13], lf[:, 1, 1, :, :, 1])
    assert np.array_equal(lf_r[:, :, :, 14], lf[:, 1, 1, :, :, 2])
    assert np.array_equal(lf_r[:, :, :, 15], lf[:, 1, 2, :, :, 0])
    assert np.array_equal(lf_r[:, :, :, 16], lf[:, 1, 2, :, :, 1])
    assert np.array_equal(lf_r[:, :, :, 17], lf[:, 1, 2, :, :, 2])
    assert np.array_equal(lf_r[:, :, :, 18], lf[:, 2, 0, :, :, 0])
    assert np.array_equal(lf_r[:, :, :, 19], lf[:, 2, 0, :, :, 1])
    assert np.array_equal(lf_r[:, :, :, 20], lf[:, 2, 0, :, :, 2])
    assert np.array_equal(lf_r[:, :, :, 21], lf[:, 2, 1, :, :, 0])
    assert np.array_equal(lf_r[:, :, :, 22], lf[:, 2, 1, :, :, 1])
    assert np.array_equal(lf_r[:, :, :, 23], lf[:, 2, 1, :, :, 2])
    assert np.array_equal(lf_r[:, :, :, 24], lf[:, 2, 2, :, :, 0])
    assert np.array_equal(lf_r[:, :, :, 25], lf[:, 2, 2, :, :, 1])
    assert np.array_equal(lf_r[:, :, :, 26], lf[:, 2, 2, :, :, 2])
    assert lf_r.shape == (32, 32, 32, 27)

    return


def test_lf_subaperture_ch_stack():
    # Reshapes (b, u, v, s, t, ch) -> (b, s, t, u*v, ch)

    lf = np.random.rand(32, 3, 3, 32, 32, 3)
    labels = []

    lf_r, _ = lf_subaperture_channel_stack(lf, labels)

    assert np.array_equal(lf_r[:, :, :, 0, 0], lf[:, 0, 0, :, :, 0])
    assert np.array_equal(lf_r[:, :, :, 0, 1], lf[:, 0, 0, :, :, 1])
    assert np.array_equal(lf_r[:, :, :, 0, 2], lf[:, 0, 0, :, :, 2])
    assert np.array_equal(lf_r[:, :, :, 1, 0], lf[:, 0, 1, :, :, 0])
    assert np.array_equal(lf_r[:, :, :, 1, 1], lf[:, 0, 1, :, :, 1])
    assert np.array_equal(lf_r[:, :, :, 1, 2], lf[:, 0, 1, :, :, 2])
    assert np.array_equal(lf_r[:, :, :, 2, 0], lf[:, 0, 2, :, :, 0])
    assert np.array_equal(lf_r[:, :, :, 2, 1], lf[:, 0, 2, :, :, 1])
    assert np.array_equal(lf_r[:, :, :, 2, 2], lf[:, 0, 2, :, :, 2])
    assert np.array_equal(lf_r[:, :, :, 3, 0], lf[:, 1, 0, :, :, 0])
    assert np.array_equal(lf_r[:, :, :, 3, 1], lf[:, 1, 0, :, :, 1])
    assert np.array_equal(lf_r[:, :, :, 3, 2], lf[:, 1, 0, :, :, 2])
    assert np.array_equal(lf_r[:, :, :, 4, 0], lf[:, 1, 1, :, :, 0])
    assert np.array_equal(lf_r[:, :, :, 4, 1], lf[:, 1, 1, :, :, 1])
    assert np.array_equal(lf_r[:, :, :, 4, 2], lf[:, 1, 1, :, :, 2])
    assert np.array_equal(lf_r[:, :, :, 5, 0], lf[:, 1, 2, :, :, 0])
    assert np.array_equal(lf_r[:, :, :, 5, 1], lf[:, 1, 2, :, :, 1])
    assert np.array_equal(lf_r[:, :, :, 5, 2], lf[:, 1, 2, :, :, 2])
    assert np.array_equal(lf_r[:, :, :, 6, 0], lf[:, 2, 0, :, :, 0])
    assert np.array_equal(lf_r[:, :, :, 6, 1], lf[:, 2, 0, :, :, 1])
    assert np.array_equal(lf_r[:, :, :, 6, 2], lf[:, 2, 0, :, :, 2])
    assert np.array_equal(lf_r[:, :, :, 7, 0], lf[:, 2, 1, :, :, 0])
    assert np.array_equal(lf_r[:, :, :, 7, 1], lf[:, 2, 1, :, :, 1])
    assert np.array_equal(lf_r[:, :, :, 7, 2], lf[:, 2, 1, :, :, 2])
    assert np.array_equal(lf_r[:, :, :, 8, 0], lf[:, 2, 2, :, :, 0])
    assert np.array_equal(lf_r[:, :, :, 8, 1], lf[:, 2, 2, :, :, 1])
    assert np.array_equal(lf_r[:, :, :, 8, 2], lf[:, 2, 2, :, :, 2])
    assert lf_r.shape == (32, 32, 32, 9, 3)

    return


def test_lf_distributed():
    # Reshapes (b, u, v, s, t, ch) -> (u*v, b, s, t, ch)

    lf = np.random.rand(32, 3, 3, 32, 32, 3)
    labels = []

    lf_r, _ = lf_distributed(lf, labels)

    assert np.array_equal(lf_r[:, 0, :, :, 0], lf[:, 0, 0, :, :, 0])
    assert np.array_equal(lf_r[:, 0, :, :, 1], lf[:, 0, 0, :, :, 1])
    assert np.array_equal(lf_r[:, 0, :, :, 2], lf[:, 0, 0, :, :, 2])
    assert np.array_equal(lf_r[:, 1, :, :, 0], lf[:, 0, 1, :, :, 0])
    assert np.array_equal(lf_r[:, 1, :, :, 1], lf[:, 0, 1, :, :, 1])
    assert np.array_equal(lf_r[:, 1, :, :, 2], lf[:, 0, 1, :, :, 2])
    assert np.array_equal(lf_r[:, 2, :, :, 0], lf[:, 0, 2, :, :, 0])
    assert np.array_equal(lf_r[:, 2, :, :, 1], lf[:, 0, 2, :, :, 1])
    assert np.array_equal(lf_r[:, 2, :, :, 2], lf[:, 0, 2, :, :, 2])
    assert np.array_equal(lf_r[:, 3, :, :, 0], lf[:, 1, 0, :, :, 0])
    assert np.array_equal(lf_r[:, 3, :, :, 1], lf[:, 1, 0, :, :, 1])
    assert np.array_equal(lf_r[:, 3, :, :, 2], lf[:, 1, 0, :, :, 2])
    assert np.array_equal(lf_r[:, 4, :, :, 0], lf[:, 1, 1, :, :, 0])
    assert np.array_equal(lf_r[:, 4, :, :, 1], lf[:, 1, 1, :, :, 1])
    assert np.array_equal(lf_r[:, 4, :, :, 2], lf[:, 1, 1, :, :, 2])
    assert np.array_equal(lf_r[:, 5, :, :, 0], lf[:, 1, 2, :, :, 0])
    assert np.array_equal(lf_r[:, 5, :, :, 1], lf[:, 1, 2, :, :, 1])
    assert np.array_equal(lf_r[:, 5, :, :, 2], lf[:, 1, 2, :, :, 2])
    assert np.array_equal(lf_r[:, 6, :, :, 0], lf[:, 2, 0, :, :, 0])
    assert np.array_equal(lf_r[:, 6, :, :, 1], lf[:, 2, 0, :, :, 1])
    assert np.array_equal(lf_r[:, 6, :, :, 2], lf[:, 2, 0, :, :, 2])
    assert np.array_equal(lf_r[:, 7, :, :, 0], lf[:, 2, 1, :, :, 0])
    assert np.array_equal(lf_r[:, 7, :, :, 1], lf[:, 2, 1, :, :, 1])
    assert np.array_equal(lf_r[:, 7, :, :, 2], lf[:, 2, 1, :, :, 2])
    assert np.array_equal(lf_r[:, 8, :, :, 0], lf[:, 2, 2, :, :, 0])
    assert np.array_equal(lf_r[:, 8, :, :, 1], lf[:, 2, 2, :, :, 1])
    assert np.array_equal(lf_r[:, 8, :, :, 2], lf[:, 2, 2, :, :, 2])
    assert lf_r.shape == (32, 9, 32, 32, 3)

    return


def test_lf_crosshair():
    # Creates crosshair -, |, \, /

    lf = np.random.rand(32, 3, 3, 32, 32, 3)
    labels = []

    lf_r, _ = lf_crosshair(lf, labels)

    horz = lf_r['input_1']
    vert = lf_r['input_2']
    diag1 = lf_r['input_3']
    diag2 = lf_r['input_4']

    for tmp in [horz, vert, diag1, diag2]:
        assert tmp.shape == (32, 3, 32, 32, 3)

    diag1_ref = np.zeros((32, 3, 32, 32, 3))
    diag1_ref[:, 0] = lf[:, 0, 0]
    diag1_ref[:, 1] = lf[:, 1, 1]
    diag1_ref[:, 2] = lf[:, 2, 2]

    diag2_ref = np.zeros((32, 3, 32, 32, 3))
    diag2_ref[:, 0] = lf[:, 2, 0]
    diag2_ref[:, 1] = lf[:, 1, 1]
    diag2_ref[:, 2] = lf[:, 0, 2]

    assert np.array_equal(horz, lf[:, 1, :, :, :])
    assert np.array_equal(vert, lf[:, :, 1, :, :])
    assert np.array_equal(diag1, diag1_ref)
    assert np.array_equal(diag2, diag2_ref)

    return


def test_lf_crosshair_stacked():
    # Creates crosshair -, |, \, /

    lf = np.random.rand(32, 3, 3, 32, 32, 3)
    labels = []

    lf_r, _ = lf_crosshair_stacked(lf, labels)

    horz = lf_r['input_1']
    vert = lf_r['input_2']
    diag1 = lf_r['input_3']
    diag2 = lf_r['input_4']

    for tmp in [horz, vert, diag1, diag2]:
        assert tmp.shape == (32, 32, 32, 3*3)

    diag1_ref = np.zeros((32, 32, 32, 3*3))
    diag1_ref[:, :, :, 0:3] = lf[:, 0, 0, :]
    diag1_ref[:, :, :, 3:6] = lf[:, 1, 1, :]
    diag1_ref[:, :, :, 6:9] = lf[:, 2, 2, :]

    diag2_ref = np.zeros((32, 32, 32, 3*3))
    diag2_ref[:, :, :, 0:3] = lf[:, 2, 0, :]
    diag2_ref[:, :, :, 3:6] = lf[:, 1, 1, :]
    diag2_ref[:, :, :, 6:9] = lf[:, 0, 2, :]

    assert np.array_equal(horz[:, :, :, 0:3], lf[:, 1, 0, :, :])
    assert np.array_equal(horz[:, :, :, 3:6], lf[:, 1, 1, :, :])
    assert np.array_equal(horz[:, :, :, 6:9], lf[:, 1, 2, :, :])
    assert np.array_equal(vert[:, :, :, 0:3], lf[:, 0, 1, :, :])
    assert np.array_equal(vert[:, :, :, 3:6], lf[:, 1, 1, :, :])
    assert np.array_equal(vert[:, :, :, 6:9], lf[:, 2, 1, :, :])
    assert np.array_equal(diag1, diag1_ref)
    assert np.array_equal(diag2, diag2_ref)

    return
