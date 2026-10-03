# NeuroABR

**Frequency-specific automated ABR threshold estimation using objective response detection.**

NeuroABR is a research platform designed to reduce the manual workload involved in analyzing frequency-specific ABR recordings. It combines ABR waveform processing, reproducibility/cross-correlation, SNR, Wave-V evidence and automated intensity searching to produce frequency-specific **estimated ABR response thresholds**.

## Research basis

The objective detector is based on published cross-correlation ABR thresholding concepts. NeuroABR independently implements repeated split-half reproducibility and compares **sigmoid and power-law response curves**, selecting the lower-error fit when sufficient levels are available. citeturn0search0turn0search2

Frequency-specific ABR threshold estimation requires frequency-specific stimuli; common clinical frequencies include 500, 1000, 2000 and 4000 Hz, with intensity reduced toward the lowest repeatable response. nHL-to-eHL correction is protocol/system dependent. citeturn0search4turn0search13

## Workflow

```
Frequency-specific ABR
        ↓
Signal quality + preprocessing
        ↓
Independent subaverage comparison
        ↓
Objective response detection
        ↓
Wave-V candidate analysis
        ↓
Automated threshold search
        ↓
Validated nHL → eHL correction
        ↓
Audiogram-style frequency display
        ↓
PTA-style summary when appropriate
```

## Why NeuroABR?

The goal is to automate repetitive waveform inspection and intensity stepping. The detector combines:

- waveform reproducibility
- cross-correlation
- SNR
- objective response evidence
- Wave-V morphology and latency
- neighboring intensity consistency
- confidence scoring
- frequency-specific threshold estimation

The objective-detection philosophy is inspired by ASSR, but NeuroABR is an **ABR-specific** analysis system, not an ASSR converter.

## Important limitation

A broadband click-ABR waveform does **not** provide enough independent frequency information to reconstruct a complete 250–8000 Hz audiogram by itself.

For frequency-specific estimation, NeuroABR expects frequency-specific ABR recordings such as tone-burst/chirp ABR, together with stimulus-frequency metadata.

NeuroABR will not fabricate missing frequencies.

## PTA

PTA is calculated only from available frequency-specific corrected thresholds under the selected PTA definition. A single ABR waveform is not automatically labelled as a conventional behavioral PTA.

## nHL → eHL

Conversion is stimulus-, transducer-, frequency- and population-dependent. NeuroABR therefore requires an explicit validated correction table/model instead of applying an unsupported universal correction.

## Input format

The first working app accepts long-format single-trial CSV data with:

`frequency_hz, intensity_db_nhl, trial_id, time_ms, amplitude`

Repeated trials are grouped automatically by frequency and intensity. The application currently reports objective ABR thresholds in **dB nHL**. A validated correction table must be supplied before reporting eHL/PTA values.

## First real-data run

Follow [`docs/GETTING_STARTED_DATA.md`](docs/GETTING_STARTED_DATA.md) to install WFDB support, download a small EARNDB subset, run the tests, and launch the Streamlit app.

## Public datasets

See [`docs/DATASETS.md`](docs/DATASETS.md) for the human and research ABR datasets identified for NeuroABR development and validation, including PhysioNet EARH/EARNDB, pABR Dryad data, and the 70-adult hearing-loss pABR study whose raw data are available on request.

## Project files

- [Validation protocol](docs/VALIDATION_PROTOCOL.md)
- [Security policy](SECURITY.md)
- [Contributing guide](CONTRIBUTING.md)
- [Citation metadata](CITATION.cff)

## Validation protocol

See [`docs/VALIDATION_PROTOCOL.md`](docs/VALIDATION_PROTOCOL.md) for the empirical validation workflow, required metadata, agreement analysis and version-freeze requirements.

## Status

**Research prototype / clinician decision-support only.** Automated estimates require validation against clinician-labelled human datasets before clinical use.

## Roadmap

- [x] CSV waveform ingestion
- [x] Baseline correction and band-pass filtering
- [x] Correlation/SNR response metrics
- [x] Wave-V candidate detector
- [x] Frequency-specific threshold model
- [x] Objective response score
- [x] nHL→eHL correction framework
- [x] Multi-subaverage objective ABR engine
- [x] Response-curve threshold estimation (sigmoid + power-law model selection)
- [x] Streamlit upload application
- [ ] Sequential/bracketed threshold search
- [ ] Audiogram/PTA dashboard
- [ ] Human-data validation
- [ ] Machine-learning response classifier
