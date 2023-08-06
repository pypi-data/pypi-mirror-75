"""Main module."""

import numpy as np


TIME_AX = 0
SPACE_AX = -1


def wnfreq(arr, time_ax=TIME_AX, space_ax=SPACE_AX):
    """Compute wavenumber-frequency spectrum of arr.
    
    Args:
        arr (np.ndarray): input data.
        time_ax (int, optional): axis of time dimension. Defaults to first.
        space_ax (int, optional): axis of spatial dimension. Defaults to last.

    Returns:
        np.ndarray: wavenumber-frequency spectrum.
    """
    wnfreq = np.fft.rfft2(arr, axes=(time_ax, space_ax))
    return np.fft.fftshift(wnfreq, axes=time_ax)


def invert_wnfreq(wnfreq, shape=None, time_ax=TIME_AX, space_ax=SPACE_AX):
    """Invert wavenumber-frequency spectrum.
    
    Args:
        wnfreq (np.ndarray): wavenumber-frequency spectrum.
        shape (tuple, optional): desired shape of output. See documentation of np.irfft
        function for details. Defaults to None.
        time_ax (int, optional): axis of time dimension. Defaults to first.
        space_ax (int, optional): axis of spatial dimension. Defaults to last.

    Returns:
        np.ndarray: inverted spectrum.
    """
    unshifted_wnfreq = np.fft.ifftshift(wnfreq, axes=time_ax)
    return np.fft.irfft2(unshifted_wnfreq, s=shape, axes=(time_ax, space_ax))


def decompose(wnfreq, time_ax=TIME_AX):
    """Decompose wavenumber-frequency spectrum into standing and traveling parts.
    
    Args:
        wnfreq (np.ndarray): wavenumber-frequency spectrum
        time_ax (int, optional): axis of time dimension. Defaults to first.
        
    Returns:
        (np.ndarray, np.ndarray): tuple of standing and traveling components of
        wavenumber-frequency spectrum.
    """
    magnitude = np.abs(wnfreq)
    phase = np.angle(wnfreq)
    standing_magnitude = np.minimum(magnitude, np.flip(magnitude, axis=time_ax))
    traveling_magnitude = magnitude - standing_magnitude
    wnfreq_standing = standing_magnitude * (np.cos(phase) + 1j * np.sin(phase))
    wnfreq_traveling = traveling_magnitude * (np.cos(phase) + 1j * np.sin(phase))
    return wnfreq_standing, wnfreq_traveling
