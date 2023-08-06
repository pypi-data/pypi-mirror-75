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
import random
from typing import Tuple

import numpy as np
from numpy import ndarray
from numpy.random import permutation as randperm

from pymodalib.utils.decorators import experimental

"""
Translation of `surrcalc` from MODA.

STATUS:
- RP, FT, AAFT, IAFFT1, tshift and CPP surrogates are implemented.
- IAFFT1 needs to be fixed (it crashes).
- IAAFT is not implemented yet.
- WIAAFT requires a function "modwt" which is not implemented in scipy. Not implemented yet.
- Results may need to be checked for surrogates.
"""

_RP = "RP"
_FT = "FT"
_AAFT = "AAFT"
_IAFFT1 = "IAAFT1"
_IAFFT2 = "IAAFT2"
_WIAFFT = "WIAAFT"
_tshift = "tshift"
_CPP = "CPP"


@experimental
def surrogate_calc(
    signal: ndarray,
    N: int,
    method: str,
    pp: bool,
    fs: float,
    return_params: bool = False,
) -> Tuple[ndarray, "Params"]:
    """
    Calculates surrogates.
    """
    sig = signal
    surr = np.empty((N, len(sig)), dtype=np.float64)

    params = Params()
    origsig = sig
    params.origsig = origsig
    params.method = method
    params.numsurr = N
    params.fs = fs

    if pp:
        sig, time, ks, ke = surr_preprocessing(sig, fs)
        params.preprocessing = True
        params.cutsig = sig
        params.sigstart = ks
        params.sigend = ke
    else:
        time = np.linspace(0, len(sig), int(len(sig) / fs))
        params.preprocessing = False

    L = len(sig)
    L2 = np.int(np.ceil(L / 2))

    params.time = time

    # Random permutation surrogates.
    if method == _RP:
        for k in range(N):
            surr[k, :] = sig[randperm(L)]

    # Fourier transform surrogates.
    elif method == _FT:
        b = 2 * np.pi

        # Note: removed 'eta' parameter from function.
        eta = b * np.random.rand(N, L2 - 1)

        ftsig = np.fft.fft(sig, axis=0)
        ftrp = np.zeros((N, len(ftsig)), dtype=np.complex64)
        ftrp[:, 0] = ftsig[0]

        F = ftsig[1:L2]
        F = np.tile(F, (N, 1))

        ftrp[:, 1:L2] = F * np.exp(1j * eta)
        ftrp[:, 1 + L - L2 : L] = np.conj(np.fliplr(ftrp[:, 1:L2]))

        surr = np.fft.ifft(ftrp, axis=0)
        surr = np.real(surr)

        params.rphases = eta

    # Amplitude-adjusted Fourier transform surrogates.
    elif method == _AAFT:
        b = 2 * np.pi
        eta = b * np.random.rand(N, L2 - 1)

        val = np.sort(sig)
        ind = np.argsort(sig)
        rankind = np.empty(ind.shape, dtype=np.int)
        rankind[ind] = np.arange(0, L)

        gn = np.sort(np.random.randn(N, len(sig)), 1)
        for j in range(N):
            gn[j, :] = gn[j, rankind]

        ftgn = np.fft.fft(gn, axis=0)
        F = ftgn[:, 1:L2]

        surr = np.zeros((N, len(sig)), dtype=np.complex)
        surr[:, 0] = gn[:, 0]
        surr[:, 1:L2] = np.multiply(F, np.exp(np.complex(0, 1) * eta))
        surr[:, 1 + L - L2 : L] = np.conj(np.fliplr(surr[:, 1:L2]))
        surr = np.fft.ifft(surr, axis=0)

        ind2 = np.argsort(surr, axis=1)
        rrank = np.zeros((1, L), dtype=np.int)
        for k in range(N):
            rrank[:, ind2[k, :]] = np.arange(0, L)
            surr[k, :] = val[rrank]

        surr = np.real(surr)

    # Iterated amplitude-adjusted Fourier transform with exact distribution.
    elif method == _IAFFT1:
        maxit = 1000
        val = np.sort(sig)
        ind = np.argsort(sig)

        rankind = np.empty(ind.shape, dtype=np.int)
        rankind[ind] = np.arange(0, L)

        ftsig = np.fft.fft(sig, axis=0)
        F = np.tile(ftsig, (N, 1))
        surr = np.zeros((N, L))

        for j in range(N):
            surr[j, :] = sig[randperm(L)]

        it = 1
        irank = rankind.copy()
        irank = np.tile(irank, (N, 1))
        irank2 = np.zeros((1, L))
        oldrank = np.zeros((N, L))
        iind = np.zeros((N, L))
        iterf = iind.copy()

        while np.max(np.abs(oldrank - irank), axis=1) != 0 and it < maxit:
            go = np.max(np.abs(oldrank - irank), axis=1)
            go_c = go.conj().T

            inc = go_c[go_c != 0].nonzero()

            oldrank = irank.copy()
            iterf[inc, :] = np.real(np.fft.ifft(np.abs(F[inc, :]), axis=0)) * np.exp(
                1j * np.angle(np.fft.fft(surr[inc, :], axis=1))
            )

            iind[inc, :] = np.sort(iterf[inc, :], axis=1)
            for k in range(inc):
                irank2[iind[k, :]] = np.arange(0, L)
                irank[k, :] = irank2.copy()
                surr[k, :] = val[irank2]

            it += 1

    # Iterated amplitude-adjusted Fourier transform with exact spectrum.
    elif method == _IAFFT2:  # Note: needs testing.
        maxit = 1000

        val = np.sort(sig)
        ind = np.argsort(sig)

        rankind = np.empty(L, dtype=np.int64)
        rankind[ind] = np.arange(0, L)

        ftsig = np.fft.fft(sig, axis=0)
        F = ftsig[np.ones((1, N)), :]
        surr = np.zeros((N, L))

        for j in range(N):
            surr[j, :] = sig[randperm(L)]

        it = 1
        irank = rankind.copy()
        irank = irank[np.ones((1, N)), :]
        irank2 = np.zeros((N, L))
        oldrank = np.zeros((N, L))
        iind = np.zeros((N, L))
        iterf = np.zeros((N, L))

        while np.max(np.abs(oldrank - irank)) != 0 and it < maxit:
            go = np.max(np.abs(oldrank - irank))
            inc = (go.T != 0).nonzero()[0]

            oldrank = irank.copy()
            iterf[inc, :] = np.real(
                np.fft.ifft(
                    np.abs(F[inc, :])
                    * np.exp(1j * np.angle(np.fft.fft(surr[inc, :], axis=1))),
                    axis=1,
                )
            )

            iind[inc, :] = np.argsort(iterf[inc, :], axis=1)

            k = inc
            irank2[iind[k, :]] = np.arange(0, L)
            irank[k, :] = irank2.copy()
            surr[k, :] = val[irank2]

            it += 1

        surr = iterf

    # Wavelet iterated amplitude adjusted Fourier transform surrogates
    elif method == _WIAFFT:
        pass

    # Time-shifted surrogates.
    elif method == _tshift:
        for sn in range(N):
            startp = random.randint(1, L - 1)
            surr[sn, :] = np.hstack([sig[startp:L], sig[:startp]])

    # Cycle phase permutation surrogates.
    elif method == _CPP:
        signal = np.mod(sig, 2 * np.pi)

        dcpoints = ((signal[1:] - signal[:-1]) < -np.pi).nonzero()
        dcpoints = dcpoints[0]

        NC = len(dcpoints) - 1
        if NC > 0:
            cycles = []

            for k in range(NC):
                cycles.append(signal[dcpoints[k] : dcpoints[k + 1]])

            stcycle = signal[: dcpoints[0]]
            endcycle = signal[dcpoints[NC] :]

            rand_cycles = []
            for i in randperm(NC):
                rand_cycles.append(cycles[i])

            for sn in range(N):
                surr[sn, :] = np.unwrap(
                    np.concatenate((stcycle, *rand_cycles, endcycle))
                )
        else:
            for sn in range(N):
                surr[sn, :] = np.unwrap(signal)

    params.type = method
    params.numsurr = N

    if pp:
        params.preprocessing = True
        params.cutsig = sig
        params.sigstart = ks
        params.sigend = ke
    else:
        params.preprocessing = False

    params.time = time
    params.fs = fs

    if return_params:
        return surr, params

    return surr


