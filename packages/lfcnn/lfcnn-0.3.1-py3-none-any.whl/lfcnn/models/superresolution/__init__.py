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


"""The LFCNN superresolution models.
"""

from .sas_conv import SasConv
from .dummy import Dummy


def get(model: str):
    """Given a model name, returns an lfcnn model instance.

    Args:
        model: Name of the model.

    Returns:
        Model instance.
    """
    # Available model classes
    classes = {
        "dummy": Dummy,
        "sasconv": SasConv
    }
    try:
        return classes[model.lower()]
    except KeyError:
        raise ValueError(f"Unknown superresolution model '{model}'.")
