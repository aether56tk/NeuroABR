from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from scipy.optimize import curve_fit


@dataclass(frozen=True)
class LevelEvidence:
    intensity_db_nhl: float
    mean_correlation: float
    correlation_sd: float
    n_resamples: int
    response_probability: float
    response_present: bool


@dataclass(frozen=True)
class ThresholdFit:
    threshold_db_nhl: float | None
    criterion: float
    model: str
    fit_error: float | None
    status: str


def _normalised_xcorr(a: np.ndarray, b: np.ndarray) -> float:
    a, b = np.asarray(a, float), np.asarray(b, float)
    if a.shape != b.shape or a.size < 3:
        raise ValueError("Waveforms must have the same length.")
    a, b = a - a.mean(), b - b.mean()
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / denom) if denom else 0.0


def resampled_split_half_correlation(trials, *, n_resamples=200, seed=0):
    """Independent split-half median reproducibility detector."""
    x = np.asarray(trials, float)
    if x.ndim != 2 or x.shape[0] < 4:
        raise ValueError("trials must have shape (n_trials, n_samples), with >=4 trials.")
    rng = np.random.default_rng(seed)
    half = x.shape[0] // 2
    values = []
    for _ in range(int(n_resamples)):
        order = rng.permutation(x.shape[0])
        values.append(_normalised_xcorr(
            np.median(x[order[:half]], axis=0),
            np.median(x[order[-half:]], axis=0),
        ))
    return np.asarray(values)


def level_evidence(trials, intensity_db_nhl, *, n_resamples=200, criterion=0.30, seed=0):
    values = resampled_split_half_correlation(trials, n_resamples=n_resamples, seed=seed)
    mean_corr = float(values.mean())
    return LevelEvidence(
        float(intensity_db_nhl), mean_corr,
        float(values.std(ddof=1)) if values.size > 1 else 0.0,
        int(values.size),
        float(np.clip((mean_corr + 1.0) / 2.0, 0.0, 1.0)),
        bool(mean_corr >= criterion),
    )


def _sigmoid(x, low, high, midpoint, slope):
    return low + (high-low) / (1.0 + np.exp(-(x-midpoint)/np.maximum(slope, 1e-6)))


def _power(x, low, scale, exponent):
    return low + scale * np.power(np.maximum(x, 1e-6), exponent)


def _fit_candidate(model, x, y, p0, bounds, criterion):
    params, _ = curve_fit(model, x, y, p0=p0, bounds=bounds, maxfev=30000)
    predicted = model(x, *params)
    error = float(np.mean((predicted-y)**2))
    grid = np.linspace(float(x.min()), float(x.max()), 4000)
    values = model(grid, *params)
    lo, hi = float(values.min()), float(values.max())
    if hi <= lo:
        raise RuntimeError("Non-monotonic response fit.")
    target = lo + criterion*(hi-lo)
    threshold = float(grid[np.argmin(np.abs(values-target))])
    return threshold, error


def fit_threshold(evidence: list[LevelEvidence], *, criterion=0.30):
    """Compare sigmoid and power-law fits; choose the lower-MSE model."""
    if not evidence:
        return ThresholdFit(None, criterion, "none", None, "no_data")

    ordered = sorted(evidence, key=lambda e: e.intensity_db_nhl)
    x = np.asarray([e.intensity_db_nhl for e in ordered], float)
    y = np.asarray([e.mean_correlation for e in ordered], float)

    if len(x) < 3 or np.ptp(y) < 1e-6:
        positives = [e.intensity_db_nhl for e in ordered if e.mean_correlation >= criterion]
        return ThresholdFit(min(positives) if positives else None, criterion, "discrete", None, "discrete_fallback")

    candidates = []
    try:
        candidates.append(("sigmoid", *_fit_candidate(
            _sigmoid, x, y,
            [float(y.min()), float(y.max()), float(np.median(x)), 10.0],
            ([-1, -1, float(x.min()-100), 0.5], [1, 1, float(x.max()+100), 100]),
            criterion,
        )))
    except Exception:
        pass
    try:
        candidates.append(("power_law", *_fit_candidate(
            _power, x, y,
            [float(y.min()), max(float(y.max()-y.min()), 1e-3), 1.0],
            ([-1, -10, 0.05], [1, 10, 5]),
            criterion,
        )))
    except Exception:
        pass

    if candidates:
        model, threshold, error = min(candidates, key=lambda z: z[2])
        return ThresholdFit(float(threshold), criterion, model, float(error), "estimated")

    positives = [e.intensity_db_nhl for e in ordered if e.mean_correlation >= criterion]
    return ThresholdFit(min(positives) if positives else None, criterion, "discrete", None, "discrete_fallback")
