#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020 Takenori Yoshimura
# Licensed under the MIT license

import numpy as np

from scipy import signal


def get_sptk_window(window, Nx):
    """Return a SPTK-like window of a given length and type.

    Parameters
    ----------
    window : string, float, or tuple
        Type of window to create.

    Nx : int > 0 [scalar]
        The number of samples in the window.

    Returns
    -------
    get_window : np.ndarray [shape=(Nx,)]
        SPTK-like window.

    """

    if Nx <= 0:
        raise ValueError('Window length Nx must be a positive integer')

    w = signal.get_window(window, Nx, fftbins=False)
    z = np.reciprocal(np.sqrt(np.dot(w, w)))
    return w * z
