from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class ABRWaveform:
    time_ms: pd.Series
    amplitude: pd.Series
    intensity_db_nhl: float | None = None


def load_csv(path: str | Path, intensity_db_nhl: float | None = None) -> ABRWaveform:
    """Load a single ABR waveform from CSV.

    Required columns: time_ms, amplitude.
    An optional intensity_db_nhl column may contain a single unique intensity.
    """
    frame = pd.read_csv(path)
    required = {"time_ms", "amplitude"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if frame[["time_ms", "amplitude"]].isna().any().any():
        raise ValueError("time_ms and amplitude must not contain missing values.")

    inferred = intensity_db_nhl
    if inferred is None and "intensity_db_nhl" in frame.columns:
        values = frame["intensity_db_nhl"].dropna().unique()
        if len(values) == 1:
            inferred = float(values[0])
        elif len(values) > 1:
            raise ValueError(
                "CSV contains multiple intensities. Split the file by intensity "
                "or use the multi-level loader."
            )

    return ABRWaveform(
        time_ms=frame["time_ms"].astype(float),
        amplitude=frame["amplitude"].astype(float),
        intensity_db_nhl=inferred,
    )


def load_multilevel_csv(path: str | Path) -> dict[float, ABRWaveform]:
    """Load long-format ABR data grouped by intensity."""
    frame = pd.read_csv(path)
    required = {"time_ms", "amplitude", "intensity_db_nhl"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    result: dict[float, ABRWaveform] = {}
    for intensity, group in frame.groupby("intensity_db_nhl", sort=False):
        result[float(intensity)] = ABRWaveform(
            time_ms=group["time_ms"].astype(float).reset_index(drop=True),
            amplitude=group["amplitude"].astype(float).reset_index(drop=True),
            intensity_db_nhl=float(intensity),
        )
    return result
