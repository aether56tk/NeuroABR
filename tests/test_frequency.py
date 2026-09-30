from neuroabr.frequency import FrequencyLevel, estimate_frequency_threshold, estimate_session_thresholds


def test_frequency_threshold():
    levels = [
        FrequencyLevel(2000, 60, True, 0.9),
        FrequencyLevel(2000, 40, True, 0.9),
        FrequencyLevel(2000, 30, False, 0.2),
        FrequencyLevel(2000, 20, False, 0.1),
    ]
    result = estimate_frequency_threshold(levels)
    assert result.threshold_db_nhl == 40
    assert result.status == "estimated"


def test_session_groups_by_frequency():
    levels = [
        FrequencyLevel(500, 40, True),
        FrequencyLevel(500, 30, False),
        FrequencyLevel(2000, 50, True),
        FrequencyLevel(2000, 40, True),
    ]
    results = estimate_session_thresholds(levels)
    assert [x.frequency_hz for x in results] == [500, 2000]
