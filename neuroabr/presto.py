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
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape != b.shape or a.size < 3:
        raise ValueError("Waveforms must have the same length.")
    a = a - np.mean(a)
    b = b - np.mean(b)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def resampled_split_half_correlation(
    trials: np.ndarray,
    *,
    n_resamples: int = 200,
    seed: int = 0,
) -> np.ndarray:
    """Estimate response reproducibility from independent split-half medians.

    This follows the published ABRpresto idea of repeatedly partitioning
    single-trial responses into two independent groups and correlating their
    representative waveforms, but is implemented independently for NeuroABR.
    """
    x = np.asarray(trials, dtype=float)
    if x.ndim != 2:
        raise ValueError("trials must have shape (n_trials, n_samples).")
    n_trials = x.shape[0]
    if n_trials < 4:
        raise ValueError("At least four trials are required.")
    rng = np.random.default_rng(seed)
    correlations: list[float] = []

    for _ in range(int(n_resamples)):
        order = rng.permutation(n_trials)
        half = n_trials // 2
        a = np.median(x[order[:half]], axis=0)
        b = np.median(x[order[-half:]], axis=0)
        correlations.append(_normalised_xcorr(a, b))

    return np.asarray(correlations, dtype=float)


def level_evidence(
    trials: np.ndarray,
    intensity_db_nhl: float,
    *,
    n_resamples: int = 200,
    criterion: float = 0.30,
    seed: int = 0,
) -> LevelEvidence:
    """Compute reproducibility evidence for one stimulus level."""
    values = resampled_split_half_correlation(
        trials, n_resamples=n_resamples, seed=seed
    )
    # Convert the correlation distribution to a bounded evidence score.
    mean_corr = float(np.mean(values))
    probability = float(np.clip((mean_corr + 1.0) / 2.0, 0.0, 1.0))
    return LevelEvidence(
        intensity_db_nhl=float(intensity_db_nhl),
        mean_correlation=mean_corr,
        correlation_sd=float(np.std(values, ddof=1)) if values.size > 1 else 0.0,
        n_resamples=int(values.size),
        response_probability=probability,
        response_present=bool(mean_corr >= criterion),
    )


def _logistic(level: np.ndarray, low: float, high: float, midpoint: float, slope: float) -> np.ndarray:
    return low + (high - low) / (1.0 + np.exp(-(level - midpoint) / np.maximum(slope, 1e-6)))


def fit_threshold(
    evidence: list[LevelEvidence],
    *,
    criterion: float = 0.30,
) -> ThresholdFit:
    """Fit a monotonic logistic response curve and return its criterion crossing.

    The fitted curve is a research aid; if fitting is unstable, the caller
    should fall back to the discrete lowest reproducible response.
    """
    if not evidence:
        return ThresholdFit(None, criterion, "logistic", None, "no_data")

    ordered = sorted(evidence, key=lambda x: x.intensity_db_nhl)
    x = np.asarray([e.intensity_db_nhl for e in ordered], dtype=float)
    y = np.asarray([e.mean_correlation for e in ordered], dtype=float)

    if len(x) < 3 or np.ptp(y) < 1e-6:
        positives = [e.intensity_db_nhl for e in ordered if e.mean_correlation >= criterion]
        return ThresholdFit(
            min(positives) if positives else None,
            criterion, "discrete", None,
            "discrete_fallback",
        )

    p0 = [float(np.min(y)), float(np.max(y)), float(np.median(x)), 10.0]
    try:
        params, _ = curve_fit(
            _logistic, x, y, p0=p0, maxfev=20000,
            bounds=([-1.0, -1.0, np.min(x)-100.0, 0.5],
                    [1.0, 1.0, np.max(x)+100.0, 100.0]),
        )
        low, high, midpoint, slope = params
        if high <= low:
            raise RuntimeError("Non-monotonic fit.")
        target = low + criterion * (high - low)
        if not (low <= target <= high):
            raise RuntimeError("Criterion outside fitted range.")
        threshold = float(midpoint + slope * np.log((target - low) / (high - target)))
        pred = _logistic(x, *params)
        error = float(np.mean((pred - y) ** 2))
        return ThresholdFit(threshold, criterion, "logistic", error, "estimated")
    except Exception:
        positives = [e.intensity_db_nhl for e in ordered if e.mean_correlation >= criterion]
        return ThresholdFit(
            min(positives) if positives else None,
            criterion, "discrete", None,
            "discrete_fallback",
        )
