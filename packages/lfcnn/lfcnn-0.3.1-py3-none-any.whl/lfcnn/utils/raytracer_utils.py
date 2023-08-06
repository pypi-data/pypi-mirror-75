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

"""Utilities to convert depth maps as created by the IIIT Raytracer
See: https://gitlab.com/iiit-public/raytracer

"""
import json
from pathlib import Path

import numpy as np
import imageio
from plenpy.lightfields import LightField

from .data_utils import disp_from_depth, depth_from_distance_lf


def disp_from_folder(path, overwrite=False):
    """Create disparity maps for all depth files in a given folder.
    For each depth .pfm file, an according .json Raytracer description
    has to be available.
    """

    p = Path(path)
    print(f"Convertering dista files in folder {p}")

    files = [x for x in p.glob("*_dist.json")]
    files.sort()
    for i, file in enumerate(files):
        print(f"Converting {i+1} from {len(files)}. ", f"file: {file}")
        disp_from_json(file, overwrite=overwrite)


def disp_from_json(json_path, overwrite=False):
    """Reads the traced *_dist.json file and converts and saves a
    disparity map *_disp.pfm from the corresponding distance map *_dist.pfm.

    Args:
        paths : Path to the *_depth.json file.
        overwrite: Whether to overwrite a possibly existing disparity map.
    """
    # Set Path on Json File
    path = Path(json_path)
    path_dist = path.with_suffix(".pfm")
    # Replace _depth with _disp
    path_disp = Path(str(path_dist).replace("_dist.pfm", "_disp.pfm"))

    if path_disp.exists() and not overwrite:
        print("Skipping", path_disp)
        return

    # Load scene data form .json file
    with open(path) as fh:
        data = json.load(fh)

    # Read camera parameters
    focus_distance = data['camera']['focusDistance']
    image_distance = data['camera']['imageDistance']
    lens_radius = data['camera']['lensRadius']
    microlens_radius = data['camera']['microLensRadius']
    num_ang_steps = data['camera']['numAngSteps']
    s_max = data['camera']['numULenses']
    t_max = data['camera']['numVLenses']

    # Calculate the focus of the main lens using thin lens equation
    focal_length = (focus_distance * image_distance) / (focus_distance + image_distance)

    # Load distance data
    dist = LightField.from_file(path_dist, s_max, t_max)

    # Calculate depth from distance
    depth = depth_from_distance_lf(dist,
                                   r=microlens_radius,
                                   R=lens_radius,
                                   b=image_distance,
                                   g=focus_distance)

    # Get corresponding disparity
    disp = disp_from_depth(depth=depth,
                           f=focal_length,
                           g=focus_distance,
                           r=microlens_radius,
                           R=lens_radius,
                           numAngSteps=num_ang_steps)

    disp = LightField(disp)

    # Set disparity values for depth==0 to large value
    nan_vals = np.isnan(disp)
    if np.any(nan_vals):
        print("Encountered NAN values. Replacing with zero.")
        disp[nan_vals] = 0

    inf_vals = np.isinf(disp)
    if np.any(inf_vals):
        print("Encountered INF values. Replacing with zero.")
        disp[inf_vals] = 0

    imageio.imsave(path_disp, np.asarray(disp.get_2d(), dtype=dist.dtype))

    return


def depth_from_folder(path, overwrite=False):
    """Create disparity maps for all depth files in a given folder.
    For each depth .pfm file, an according .json Raytracer description
    has to be available.
    """

    p = Path(path)
    print(f"Convertering dist files in folder {p}")

    files = [x for x in p.glob("*_dist.json")]
    files.sort()
    for i, file in enumerate(files):
        print(f"Converting {i+1} from {len(files)}. ", f"file: {file}")
        disp_from_json(file, overwrite=overwrite)


def depth_from_json(json_path, overwrite=False):
    """Reads the traced *_dist.json file and converts and saves a
    depth map *_depth.pfm from the corresponding distance map *_dist.pfm.

    Args:
        paths : Path to the *_depth.json file.
        overwrite: Whether to overwrite a possibly existing depth map.
    """
    # Set Path on Json File
    path = Path(json_path)
    path_dist = path.with_suffix(".pfm")
    path_depth = Path(str(path_dist).replace("_dist.pfm", "_depth.pfm"))

    if path_depth.exists() and not overwrite:
        return

    # Load scene data form .json file
    with open(path) as fh:
        data = json.load(fh)

    # Read camera parameters
    focus_distance = data['camera']['focusDistance']
    image_distance = data['camera']['imageDistance']
    lens_radius = data['camera']['lensRadius']
    microlens_radius = data['camera']['microLensRadius']
    s_max = data['camera']['numULenses']
    t_max = data['camera']['numVLenses']

    # Load distance data
    dist = LightField.from_file(path_dist, s_max, t_max)

    # Calculate depth from distance
    depth = depth_from_distance_lf(dist,
                                   r=microlens_radius,
                                   R=lens_radius,
                                   b=image_distance,
                                   g=focus_distance)

    depth = LightField(depth)

    imageio.imsave(path_depth, np.asarray(depth.get_2d(), dtype=dist.dtype))

    return

