#  PyMODAlib, a Python implementation of the algorithms from MODA (Multiscale Oscillatory Dynamics Analysis).
#  Copyright (C) 2020 Lancaster University
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.

# The version of the MATLAB Runtime required.
import os
import re
from typing import List, Optional

from utils.Platform import Platform

MATLAB_RUNTIME_VERSION = 96

platform = Platform.get()
regexp = re.compile("v[0-9]{2}")


def is_runtime_valid() -> bool:
    versions = get_matlab_runtime_versions()
    return any([v == MATLAB_RUNTIME_VERSION for v in versions])


def get_matlab_runtime_versions() -> List[int]:
    versions = []
    path_var = "path"

    for var in os.environ.get(path_var).split(os.pathsep):
        if platform is Platform.WINDOWS:
            version = get_runtime_version_windows(var)
            versions.append(version)

    return versions


def get_runtime_version_windows(var: str) -> Optional[int]:
    if "MATLAB Runtime" in var and "runtime" in var:
        substrings = regexp.findall(var)
        try:
            return int(substrings[0][1:])
        except ValueError or IndexError:
            print(f"Error parsing MATLAB Runtime version from {var}")

    return None
