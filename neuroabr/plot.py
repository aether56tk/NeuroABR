from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_stacked(
    waveforms: dict[float, pd.DataFrame],
    output: str | Path | None = None,
):
    """Plot stacked ABR waveforms keyed by dB nHL."""
    fig, ax = plt.subplots(figsize=(10, 6))

    offsets = list(range(len(waveforms)))
    for offset, intensity in zip(offsets, sorted(waveforms, reverse=True)):
        frame = waveforms[intensity]
        time = frame["time_ms"].to_numpy()
        amp = frame["amplitude"].to_numpy()
        scale = max(abs(amp).max(), 1e-12)
        y = offset + amp / scale * 0.35
        ax.plot(time, y, linewidth=1.2)
        ax.text(time.min(), offset + 0.38, f"{intensity:g} dB nHL")

    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Relative stacked response")
    ax.set_title("NeuroABR — ABR Waveforms")
    ax.grid(alpha=0.2)

    fig.tight_layout()
    if output is not None:
        fig.savefig(output, dpi=180)
    return fig, ax
