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
import warnings

import numpy as np
from numpy import ndarray


def contourf(
    axes, x: ndarray, y: ndarray, z: ndarray, levels: int = 256, *args, **kwargs
) -> None:
    """
    Plots a contour plot in PyMODA style. Useful for easily plotting a wavelet transform, etc.

    This function is a Wrapper around matplotlib's 'contourf'.

    Parameters
    ----------
    axes
        The Axes object to plot on.
    x, y : ndarray
        The coordinates of the values in Z.

        X and Y must both be 2-D with the same shape as Z (e.g. created via numpy.meshgrid),
        or they must both be 1-D such that len(X) == M is the number of columns in Z and
        len(Y) == N is the number of rows in Z.
    z : ndarray
        The height values over which the contour is drawn.
    levels : int
        Determines the number and positions of the contour lines / regions.

        If an int n, use n data intervals; i.e. draw n+1 contour lines. The level heights are automatically chosen.

        If array-like, draw contour lines at the specified levels. The values must be in increasing order.

    .. note::
        Documentation copied from the relevant matplotlib function, `matplotlib.pyplot.contourf`.
    """
    axes.contourf(
        x,
        y,
        z,
        levels,
        vmin=np.nanmin(z),
        vmax=np.nanmax(z),
        cmap=colormap(),
        *args,
        **kwargs
    )


def colormap() -> "LinearSegmentedColormap":
    """
    Loads the colormap used by PyMODA.

    Returns
    -------
    LinearSegmentedColormap
        The colormap, as an object which can be passed to matplotlib functions.
    """
    from matplotlib.colors import LinearSegmentedColormap
    from scipy.io import loadmat
    import os

    here = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(here, "colormap.mat")
    cmap = loadmat(filename).get("cmap")

    if cmap is None:
        warnings.warn(
            "Could not load colormap. The colormap data is not supplied with "
            "source-distributions of PyMODAlib.",
            RuntimeWarning,
        )
        return "jet"

    return LinearSegmentedColormap.from_list("colours", cmap, N=len(cmap), gamma=1.0)
