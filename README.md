# NeuroABR

NeuroABR is an open-source research platform for Auditory Brainstem Response (ABR) waveform analysis.

## Current scope

- Import ABR waveform CSV files
- Preprocess waveforms with baseline correction and configurable band-pass filtering
- Estimate response strength using reproducibility/correlation and SNR-style metrics
- Generate response-present / response-absent decisions
- Estimate the lowest tested intensity with a detectable response
- Visualize stacked ABR waveforms
- Keep results explicitly research-oriented and clinician-reviewable

## Research safety

NeuroABR is a research/decision-support prototype. An automated estimate must not be treated as an autonomous clinical diagnosis or as a direct dB HL hearing threshold without appropriate validation and stimulus/transducer-specific correction.

## CSV format

The first version accepts a CSV with:

- `time_ms`: time in milliseconds
- `amplitude`: voltage/amplitude
- Optional `intensity_db_nhl`: stimulus intensity for each row

For multi-level datasets, the preferred format is one file per intensity, or a long-format CSV with an `intensity_db_nhl` column.

Example:

```csv
time_ms,amplitude,intensity_db_nhl
0.0,0.012,80
0.1,0.010,80
...
```

## Development

Python 3.10+ is recommended.

```bash
pip install -r requirements.txt
pytest
python -m neuroabr.cli --help
```

## Roadmap

1. Waveform import and validation
2. DSP preprocessing
3. Reproducibility/response detection
4. Wave V candidate detection
5. Automated threshold estimation
6. ABRpresto-inspired cross-correlation module
7. Validation against clinician-labelled human ABR datasets
8. Web interface and report generation
