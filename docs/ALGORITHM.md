# NeuroABR algorithm

## Design basis

NeuroABR combines published ideas without copying source code:

- **Resampled split-half reproducibility:** ABRpresto repeatedly partitions single-trial ABR responses and compares representative waveforms with normalized cross-correlation.
- **Adaptive objective detection:** published real-time ABR work uses cross-correlation of time-locked responses to automate threshold determination.
- **Frequency-specific clinical thresholding:** tone-burst/chirp ABR is used when frequency-specific thresholds are required, with protocol-specific nHL-to-eHL corrections.

## Detector

For every frequency/intensity:

1. accept repeated single-trial waveforms;
2. repeatedly split them into independent groups;
3. calculate median representative waveforms;
4. calculate normalized cross-correlation;
5. summarize the resampled correlation distribution;
6. derive a transparent response-evidence score;
7. classify response presence using a configurable criterion.

Across intensity, a monotonic logistic response curve is fitted when enough levels are available. The threshold is its criterion crossing. If fitting is unstable, the engine falls back to the lowest discrete reproducible response.

## Output

NeuroABR reports:

- threshold in dB nHL;
- optional validated dB eHL after correction;
- response evidence at every tested level;
- confidence and fit status;
- PTA-style summary only when the required corrected frequencies exist.

This is an automated **ABR response-threshold estimator**, not a universal conversion from a click ABR waveform to a behavioral audiogram.

## Validation

Before clinical deployment, validate against labelled human datasets containing stimulus, transducer, calibration, frequency, intensity, single-trial/subaverage waveforms, clinician response labels, manual ABR thresholds, and behavioral thresholds where available.

Recommended metrics include threshold bias/error, agreement within ±5/±10/±15 dB, response sensitivity/specificity, calibration of confidence, and failure-case analysis.
