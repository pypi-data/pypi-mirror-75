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


"""The LFCNN layers module.
"""
from .layers import res_block_2d, res_block_3d
from .layers import reshape_3d_to_2d
from .layers import sample_down_2d, sample_up_2d, sample_down_3d, sample_up_3d


def get(layer: str) -> callable:
    """Given a layer name, returns an lfcnn layer callable.

    Args:
        layer: Name of the layer.

    Returns:
        Layer callable.
    """
    # Available layer classes
    classes = {
        "res_block_2d": res_block_2d,
        "res_block_3d": res_block_3d,
        "reshape_3d_to_2d": reshape_3d_to_2d,
        "sample_down_2d": sample_down_2d,
        "sample_up_2d": sample_up_2d,
        "sample_down_3d": sample_down_3d,
        "sample_up_3d": sample_up_3d
    }
    try:
        return classes[layer.lower()]
    except KeyError:
        raise ValueError(f"Unknown layer '{layer}'.")
