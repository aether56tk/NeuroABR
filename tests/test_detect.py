import numpy as np

from neuroabr.detect import cross_correlation_score, snr_db, classify_response


def test_cross_correlation_identical_signals():
    x = np.array([1.0, 2.0, 3.0, 2.0, 1.0])
    assert cross_correlation_score(x, x) > 0.99


def test_snr_is_positive_for_clean_signal():
    signal = np.ones(100)
    noise = np.full(100, 0.1)
    assert snr_db(signal, noise) > 15


def test_response_classifier():
    assert classify_response(0.8, 8.0)
    assert not classify_response(0.2, 8.0)
