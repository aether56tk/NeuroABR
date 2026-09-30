from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LevelDecision:
    intensity_db_nhl: float
    response_present: bool
    confidence: float = 0.0


def estimate_abr_threshold(
    decisions: list[LevelDecision],
    require_adjacent_confirmation: bool = True,
) -> float | None:
    """Estimate the lowest tested dB nHL with a detectable ABR response.

    With adjacent confirmation enabled, a lone isolated positive level is not
    accepted as a threshold. This is intentionally conservative for the
    research prototype.
    """
    ordered = sorted(decisions, key=lambda x: x.intensity_db_nhl)
    present = [x for x in ordered if x.response_present]

    if not present:
        return None

    if not require_adjacent_confirmation:
        return present[0].intensity_db_nhl

    # Require the lowest positive level to have at least one positive level
    # immediately above it in the tested sequence.
    for i, item in enumerate(ordered):
        if not item.response_present:
            continue
        if i + 1 < len(ordered) and ordered[i + 1].response_present:
            return item.intensity_db_nhl

    return None
