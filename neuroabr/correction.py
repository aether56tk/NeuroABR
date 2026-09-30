from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CorrectionFactor:
    frequency_hz: float
    correction_db: float


class CorrectionTable:
    """Explicit frequency-specific nHL -> eHL correction table.

    No universal correction values are hard-coded. A validated table must be
    supplied for the stimulus, transducer and population being studied.
    """

    def __init__(self, factors: list[CorrectionFactor]):
        self._factors = {float(x.frequency_hz): float(x.correction_db) for x in factors}

    def convert(self, frequency_hz: float, threshold_db_nhl: float) -> float:
        if frequency_hz not in self._factors:
            raise KeyError(
                f"No validated correction for {frequency_hz:g} Hz. "
                "Supply a stimulus/transducer-specific correction table."
            )
        return float(threshold_db_nhl + self._factors[frequency_hz])

    def convert_thresholds(self, thresholds):
        return [
            type(x)(
                frequency_hz=x.frequency_hz,
                threshold_db_nhl=x.threshold_db_nhl,
                threshold_db_ehl=(
                    None if x.threshold_db_nhl is None
                    else self.convert(x.frequency_hz, x.threshold_db_nhl)
                ),
                confidence=x.confidence,
                method=x.method,
                status=x.status,
            )
            for x in thresholds
        ]
