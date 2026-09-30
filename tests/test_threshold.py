from neuroabr.threshold import LevelResult, estimate_threshold


def test_estimate_lowest_present_level():
    levels = [
        LevelResult(80, True),
        LevelResult(60, True),
        LevelResult(40, True),
        LevelResult(30, False),
        LevelResult(20, False),
    ]
    assert estimate_threshold(levels) == 40


def test_no_response():
    levels = [LevelResult(40, False), LevelResult(20, False)]
    assert estimate_threshold(levels) is None
