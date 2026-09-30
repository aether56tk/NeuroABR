import numpy as np

from neuroabr.presto import level_evidence, fit_threshold


def test_resampled_detector_detects_repeatable_signal():
    rng = np.random.default_rng(2)
    t = np.linspace(0, 1, 250)
    signal = np.exp(-((t - 0.35) / 0.03) ** 2)
    trials = signal + 0.05 * rng.normal(size=(40, t.size))
    evidence = level_evidence(trials, 50, n_resamples=50)
    assert evidence.mean_correlation > 0.5
    assert evidence.response_present


def test_threshold_fit_returns_response_level():
    rng = np.random.default_rng(3)
    levels = []
    t = np.linspace(0, 1, 250)
    signal = np.exp(-((t - 0.35) / 0.03) ** 2)
    for intensity, noise in [(20, 0.30), (30, 0.20), (40, 0.08), (50, 0.04)]:
        trials = signal + noise * rng.normal(size=(32, t.size))
        levels.append(level_evidence(trials, intensity, n_resamples=30))
    fit = fit_threshold(levels)
    assert fit.threshold_db_nhl is not None
    assert 20 <= fit.threshold_db_nhl <= 50
