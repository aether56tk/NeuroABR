import numpy as np

from neuroabr.objective import objective_response_score


def test_objective_detector_detects_reproducible_signal():
    rng = np.random.default_rng(7)
    signal = np.sin(np.linspace(0, 8, 300))
    a = signal + rng.normal(0, 0.05, 300)
    b = signal + rng.normal(0, 0.05, 300)
    noise = rng.normal(0, 0.03, 300)

    result = objective_response_score(a, b, noise)
    assert result.correlation > 0.9
    assert result.present


def test_objective_detector_rejects_unrelated_noise():
    rng = np.random.default_rng(7)
    a = rng.normal(0, 1, 300)
    b = rng.normal(0, 1, 300)
    noise = rng.normal(0, 0.1, 300)

    result = objective_response_score(a, b, noise)
    assert not result.present
