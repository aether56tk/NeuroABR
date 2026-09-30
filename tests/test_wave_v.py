import numpy as np

from neuroabr.wave_v import detect_wave_v


def test_wave_v_candidate():
    t = np.linspace(0, 12, 1201)
    x = np.exp(-0.5 * ((t - 6.2) / 0.15) ** 2)
    candidate = detect_wave_v(t, x)
    assert candidate is not None
    assert 6.0 < candidate.latency_ms < 6.4
