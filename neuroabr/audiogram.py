from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import matplotlib.pyplot as plt

from .frequency import FrequencyThreshold


@dataclass(frozen=True)
class AudiogramPoint:
    frequency_hz: float
    threshold_db_ehl: float


def make_audiogram_points(
    thresholds: Iterable[FrequencyThreshold],
) -> list[AudiogramPoint]:
    return [
        AudiogramPoint(
            frequency_hz=float(x.frequency_hz),
            threshold_db_ehl=float(x.threshold_db_ehl),
        )
        for x in thresholds
        if x.threshold_db_ehl is not None
    ]


def plot_estimated_audiogram(
    thresholds: Iterable[FrequencyThreshold],
    output: str | None = None,
):
    points = make_audiogram_points(thresholds)
    if not points:
        raise ValueError("No corrected frequency-specific thresholds available.")

    points.sort(key=lambda x: x.frequency_hz)

    fig, ax = plt.subplots(figsize=(9, 5))
    x = [p.frequency_hz for p in points]
    y = [p.threshold_db_ehl for p in points]

    ax.plot(x, y, marker="o")
    ax.set_xscale("log", base=2)
    ax.invert_yaxis()
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Estimated threshold (dB eHL)")
    ax.set_title("NeuroABR — Estimated Frequency-Specific Thresholds")
    ax.grid(alpha=0.2, which="both")

    if output:
        fig.savefig(output, dpi=180, bbox_inches="tight")

    return fig, ax
