from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

import numpy as np

try:
    import wfdb
except ImportError:  # pragma: no cover
    wfdb = None

_EARNDB_RE = re.compile(
    r"^(?P<subject>N\d+)_evoked_ave(?P<level>[-+]?\d+(?:\.\d+)?)"
    r"_F(?P<freq>[-+]?\d+(?:\.\d+)?)_R(?P<rep>\d+)(?:_x)?$",
    re.IGNORECASE,
 )

@dataclass(frozen=True)
class PhysioNetABR:
    """One EARNDB independent averaged ABR recording.

    EARNDB levels are peSPL, not dB nHL. Do not pass these values directly
    into a clinical nHL-to-eHL correction table.
    """
    subject: str
    frequency_khz: float
    level_pespl: float
    repetition: int
    sampling_rate_hz: float
    time_ms: np.ndarray
    amplitude: np.ndarray
    unit: str
    record_name: str

def parse_earndb_average_name(record_name: str) -> dict:
    """Parse an EARNDB averaged record basename."""
    match = _EARNDB_RE.match(Path(record_name).name)
    if not match:
        raise ValueError(f"Not a recognized EARNDB average record: {record_name}")
    values = match.groupdict()
    return {
        "subject": values["subject"].upper(),
        "frequency_khz": float(values["freq"]),
        "level_pespl": float(values["level"]),
        "repetition": int(values["rep"]),
    }

def _require_wfdb():
    if wfdb is None:
        raise ImportError("WFDB support requires the 'wfdb' package. Install with: pip install wfdb")

def read_earndb_average(record_name: str | Path, *, pn_dir: str | None = None) -> PhysioNetABR:
    """Read only the ABR channel from an EARNDB averaged record."""
    _require_wfdb()
    record_name = str(record_name)
    header = wfdb.rdheader(record_name, pn_dir=pn_dir)
    candidates = []
    for idx, (name, unit) in enumerate(zip(header.sig_name, header.units)):
        lname = str(name).strip().lower()
        lunit = str(unit).strip().lower()
        if "abr" in lname:
            candidates.append((idx, lunit))
    if not candidates:
        raise ValueError(f"No ABR channel found in WFDB record: {record_name}")
    channel = next((idx for idx, unit in candidates if "nv" in unit), candidates[0][0])
    signal, fields = wfdb.rdsamp(record_name, pn_dir=pn_dir, channels=[channel], return_res=64)
    meta = parse_earndb_average_name(record_name)
    fs = float(fields["fs"])
    amplitude = np.asarray(signal[:, 0], dtype=float)
    time_ms = np.arange(amplitude.size, dtype=float) / fs * 1000.0
    return PhysioNetABR(
        subject=meta["subject"], frequency_khz=meta["frequency_khz"],
        level_pespl=meta["level_pespl"], repetition=meta["repetition"],
        sampling_rate_hz=fs, time_ms=time_ms, amplitude=amplitude,
        unit=str(fields["units"][channel]), record_name=record_name,
    )

def list_earndb_average_records(records: list[str] | None = None, *, pn_dir: str = "earndb/1.0.0") -> list[str]:
    """List EARNDB averaged records without downloading waveform data."""
    _require_wfdb()
    available = wfdb.get_record_list(pn_dir)
    allowed = {s.upper() for s in records} if records else None
    output = []
    for item in available:
        name = Path(item).name
        try:
            meta = parse_earndb_average_name(name)
        except ValueError:
            continue
        if allowed is None or meta["subject"] in allowed:
            output.append(item)
    return sorted(output)
