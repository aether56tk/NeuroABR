from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .detect import cross_correlation_score, snr_db


@dataclass(frozen=True)
class ObjectiveResponse:
    correlation: float
    snr_db: float
    reproducibility: float
    response_probability: float
    present: bool


def objective_response_score(
    subaverage_a: np.ndarray,
    subaverage_b: np.ndarray,
    noise: np.ndarray,
    correlation_threshold: float = 0.45,
    snr_threshold_db: float = 3.0,
) -> ObjectiveResponse:
    """ASSR-inspired objective response scoring for ABR subaverages.

    This is a research detector. It combines reproducibility and SNR rather
    than relying on visual Wave-V inspection alone.
    """
    corr = cross_correlation_score(subaverage_a, subaverage_b)
    snr = snr_db((np.asarray(subaverage_a) + np.asarray(subaverage_b)) / 2.0, noise)

    # Map useful detector evidence to a bounded 0-1 research score.
    corr_component = np.clip((corr + 1.0) / 2.0, 0.0, 1.0)
    snr_component = np.clip((snr - snr_threshold_db) / 12.0, 0.0, 1.0)
    probability = float(0.5 * corr_component + 0.5 * snr_component)

    present = bool(corr >= correlation_threshold and snr >= snr_threshold_db)

    return ObjectiveResponse(
        correlation=float(corr),
        snr_db=float(snr),
        reproducibility=float(corr_component),
        response_probability=probability,
        present=present,
    )
