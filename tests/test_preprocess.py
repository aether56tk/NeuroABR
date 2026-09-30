import numpy as np

from neuroabr.preprocess import baseline_correct


def test_baseline_correct_removes_offset():
    x = np.array([2.0, 2.0, 3.0, 4.0])
    y = baseline_correct(x, baseline_samples=2)
    np.testing.assert_allclose(y, [0.0, 0.0, 1.0, 2.0])
