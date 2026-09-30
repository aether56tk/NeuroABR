from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
from typing import Iterable

import numpy as np

from .presto import LevelEvidence, ThresholdFit, fit_threshold, level_evidence
from .correction import CorrectionTable
from .clinical import FrequencyThreshold, pure_tone_average


@dataclass(frozen=True)
class ABRLevel:
    frequency_hz: float
    intensity_db_nhl: float
    trials: np.ndarray
    wave_v_latency_ms: float | None = None


@dataclass(frozen=True)
class FrequencyResult:
    frequency_hz: float
    levels: tuple[LevelEvidence, ...]
    fit: ThresholdFit
    threshold_db_nhl: float | None
    threshold_db_ehl: float | None
    confidence: float
    status: str


@dataclass(frozen=True)
class SessionResult:
    frequencies: tuple[FrequencyResult, ...]
    pta_db_ehl: float | None
    pta_frequencies_hz: tuple[float, ...]
    warnings: tuple[str, ...]


def analyze_frequency(
    levels: Iterable[ABRLevel],
    *,
    n_resamples: int = 200,
    criterion: float = 0.30,
    seed: int = 0,
    correction_table: CorrectionTable | None = None,
) -> FrequencyResult:
    ordered = sorted(levels, key=lambda z: z.intensity_db_nhl)
    if not ordered:
        raise ValueError("At least one level is required.")

    frequency = float(ordered[0].frequency_hz)
    if any(float(z.frequency_hz) != frequency for z in ordered):
        raise ValueError("All levels must have the same frequency.")

    evidence = tuple(
        level_evidence(
            z.trials,
            z.intensity_db_nhl,
            n_resamples=n_resamples,
            criterion=criterion,
            seed=seed + i,
        )
        for i, z in enumerate(ordered)
    )
    fit = fit_threshold(list(evidence), criterion=criterion)
    threshold_nhl = fit.threshold_db_nhl
    threshold_ehl = None
    if threshold_nhl is not None and correction_table is not None:
        threshold_ehl = correction_table.apply(frequency, threshold_nhl)

    # Confidence is based on response strength, fit quality, and amount of
    # independent trial data, deliberately kept as a transparent heuristic.
    positive = [e.response_probability for e in evidence if e.response_present]
    strength = float(np.mean(positive)) if positive else 0.0
    fit_quality = 1.0 if fit.status == "estimated" else 0.6 if fit.status == "discrete_fallback" else 0.0
    trial_factor = min(1.0, float(np.mean([z.trials.shape[0] for z in ordered])) / 32.0)
    confidence = float(np.clip(0.55 * strength + 0.30 * fit_quality + 0.15 * trial_factor, 0.0, 1.0))

    status = "estimated" if threshold_nhl is not None else "no_detectable_response"
    return FrequencyResult(
        frequency_hz=frequency,
        levels=evidence,
        fit=fit,
        threshold_db_nhl=threshold_nhl,
        threshold_db_ehl=threshold_ehl,
        confidence=confidence,
        status=status,
    )


def analyze_session(
    levels: Iterable[ABRLevel],
    *,
    n_resamples: int = 200,
    criterion: float = 0.30,
    seed: int = 0,
    correction_table: CorrectionTable | None = None,
    pta_frequencies_hz: tuple[float, ...] = (500.0, 1000.0, 2000.0),
) -> SessionResult:
    grouped: dict[float, list[ABRLevel]] = defaultdict(list)
    for level in levels:
        grouped[float(level.frequency_hz)].append(level)

    results = tuple(
        analyze_frequency(
            grouped[f],
            n_resamples=n_resamples,
            criterion=criterion,
            seed=seed + i * 1000,
            correction_table=correction_table,
        )
        for i, f in enumerate(sorted(grouped))
    )

    values = {
        r.frequency_hz: r.threshold_db_ehl
        for r in results
        if r.threshold_db_ehl is not None
    }
    pta = calculate_pta(
        values,
        frequencies_hz=pta_frequencies_hz,
    ) if correction_table is not None else None

    warnings: list[str] = []
    if correction_table is None:
        warnings.append("No nHL-to-eHL correction table supplied; PTA/eHL is not calculated.")
    missing_pta = [f for f in pta_frequencies_hz if f not in values]
    if missing_pta:
        warnings.append("PTA frequencies missing: " + ", ".join(str(int(f)) for f in missing_pta) + " Hz.")

    return SessionResult(
        frequencies=results,
        pta_db_ehl=pta,
        pta_frequencies_hz=pta_frequencies_hz,
        warnings=tuple(warnings),
    )