def surr_preprocessing(
    sig: ndarray, fs: float
) -> Tuple[ndarray, ndarray, ndarray, float]:
    sig -= np.mean(sig)
    t = np.linspace(0, len(sig), int(len(sig) // fs))
    L = len(sig)

    # Find pair of points which minimises mismatch between p consecutive points and the beginning and end of the signal
    p = 10

    K1 = np.round(L / 100)  # Proportion of signal to consider at beginning.
    k1 = sig[:K1]
    K2 = np.round(L / 10)  # Proportion of signal to consider at end.
    k2 = sig[-K2:]

    # Truncate to match start and end points and first derivatives.
    if len(k1) <= p:
        p = len(k1) - 1

    d = np.zeros((len(k1) - p, len(k2) - p))

    for j in range(len(k1) - p):
        for k in range(len(k2) - p):
            d[j, k] = np.sum(np.abs(k1[j : j + p]) - k2[k : k + p])

    abs_d = np.abs(d)
    v = np.min(abs_d, axis=1)
    I = np.argmin(abs_d, axis=1)
    I2 = np.argmin(v)  # Minimum mismatch.

    kstart = I2
    kend = I[I2] + len(sig[:-k2])
    cutsig = sig[kstart:kend]  # New truncated time series.
    t2 = t[kstart:kend]  # Corresponding time.

    return cutsig, t2, kstart, kend


class Params:
    def __init__(self):
        self.origsig = None
        self.numsurr = None
        self.fs = None
        self.method = None
