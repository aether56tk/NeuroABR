from __future__ import annotations

import argparse
from pathlib import Path

from .io import load_multilevel_csv
from .threshold import LevelResult, estimate_threshold, response_table


def main() -> None:
    parser = argparse.ArgumentParser(description="NeuroABR prototype CLI")
    parser.add_argument("csv", type=Path, help="Long-format ABR CSV")
    args = parser.parse_args()

    levels = load_multilevel_csv(args.csv)

    print(f"Loaded {len(levels)} intensity levels.")
    print("Waveform lengths:", {k: len(v.amplitude) for k, v in levels.items()})

    # Placeholder until the response detector is connected to repeated subaverages.
    results = [LevelResult(intensity_db_nhl=k, response_present=False) for k in levels]
    threshold = estimate_threshold(results)

    for row in response_table(results):
        print(f"{row['intensity_db_nhl']:g} dB nHL: {row['response']}")
    print("Estimated threshold:", threshold if threshold is not None else "Not detected")


if __name__ == "__main__":
    main()
