from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class FrequencyThreshold:
    frequency_hz: float
    threshold_db_ehl: float


def pure_tone_average(
    thresholds: Iterable[FrequencyThreshold],
    frequencies_hz: tuple[float, ...] = (500.0, 1000.0, 2000.0),
) -> float | None:
    """Calculate PTA from frequency-specific dB eHL/HL thresholds.

    This function deliberately does not convert a single ABR waveform into PTA.
    PTA requires frequency-specific behavioral or appropriately corrected
    electrophysiologic thresholds.
    """
    wanted = set(frequencies_hz)
    values = [
        float(x.threshold_db_ehl)
        for x in thresholds
        if float(x.frequency_hz) in wanted
    ]
    if len(values) != len(wanted):
        return None
    return sum(values) / len(values)


def estimate_pta_from_frequency_thresholds(
    thresholds: Iterable[FrequencyThreshold],
) -> dict:
    items = list(thresholds)
    pta = pure_tone_average(items)
    return {
        "pta_db": pta,
        "method": "3-frequency average (500, 1000, 2000 Hz)",
        "status": "estimated" if pta is not None else "insufficient_frequency_data",
        "clinical_note": (
            "PTA is not derived from a single ABR waveform. "
            "Frequency-specific thresholds and appropriate correction are required."
        ),
    }
