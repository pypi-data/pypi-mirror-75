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

"""
Detecting harmonics.
"""

from typing import Tuple

from numpy import ndarray

from pymodalib.implementations.python.harmonics.harmonics import (
    harmonicfinder_impl_python as impl,
)


def harmonicfinder(
    signal: ndarray,
    fs: float,
    scale_min: float,
    scale_max: float,
    sigma: float = 1.05,
    time_resolution: float = 0.1,
    surrogates: int = 10,
    parallel: bool = True,
    crop: bool = True,
) -> Tuple[ndarray, ndarray, ndarray, ndarray]:
    """
    Harmonic-finder algorithm.

    Parameters
    ----------
    signal : ndarray
        [1D array] The signal to analyse.
    fs : float
        The sampling frequency of the signal.
    scale_min : float
        The minimum wavelet timescale.
    scale_max : float
        The maximum wavelet timescale.
    sigma : float
        (Default value = 1.05) Used to define the timescale increment. For example, `sigma = 1.05` is a timescale
        increment of 5 percent.
    time_resolution : float, optional
        (Default value = 0.1) The time resolution.
    surrogates : int
        (Default value = 10) The number of surrogates.
    parallel : bool
        (Default value = True) Whether to parallelize the algorithm, which provides a significant
        speed boost in many cases.
    crop : bool, optional
        (Default value = True) Whether to crop the results, removing the NaN values around the left and bottom edges.

    Returns
    -------
    freq : ndarray
        [1D array] The frequencies.
    res : ndarray
        [2D array] The raw harmonics.
    pos1 : ndarray
        [2D array] The number of surrogates which the raw harmonics are higher than at each point.
    pos2 : ndarray
        [2D array] The raw harmonics relative to the mean and standard deviation of the surrogate distribution.

    Notes
    -----
    Author: Lawrence Sheppard.

    .. [1] L.W. Sheppard, A. Stefanovska and P.V.E. McClintock,
        "Detecting the harmonics of oscillations with time-variable frequencies".
        {doi:10.1103/PhysRevE.83.016206}
    """
    return impl(
        signal,
        fs,
        scale_min,
        scale_max,
        sigma,
        time_resolution,
        surrogates,
        parallel,
        crop,
    )
