from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LevelResult:
    intensity_db_nhl: float
    response_present: bool


def estimate_threshold(levels: list[LevelResult] | tuple[LevelResult, ...]) -> float | None:
    """Return the lowest tested intensity with a detected response.

    This is a simple research prototype rule and should later be replaced/augmented
    with a validated sequential thresholding strategy.
    """
    present = [x.intensity_db_nhl for x in levels if x.response_present]
    return min(present) if present else None


def response_table(levels: list[LevelResult]) -> list[dict]:
    return [
        {
            "intensity_db_nhl": x.intensity_db_nhl,
            "response": "Present" if x.response_present else "Absent",
        }
        for x in sorted(levels, key=lambda v: v.intensity_db_nhl, reverse=True)
    ]
