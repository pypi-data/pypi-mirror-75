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

"""Utilities to convert between depth and disparity for microlens array
based unfocues plenoptic cameras in the thin lens approximation.

Mostly to be used with raytracer_utils and the depth map
rendered by the IIIT Raytracer.
"""
from itertools import product

import numpy as np
from numpy.core import ndarray
from typing import Union


def depth_from_distance(dist, r, b, offset=None):
    """Calculte depth from distance values, i.e. given the norm of a
    ray distance = |(x, y, z)|, calculate the depth z.

    Args:
        dist: Distance map of shape (s, t, 1)

        r: Microlens radius

        b: Image distance

        offset: Sensor offset. Can be used for light field subapertures that show
                an effective sensor center offset.

    Returns:

    """
    s_max, t_max, ch = dist.shape
    c = np.asarray([s_max / 2, t_max / 2])

    # Pixel pitch
    pp = 2 * r

    f_eff = b/pp
    f_eff_inv = 1/f_eff

    # Meshgrid
    x = np.arange(s_max) + 0.5
    y = np.arange(t_max) + 0.5
    x, y = np.meshgrid(x, y, indexing='ij')

    offset = offset if offset is not None else 0
    c_curr = c + offset

    # Calculate camera matrix inverse
    # K = np.asarray([[f_eff, 0, c_curr[0]], [0, f_eff, c_curr[1]], [0, 0, 1]])

    K_inv = np.asarray([[f_eff_inv, 0,    -c_curr[0]*f_eff_inv],
                        [0,    f_eff_inv, -c_curr[1]*f_eff_inv],
                        [0,    0,    1]])

    coords = np.stack([x, y, np.ones(x.shape)], axis=-1)

    corr = np.einsum('xy, sty -> stx', K_inv, coords)
    corr = np.linalg.norm(corr, axis=-1, keepdims=True)
    depth = (dist.copy()).astype(np.float64) / corr

    return depth


def depth_from_distance_lf(lf_dist, r, R, b, g):
    u_max, v_max, s_max, t_max, ch = lf_dist.shape
    u_c, v_c = u_max // 2, v_max // 2

    # Pixel pitch
    pp = 2 * r

    # LF baseline
    x_u = 2 * R / u_max / pp
    x_v = 2 * R / v_max / pp

    # Init with depth
    lf_depth = np.zeros(lf_dist.shape)

    for u, v in product(range(u_max), range(v_max)):
        du, dv = u - u_c, v - v_c

        offset = np.asarray([du, dv]) * np.asarray([x_u, x_v]) * b/g
        lf_depth[u, v] = depth_from_distance(np.asarray(lf_dist[u, v]),
                                             r=r, b=b, offset=offset)

    return lf_depth


def depth_from_disp(disp: float,
                    f: float,
                    g: float,
                    r: float,
                    R: float,
                    numAngSteps: int):
    """Calculate the depth from disparity given the
    camera parameters.

    Note that all given camera parameters need to be in the same
    SI units, e.g. all in meters.

    Inverse of disp_from_depth.

    Args:
        disp: Disparity to convert.
        f: Main lens focal length
        g: Focus distance (distance of the focal plane)
        r: Micro lens radius
        R: Main lens radius
        numAngSteps: Angular resolution
                     (number of subapertures per dimension)
                     (number of pixels underneath microlens)

    Returns:
        depth (in same unit as camera parameters, e.g. in meters)
    """
    return (g * R * f) / (f * R - disp * numAngSteps * r * (f - g))


def disp_from_depth(depth: Union[float, ndarray],
                    f: float,
                    g: float,
                    r: float,
                    R: float,
                    numAngSteps):
    """Calculate the disparity from depth given the
    camera parameters.

    Note that all given camera parameters need to be in the same
    SI units, e.g. all in meters.

    Inverse of deps_from_disp.

    Args:
        depth: Depth to convert.
        f: Main lens focal length
        g: Focus distance (distance of the focal plane)
        r: Micro lens radius
        R: Main lens radius
        numAngSteps: Angular resolution
                     (number of subapertures per dimension)
                     (number of pixels underneath microlens)

    Returns:
        disparity (in pixels)
    """

    num = -(R * f * (g - depth))               # float or array
    denum = r * (f - g) * numAngSteps * depth  # float or array

    return num / denum  # element-wise division for array
