#!/usr/bin/env python

"""Tests for `standing` package."""

import pytest


import numpy as np
import standing as st

from standing.core import TIME_AX


@pytest.mark.parametrize(
    "arr",
    [
        np.array([[0, 0]]),
        np.array([[0, 1]]),
        np.array([[0, 1, 2]]),
        np.array([[0, 1], [2, 3]]),
        np.array([[0, 1, 2], [2, 3, 4]]),
        np.array([[0, 1, 2], [2, 3, 4], [5, 6, 7]]),
        np.array([[0, 1], [2, 3], [4, 5]]),
    ],
)
def test_wnfreq_round_trip(arr):
    s = arr.shape
    np.testing.assert_allclose(st.invert_wnfreq(st.wnfreq(arr), shape=s), arr)


@pytest.mark.parametrize(
    "arr",
    [
        np.array([[0, 0]]),
        np.array([[0, 0, 0]]),
        np.array([[0, 1, 2]]),
        np.array([[0, 1], [2, 3]]),
        np.array([[0, 1, 2], [2, 3, 4]]),
        np.array([[0, 1, 2], [2, 3, 4], [5, 6, 7]]),
    ],
)
def test_decompose(arr):
    wnfreq_total = st.wnfreq(arr)
    wnfreq_standing, wnfreq_traveling = st.decompose(wnfreq_total)
    wnfreq_sum = wnfreq_standing + wnfreq_traveling
    np.testing.assert_allclose(wnfreq_sum, wnfreq_total)
    standing_abs = np.abs(wnfreq_standing)
    np.testing.assert_allclose(standing_abs, np.flip(standing_abs, TIME_AX))
