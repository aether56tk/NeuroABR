from neuroabr.clinical import FrequencyThreshold, pure_tone_average


def test_three_frequency_pta():
    data = [
        FrequencyThreshold(500, 30),
        FrequencyThreshold(1000, 40),
        FrequencyThreshold(2000, 50),
    ]
    assert pure_tone_average(data) == 40


def test_missing_frequency_returns_none():
    data = [
        FrequencyThreshold(500, 30),
        FrequencyThreshold(1000, 40),
    ]
    assert pure_tone_average(data) is None
