#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020 Takenori Yoshimura
# Licensed under the MIT license

import numpy as np

from .utils import _asarray


def solve_toeplitz_plus_hankel(t, h, b):
    """Solve a Toeplitz plus Hankel system.

    Parameters
    ----------
    t : (array_like, array_like)
        First column(s) and first row(s) of the Toeplitz matrix.

    h : (array-like, array_like)
        First column(s) and last row(s) of the Hankel matrix.

    b : array-like [shape=(N,) or (N, K)]
        Constant vector(s). Right-hand side in ``(T + H) x = b``.

    Returns
    -------
    a : np.ndarray [shape=(N,) or (N, K)]
        Solution of the Toeplitz plus Hankel system.

    References
    ----------
    .. [1] G. Merchant and T. Parks, "Efficient solution of a
           Toeplitz-plus-Hankel coefficient matrix system of equations,"
           IEEE Transactions on Acoustics, Speech, and Signal Processing,
           vol. 30, no. 1, pp. 40--44, 1982.

    """

    # Perform 2-D matrix-vector multiplication, dot-product.
    def mv2d(m, v):
        ret = np.zeros(v.shape)
        ret[:, 0] = m[:, 0, 0] * v[:, 0] + m[:, 0, 1] * v[:, 1]
        ret[:, 1] = m[:, 1, 0] * v[:, 0] + m[:, 1, 1] * v[:, 1]
        return ret

    # Perform 2-D matrix-matrix mulciplication.
    def mm2d(m, n):
        ret = np.zeros(m.shape)
        ret[:, 0, 0] = m[:, 0, 0] * n[:, 0, 0] + m[:, 0, 1] * n[:, 1, 0]
        ret[:, 0, 1] = m[:, 0, 0] * n[:, 0, 1] + m[:, 0, 1] * n[:, 1, 1]
        ret[:, 1, 0] = m[:, 1, 0] * n[:, 0, 0] + m[:, 1, 1] * n[:, 1, 0]
        ret[:, 1, 1] = m[:, 1, 0] * n[:, 0, 1] + m[:, 1, 1] * n[:, 1, 1]
        return ret

    # Perform 2-D matrix inversion.
    def inv2d(x):
        y = np.zeros(x.shape)
        y[:, 0, 0] = x[:, 1, 1]
        y[:, 0, 1] = -x[:, 0, 1]
        y[:, 1, 0] = -x[:, 1, 0]
        y[:, 1, 1] = x[:, 0, 0]
        y *= np.reshape(np.reciprocal(
            x[:, 0, 0] * x[:, 1, 1] - x[:, 0, 1] * x[:, 1, 0]), (-1, 1, 1))
        return y

    # Perform 2-D cross transpose.
    def ct2d(x):
        y = np.zeros(x.shape)
        y[:, 0, 0] = x[:, 1, 1]
        y[:, 0, 1] = x[:, 1, 0]
        y[:, 1, 0] = x[:, 0, 1]
        y[:, 1, 1] = x[:, 0, 0]
        return y

    b = _asarray(b)
    if b.ndim == 1:
        is_vector_input = True
        b = np.expand_dims(b, axis=-1)
    elif b.ndim == 2:
        is_vector_input = False
    else:
        raise ValueError('Input b must be 2-D matrix or 1-D vector')
    N, K = b.shape

    if not isinstance(t, tuple) and len(t) != 2:
        raise ValueError('Input t must be a tuple of size 2')
    t_c, t_r = t
    t_c = _asarray(t_c)
    t_r = _asarray(t_r)
    if ((is_vector_input and (t_c.ndim != 1 or t_r.ndim != 1)) or
        (not is_vector_input and (t_c.ndim != 2 or t_r.ndim != 2))):
        raise ValueError('Dimension mismatch t vs b')

    if not isinstance(h, tuple) and len(h) != 2:
        raise ValueError('Input h must be a tuple of size 2')
    h_c, h_r = h
    h_c = _asarray(h_c)
    h_r = _asarray(h_r)
    if ((is_vector_input and (h_c.ndim != 1 or h_r.ndim != 1)) or
        (not is_vector_input and (h_c.ndim != 2 or h_r.ndim != 2))):
        raise ValueError('Dimension mismatch h vs b')

    # Step 1:
    if 1:
        # Set R.
        R = np.zeros((N, K, 2, 2))
        R[:, :, 0, 0] = t_c
        R[:, :, 1, 1] = t_r
        R[:, :, 0, 1] = h_c
        R[:, :, 1, 0] = h_r[::-1]

        # Apply coefficients modification.
        s = 1 if N % 2 == 0 else 0
        d0 = t_c[0]
        R[::2, :, 0, 0] += d0
        R[::2, :, 1, 1] += d0
        R[s::2, :, 0, 1] -= d0
        R[s::2, :, 1, 0] -= d0

        # Set X_0.
        X = np.zeros((N, K, 2, 2))
        X[0, :, 0, 0] = 1
        X[0, :, 1, 1] = 1
        prev_X = np.zeros((N, K, 2, 2))

        # Set p_0.
        b_bar = np.zeros((K, 2))
        b_bar[:, 0] = b[0]
        b_bar[:, 1] = b[N - 1]
        p = np.zeros((N, K, 2))
        p[0] = mv2d(inv2d(R[0]), b_bar)

        # Set V_x.
        V_x = np.copy(R[0])

    # Step 2:
    for i in range(1, N):
        # a: Calculate E_x.
        E_x = np.zeros((K, 2, 2))
        for j in range(i):
            E_x += mm2d(R[i - j], X[j])

        # b: Calculate e_p.
        e_p = np.zeros((K, 2))
        for j in range(i):
            e_p += mv2d(R[i - j], p[j])

        # c: Calculate B_x.
        B_x = mm2d(inv2d(ct2d(V_x)), E_x)

        # d: Update X and V_x.
        for j in range(1, i):
            X[j] -= mm2d(ct2d(prev_X[i - j]), B_x)
        X[i] = -B_x
        prev_X[1:i + 1] = X[1:i + 1]
        V_x -= mm2d(ct2d(E_x), B_x)

        # e: Calculate g.
        b_bar[:, 0] = b[i]
        b_bar[:, 1] = b[N - 1 - i]
        g = mv2d(inv2d(ct2d(V_x)), b_bar - e_p)

        # f: Update p.
        for j in range(i):
            p[j] += mv2d(ct2d(X[i - j]), g)
        p[i] = g

    # Step 3:
    if 1:
        # Extract solution vector.
        a = p[:, :, 0]
        if is_vector_input:
            a = np.squeeze(a, axis=-1)

    return a
