from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CorrectionFactor:
    frequency_hz: float
    correction_db: float


@dataclass(frozen=True)
class CorrectionTable:
    """Validated stimulus/transducer/population-specific nHL -> eHL corrections.

    correction_db is subtracted from the measured nHL threshold.
    Do not use generic values unless they have been validated for the
    acquisition protocol.
    """
    factors: tuple[CorrectionFactor, ...]
    name: str = "custom"

    def apply(self, frequency_hz: float, threshold_db_nhl: float) -> float:
        for factor in self.factors:
            if float(factor.frequency_hz) == float(frequency_hz):
                return float(threshold_db_nhl - factor.correction_db)
        raise KeyError(
            f"No validated correction exists for {frequency_hz:g} Hz in {self.name!r}."
        )

    def frequencies(self) -> tuple[float, ...]:
        return tuple(f.frequency_hz for f in self.factors)
