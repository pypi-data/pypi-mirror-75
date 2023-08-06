#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020 Takenori Yoshimura
# Licensed under the MIT license

import numpy as np

from .utils import _asarray, check_alpha


def freqt(C, M=24, alpha=0.42, recursive=True):
    """Perform frequency transform.

    Parameters
    ----------
    C : array_like [shape=(m + 1,) or (m + 1, T)]
        Minimum phase sequence.

    M : int >= 0 [scalar]
        Order of warped sequence.

    alpha : float in (-1, 1) [scalar]
        Frequency warping factor.

    recursive : bool [scalar]
        If True, use recursive algorithm instead of matrix multiplication.

    Returns
    -------
    G : np.ndarray [shape=(M + 1), or (M + 1, T)]
        Frequency warped sequence.

    References
    ----------
    .. [1] A. V. Oppenheim and D. H. Johnson, "Discrete representation of
           signals," in Proceedings of the IEEE, vol. 60, no. 6, pp. 681-691,
           1972.

    """

    C = _asarray(C)
    if C.ndim == 1:
        is_vector_input = True
        C = np.expand_dims(C, axis=-1)
    elif C.ndim == 2:
        is_vector_input = False
    else:
        raise ValueError('Input C must be 2-D matrix or 1-D vector')

    m = C.shape[0] - 1
    if m < 0:
        raise ValueError('Order m must be a non-negative integer')

    if M < 0:
        raise ValueError('Order M must be a non-negative integer')

    check_alpha(alpha)
    beta = 1 - alpha * alpha

    if recursive:
        L = M + 1
        T = C.shape[1]
        D = np.zeros((L, T))
        G = np.zeros((L, T))
        for i in range(m, -1, -1):
            D[0] = G[0]
            G[0] = C[i] + alpha * D[0]
            if 1 < L:
                D[1] = G[1]
                G[1] = beta * D[0] + alpha * D[1]
            for j in range(2, L):
                D[j] = G[j]
                G[j] = D[j - 1] + alpha * (D[j] - G[j - 1])
    else:
        given_param = (m, M, alpha)
        if 'param' not in dir(freqt) or freqt.param != given_param:
            freqt.param = given_param
            update = True
        else:
            update = False

        if update:
            L = M + 1
            K = m + 1
            freqt.A = np.zeros((L, K))
            freqt.A[0, :] = alpha ** np.arange(K)
            if 1 < L and 1 < K:
                freqt.A[1, 1:] = (alpha ** np.arange(K - 1) * np.arange(1, K) *
                                  beta)
            for i in range(2, L):
                i1 = i - 1
                for j in range(1, K):
                    j1 = j - 1
                    freqt.A[i, j] = (freqt.A[i1, j1] +
                                     alpha * (freqt.A[i, j1] - freqt.A[i1, j]))
        G = np.matmul(freqt.A, C)

    if is_vector_input:
        G = np.squeeze(G, axis=-1)

    return G
