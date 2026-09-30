#!/usr/bin/env python3
"""Download a small EARNDB subset and convert averaged ABRs to CSV."""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import wfdb
from neuroabr.physionet import list_earndb_average_records, read_earndb_average

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subjects", nargs="+", default=["N1"])
    parser.add_argument("--max-records", type=int, default=20)
    parser.add_argument("--output", default="data/processed/earndb_averages.csv")
    args = parser.parse_args()
    records = list_earndb_average_records(args.subjects)
    if args.max_records > 0:
        records = records[:args.max_records]
    if not records:
        raise SystemExit("No EARNDB averaged records matched the requested subjects.")
    dl_dir = Path("data/raw/earndb")
    dl_dir.mkdir(parents=True, exist_ok=True)
    wfdb.dl_database("earndb/1.0.0/average", str(dl_dir), records=records, annotators=None, keep_subdirs=True, overwrite=False)
    rows = []
    for record in records:
        item = read_earndb_average(dl_dir / record)
        for t, amp in zip(item.time_ms, item.amplitude):
            rows.append({
                "subject": item.subject, "frequency_hz": item.frequency_khz * 1000.0,
                "level_pespl": item.level_pespl, "rep": item.repetition,
                "time_ms": t, "amplitude": amp, "unit": item.unit,
                "source_record": item.record_name,
            })
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output, index=False)
    print(f"Wrote {len(rows):,} samples from {len(records)} records to {output}")

if __name__ == "__main__":
    main()
