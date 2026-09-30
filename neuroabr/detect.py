from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.stats import pearsonr


@dataclass(frozen=True)
class ResponseMetrics:
    correlation: float
    snr_db: float
    present: bool


def rms(x: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    return float(np.sqrt(np.mean(np.square(x))))


def cross_correlation_score(a: np.ndarray, b: np.ndarray) -> float:
    """Pearson correlation used as a simple reproducibility measure."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape != b.shape or a.size < 3:
        raise ValueError("Signals must have the same shape and at least 3 samples.")
    result = pearsonr(a, b)
    return float(result.statistic)


def snr_db(signal: np.ndarray, noise: np.ndarray, eps: float = 1e-12) -> float:
    """RMS-based SNR in dB."""
    return float(20.0 * np.log10((rms(signal) + eps) / (rms(noise) + eps)))


def classify_response(
    correlation: float,
    snr: float,
    correlation_threshold: float = 0.45,
    snr_threshold_db: float = 3.0,
) -> bool:
    return correlation >= correlation_threshold and snr >= snr_threshold_db


def compare_subaverages(
    subaverage_a: np.ndarray,
    subaverage_b: np.ndarray,
    noise_reference: np.ndarray,
    correlation_threshold: float = 0.45,
    snr_threshold_db: float = 3.0,
) -> ResponseMetrics:
    corr = cross_correlation_score(subaverage_a, subaverage_b)
    mean_signal = (np.asarray(subaverage_a) + np.asarray(subaverage_b)) / 2.0
    snr = snr_db(mean_signal, noise_reference)
    present = classify_response(corr, snr, correlation_threshold, snr_threshold_db)
    return ResponseMetrics(correlation=corr, snr_db=snr, present=present)
