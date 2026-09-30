import pytest
from neuroabr.physionet import parse_earndb_average_name

def test_parse_earndb_average_name():
    meta = parse_earndb_average_name("N1_evoked_ave50_F1_R2")
    assert meta == {"subject": "N1", "frequency_khz": 1.0, "level_pespl": 50.0, "repetition": 2}

def test_parse_earndb_rejects_unknown_name():
    with pytest.raises(ValueError):
        parse_earndb_average_name("not_an_earndb_record")
