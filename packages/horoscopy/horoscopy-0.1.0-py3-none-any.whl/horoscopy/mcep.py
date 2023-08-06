#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020 Takenori Yoshimura
# Licensed under the MIT license

import sys

import numpy as np
from scipy.fft import rfft, irfft

from .freqt import freqt
from .math import solve_toeplitz_plus_hankel
from .utils import _asarray, check_alpha


def stft_to_mcep(S, M=24, alpha=0.42, n_iter=10, tol=1e-4, eps=0):
    """Calculate mel-cepstral coefficients from a magnitude spectrogram.

    Parameters
    ----------
    S : array-like [shape=(1 + n_fft / 2,) or (1 + n_fft / 2, T), non-negative]
        Input linear magnitude spectrogram.

    M : int >= 0 [scalar]
        Order of mel-cepstral coefficients.

    alpha : float in (-1, 1) [scalar]
        Frequency warping factor.

    n_iter : int >= 0 [scalar]
        Number of iterations of Newton-Raphson method.

    tol : float >= 0 [scalar]:
        Relative tolerance.

    eps : float >= 0 [scalar]
        A very small value added to periodogram to avoid NaN caused by log().

    Returns
    -------
    mc : np.ndarray [shape=(M + 1, T)]
        M-th order mel-cesptral coefficients.

    Notes
    -----
    This implementation is based on an unpublished paper.

    """

    # Perform coefficients frequency transform.
    def tilde(x, M, alpha):
        if 'A' not in dir(tilde):
            m = x.shape[0]
            tilde.A = np.zeros((M, m))
            tilde.A[0, 0] = 1
            if 1 < M:
                tilde.A[1:, 0] = (-alpha) ** np.arange(1, M)
            if 1 < M and 1 < m:
                tilde.A[1, 1:] = alpha ** np.arange(m - 1) * (1 - alpha * alpha)
            for i in range(2, M):
                i1 = i - 1
                for j in range(1, m):
                    j1 = j - 1
                    tilde.A[i, j] = (tilde.A[i1, j1] +
                                     alpha * (tilde.A[i, j1] - tilde.A[i1, j]))
        return np.matmul(tilde.A, x)

    S = _asarray(S)
    if S.ndim == 1:
        is_vector_input = True
        S = np.expand_dims(S, axis=-1)
    elif S.ndim == 2:
        is_vector_input = False
    else:
        raise ValueError('Input S must be 2-D matrix or 1-D vector')

    if S.shape[0] <= 1:
        raise ValueError('S.shape[0] must be greater than 1')

    if M < 0:
        raise ValueError('Order M must be a non-negative integer')

    if n_iter < 0:
        raise ValueError('Number of iterations must be a non-negative integer')

    if tol < 0:
        raise ValueError('Relative tolerance must be a non-negative number')

    if eps < 0:
        raise ValueError('Value eps must be a non-negative number')

    check_alpha(alpha)

    n_fft = 2 * (S.shape[0] - 1)
    h_fft = n_fft // 2
    L = M + 1

    # Compute (-a)^0, (-a)^1, (-a)^2, ..., (-a)^M.
    a = np.expand_dims((-alpha) ** np.arange(L), axis=-1)

    # Compute log periodogram.
    log_I = 2 * np.log(S + eps if eps > 0 else S)

    # Make initial guess.
    c = irfft(log_I, axis=0)[:h_fft + 1]
    c[(0, -1), :] *= 0.5
    mc = freqt(c, M=M, alpha=alpha, recursive=False)

    # Perform Newton-Raphson method.
    prev_epsilon = sys.float_info.max
    for n in range(n_iter):
        c = freqt(mc, M=h_fft, alpha=-alpha, recursive=False)
        log_D = rfft(c, n=n_fft, axis=0).real

        r = irfft(np.exp(log_I - 2 * log_D), axis=0)[:h_fft + 1]
        r_t = tilde(r, 2 * L - 1, alpha)
        r_a = r_t[:L] - a

        # Update mel-cepstral coefficients.
        t = (r_t[:L], r_t[:L])
        h = (r_t[M:], r_t[:L])
        b = r_a
        grad = solve_toeplitz_plus_hankel(t, h, b)
        mc += grad

        # Check convergence.
        epsilon = np.max(r_t[0])
        relative_change = (prev_epsilon - epsilon) / epsilon
        if relative_change < tol:
            break
        prev_epsilon = epsilon

    if is_vector_input:
        mc = np.squeeze(mc, axis=-1)

    return mc
