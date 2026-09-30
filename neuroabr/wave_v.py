from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.signal import find_peaks


@dataclass(frozen=True)
class WaveVCandidate:
    latency_ms: float
    amplitude: float
    prominence: float
    score: float


def detect_wave_v(
    time_ms: np.ndarray,
    waveform: np.ndarray,
    latency_window_ms: tuple[float, float] = (4.0, 10.0),
    polarity: str = "positive",
) -> WaveVCandidate | None:
    """Return the strongest Wave-V candidate in a configurable latency window.

    This is an initial research detector, not a validated clinical Wave-V
    classifier. Future versions will combine morphology, neighboring levels,
    reproducibility and learned features.
    """
    t = np.asarray(time_ms, dtype=float)
    x = np.asarray(waveform, dtype=float)

    if t.shape != x.shape or t.size < 5:
        raise ValueError("time_ms and waveform must have the same length.")

    mask = (t >= latency_window_ms[0]) & (t <= latency_window_ms[1])
    if not np.any(mask):
        return None

    segment = x[mask]
    if polarity == "negative":
        search = -segment
    elif polarity == "positive":
        search = segment
    else:
        raise ValueError("polarity must be 'positive' or 'negative'.")

    spread = float(np.std(search))
    prominence = max(spread * 0.25, np.finfo(float).eps)
    peaks, props = find_peaks(search, prominence=prominence)

    if len(peaks) == 0:
        return None

    best = int(np.argmax(props["prominences"]))
    idx = np.flatnonzero(mask)[peaks[best]]
    amp = float(x[idx])
    prom = float(props["prominences"][best])

    return WaveVCandidate(
        latency_ms=float(t[idx]),
        amplitude=amp,
        prominence=prom,
        score=float(prom / (spread + np.finfo(float).eps)),
    )
