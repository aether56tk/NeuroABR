from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


STANDARD_FREQUENCIES_HZ = (250, 500, 1000, 2000, 4000, 8000)


@dataclass(frozen=True)
class FrequencyLevel:
    frequency_hz: float
    intensity_db_nhl: float
    response_present: bool
    confidence: float = 0.0
    wave_v_latency_ms: float | None = None


@dataclass(frozen=True)
class FrequencyThreshold:
    frequency_hz: float
    threshold_db_nhl: float | None
    threshold_db_ehl: float | None
    confidence: float
    method: str
    status: str


def estimate_frequency_threshold(
    levels: Iterable[FrequencyLevel],
    require_confirmation: bool = True,
) -> FrequencyThreshold:
    """Estimate the lowest detected response for one stimulus frequency.

    This operates on frequency-specific ABR recordings. It does not infer
    frequency thresholds from a broadband click waveform.
    """
    items = sorted(levels, key=lambda x: x.intensity_db_nhl)
    if not items:
        raise ValueError("At least one frequency level is required.")

    frequency = float(items[0].frequency_hz)
    if any(float(x.frequency_hz) != frequency for x in items):
        raise ValueError("All levels must have the same frequency.")

    positives = [x for x in items if x.response_present]
    if not positives:
        return FrequencyThreshold(
            frequency_hz=frequency,
            threshold_db_nhl=None,
            threshold_db_ehl=None,
            confidence=0.0,
            method="objective-response-search",
            status="no_detectable_response",
        )

    candidate = positives[0]

    if require_confirmation:
        idx = items.index(candidate)
        confirmed = (
            idx + 1 < len(items)
            and items[idx + 1].response_present
        )
        if not confirmed:
            return FrequencyThreshold(
                frequency_hz=frequency,
                threshold_db_nhl=candidate.intensity_db_nhl,
                threshold_db_ehl=None,
                confidence=max(0.0, candidate.confidence * 0.5),
                method="objective-response-search",
                status="provisional",
            )

    return FrequencyThreshold(
        frequency_hz=frequency,
        threshold_db_nhl=candidate.intensity_db_nhl,
        threshold_db_ehl=None,
        confidence=candidate.confidence,
        method="objective-response-search",
        status="estimated",
    )


def estimate_session_thresholds(
    levels: Iterable[FrequencyLevel],
) -> list[FrequencyThreshold]:
    groups: dict[float, list[FrequencyLevel]] = {}
    for level in levels:
        groups.setdefault(float(level.frequency_hz), []).append(level)

    return [
        estimate_frequency_threshold(groups[f])
        for f in sorted(groups)
    ]
