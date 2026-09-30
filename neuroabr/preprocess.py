from __future__ import annotations

import numpy as np
from scipy.signal import butter, filtfilt


def baseline_correct(signal: np.ndarray, baseline_samples: int) -> np.ndarray:
    """Subtract the mean of the baseline segment."""
    x = np.asarray(signal, dtype=float)
    if baseline_samples < 1 or baseline_samples > x.size:
        raise ValueError("baseline_samples must be between 1 and signal length.")
    return x - np.mean(x[:baseline_samples])


def bandpass_filter(
    signal: np.ndarray,
    fs_hz: float,
    low_hz: float = 100.0,
    high_hz: float = 3000.0,
    order: int = 4,
) -> np.ndarray:
    """Zero-phase Butterworth band-pass filter."""
    x = np.asarray(signal, dtype=float)
    if x.size < 16:
        raise ValueError("Signal is too short for stable filtering.")
    nyquist = fs_hz / 2.0
    if not (0 < low_hz < high_hz < nyquist):
        raise ValueError("Require 0 < low_hz < high_hz < Nyquist frequency.")
    b, a = butter(order, [low_hz / nyquist, high_hz / nyquist], btype="band")
    return filtfilt(b, a, x)


def preprocess(
    signal: np.ndarray,
    fs_hz: float,
    baseline_samples: int,
    low_hz: float = 100.0,
    high_hz: float = 3000.0,
) -> np.ndarray:
    corrected = baseline_correct(signal, baseline_samples)
    return bandpass_filter(corrected, fs_hz, low_hz, high_hz)
