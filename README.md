# NeuroABR

**Frequency-specific automated ABR threshold estimation using objective response detection.**

NeuroABR is a research platform designed to reduce the manual workload involved in analyzing frequency-specific ABR recordings. It combines ABR waveform processing, reproducibility/cross-correlation, SNR, Wave-V evidence and automated intensity searching to produce frequency-specific **estimated ABR response thresholds**.

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

## Input format\n\nThe first working app accepts long-format single-trial CSV data with:\n\n`frequency_hz, intensity_db_nhl, trial_id, time_ms, amplitude`\n\nRepeated trials are grouped automatically by frequency and intensity. The application currently reports objective ABR thresholds in **dB nHL**. A validated correction table must be supplied before reporting eHL/PTA values.\n\n## Status

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
- [x] Response-curve threshold estimation
- [x] Streamlit upload application
- [ ] Sequential/bracketed threshold search
- [ ] Audiogram/PTA dashboard
- [ ] Human-data validation
- [ ] Machine-learning response classifier
