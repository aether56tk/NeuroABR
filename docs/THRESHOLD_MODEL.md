# NeuroABR threshold model

## Goal

NeuroABR is designed to automate frequency-specific ABR threshold estimation using objective response detection inspired by the detection philosophy of ASSR.

It does **not** claim that a single broadband click ABR contains enough information to reconstruct a complete audiogram.

## Frequency-specific workflow

1. Identify stimulus frequency from metadata.
2. Group recordings by frequency and stimulus intensity.
3. Preprocess the waveform.
4. Compare independent subaverages/repeats.
5. Calculate reproducibility and SNR.
6. Combine objective response evidence with Wave-V evidence.
7. Search the intensity series for the lowest reproducible response.
8. Apply a validated nHL→eHL correction for the exact stimulus/transducer/population.
9. Display frequency-specific estimated thresholds.
10. Calculate PTA only from the available corrected frequency thresholds under the selected PTA definition.

## Example

500 Hz:
60 present → 40 present → 30 present → 20 absent

Estimated ABR response threshold: **30 dB nHL**.

This is an automated electrophysiologic threshold estimate, not automatically a behavioral hearing threshold.

## ASSR-inspired objective detection

ASSR demonstrates the value of objective statistical response detection. NeuroABR adapts that principle to ABR by combining:

- independent-subaverage reproducibility
- cross-correlation
- SNR
- response consistency across intensity
- Wave-V latency/morphology
- confidence scoring

Future versions can add frequency-domain/statistical detectors where the acquisition format supports them.

## PTA

PTA requires frequency-specific thresholds. Missing frequencies are reported as missing rather than fabricated.

## Validation

The system must be validated against clinician-labelled human ABR thresholds and, where PTA comparison is intended, appropriate behavioral audiometry. Performance should be reported with agreement/error metrics rather than assuming the automated output is correct.
