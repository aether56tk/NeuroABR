from __future__ import annotations

import io
import tempfile
import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import streamlit as st

from neuroabr.io import load_trial_csv
from neuroabr.session import ABRLevel, analyze_session

st.set_page_config(page_title="NeuroABR", layout="wide")
st.title("NeuroABR")
st.caption("From frequency-specific ABR waveform trials to objective response thresholds.")

st.warning(
    "Research/decision-support prototype. Do not use the output as a standalone clinical diagnosis. "
    "Frequency-specific ABR and protocol-validated calibration/correction information are required."
)

uploaded = st.file_uploader(
    "Upload long-format single-trial ABR CSV",
    type=["csv"],
    help="Columns: frequency_hz, intensity_db_nhl, trial_id, time_ms, amplitude",
)

col1, col2, col3 = st.columns(3)
with col1:
    n_resamples = st.number_input("Resamples", min_value=25, max_value=1000, value=200, step=25)
with col2:
    criterion = st.number_input("Response criterion", min_value=0.05, max_value=0.95, value=0.30, step=0.05)
with col3:
    seed = st.number_input("Random seed", min_value=0, value=0, step=1)

if uploaded is None:
    st.info(
        "Expected format: one row per sample. Repeated trials must have different trial_id values. "
        "Example frequencies: 500, 1000, 2000, 4000 Hz."
    )
    st.stop()

try:
    data = pd.read_csv(uploaded)
    required = {"frequency_hz", "intensity_db_nhl", "trial_id", "time_ms", "amplitude"}
    missing = required - set(data.columns)
    if missing:
        st.error(f"Missing columns: {sorted(missing)}")
        st.stop()

    levels: list[ABRLevel] = []
    for (frequency, intensity, trial_id), group in data.groupby(
        ["frequency_hz", "intensity_db_nhl", "trial_id"], sort=True
    ):
        group = group.sort_values("time_ms")
        levels.append(
            ABRLevel(
                frequency_hz=float(frequency),
                intensity_db_nhl=float(intensity),
                trials=group[["amplitude"]].to_numpy(dtype=float).reshape(1, -1),
            )
        )

    # Combine trial rows into one ABRLevel per frequency/intensity.
    grouped: dict[tuple[float, float], list[np.ndarray]] = {}
    for level in levels:
        grouped.setdefault((level.frequency_hz, level.intensity_db_nhl), []).append(level.trials[0])

    analysis_levels = [
        ABRLevel(frequency_hz=f, intensity_db_nhl=i, trials=np.vstack(trials))
        for (f, i), trials in grouped.items()
    ]

    result = analyze_session(
        analysis_levels,
        n_resamples=int(n_resamples),
        criterion=float(criterion),
        seed=int(seed),
        correction_table=None,
    )

    st.subheader("Frequency-specific results")

    quality = pd.DataFrame([{
        "Rows": len(data),
        "Frequencies": data["frequency_hz"].nunique(),
        "Intensity levels": data["intensity_db_nhl"].nunique(),
        "Trials": data["trial_id"].nunique(),
        "Sampling points": len(data),
    }])
    st.caption("Input summary")
    st.dataframe(quality, use_container_width=True, hide_index=True)
    table = pd.DataFrame([
        {
            "Frequency (Hz)": r.frequency_hz,
            "ABR threshold (dB nHL)": r.threshold_db_nhl,
            "Confidence": round(r.confidence, 3),
            "Fit": r.fit.status,
            "Status": r.status,
        }
        for r in result.frequencies
    ])
    st.dataframe(table, use_container_width=True)

    for r in result.frequencies:
        with st.expander(f"{int(r.frequency_hz)} Hz — {r.status}"):
            evidence = pd.DataFrame([
                {
                    "Intensity (dB nHL)": e.intensity_db_nhl,
                    "Mean correlation": round(e.mean_correlation, 4),
                    "Correlation SD": round(e.correlation_sd, 4),
                    "Response probability": round(e.response_probability, 4),
                    "Response": "Present" if e.response_present else "Absent",
                }
                for e in r.levels
            ])
            st.dataframe(evidence, use_container_width=True)

    chart_rows = [
        {"frequency_hz": r.frequency_hz, "threshold_db_nhl": r.threshold_db_nhl}
        for r in result.frequencies
        if r.threshold_db_nhl is not None
    ]
    if chart_rows:
        st.subheader("Threshold overview")
        chart = pd.DataFrame(chart_rows).sort_values("frequency_hz").set_index("frequency_hz")
        st.line_chart(chart)

    export_rows = [
        {
            "frequency_hz": r.frequency_hz,
            "threshold_db_nhl": r.threshold_db_nhl,
            "confidence": r.confidence,
            "fit_status": r.fit.status,
            "status": r.status,
        }
        for r in result.frequencies
    ]
    export_csv = pd.DataFrame(export_rows).to_csv(index=False)
    manifest = {
        "software": "NeuroABR",
        "exported_at_utc": datetime.now(timezone.utc).isoformat(),
        "n_resamples": int(n_resamples),
        "criterion": float(criterion),
        "seed": int(seed),
        "rows": int(len(data)),
        "frequencies_hz": sorted(float(x) for x in data["frequency_hz"].unique()),
        "results": export_rows,
        "warnings": result.warnings,
    }
    st.subheader("Export")
    st.download_button(
        "Download threshold CSV",
        export_csv,
        file_name="neuroabr_thresholds.csv",
        mime="text/csv",
    )
    st.download_button(
        "Download analysis JSON",
        json.dumps(manifest, indent=2),
        file_name="neuroabr_analysis.json",
        mime="application/json",
    )

    if result.warnings:
        for warning in result.warnings:
            st.info(warning)

except Exception as exc:
    st.error(f"Analysis failed: {exc}")
