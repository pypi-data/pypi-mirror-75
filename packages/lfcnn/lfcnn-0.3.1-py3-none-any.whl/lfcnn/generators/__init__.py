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


"""The LFCNN generators module.
"""
from .generators import BaseGenerator
from .generators import LfGenerator
from .generators import LfDownSampleGenerator
from .generators import DisparityGenerator
from .generators import CentralAndDisparityGenerator


def get(generator: str):
    """Given a generator name, returns an lfcnn generator instance.

    Args:
        generator: Name of the generator.

    Returns:
        Generator instance.
    """
    # Available generator classes
    classes = {
        "lfgenerator": LfGenerator,
        "disparitygenerator": DisparityGenerator,
        "centralanddisparitygenerator": CentralAndDisparityGenerator,
        "lfdownsamplegenerator": LfDownSampleGenerator
    }
    try:
        return classes[generator.lower()]
    except KeyError:
        raise ValueError(f"Unknown generator '{generator}'.")
