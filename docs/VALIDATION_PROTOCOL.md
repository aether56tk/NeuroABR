# NeuroABR Empirical Validation Protocol

NeuroABR is a research prototype. The next major milestone is **empirical validation against human/reference ABR data**, not additional model complexity.

## Validation pipeline

```
Governed dataset
      ↓
Frozen input/protocol
      ↓
Reference clinician labels
      ↓
NeuroABR analysis
      ↓
Threshold + Wave-V outputs
      ↓
Paired error/agreement analysis
      ↓
Failure-case review
      ↓
Versioned validation report
```

## Required dataset metadata

At minimum retain:

- stimulus frequency
- stimulus type
- intensity in dB nHL
- transducer/stimulus system
- trial count
- sampling rate
- time window
- preprocessing settings
- participant group metadata allowed by the governance protocol
- reference threshold and/or response-present labels
- reference Wave-V latency where available

## Primary validation outcomes

For frequency-specific threshold estimation report:

- absolute threshold error
- signed threshold error
- median absolute error
- percentage within predefined error bands
- sensitivity/specificity for response-present classification when reference labels exist
- confidence/error relationship
- failure rate and reasons

Do not select acceptance thresholds after inspecting the results.

## Agreement analysis

Use an analysis appropriate to the reference design. Where paired continuous thresholds are available, report agreement/error plots and summary statistics rather than correlation alone. Correlation measures association; it does not establish agreement.

## Subgroup and failure analysis

Predefine relevant subgroups such as frequency, stimulus type, response quality, and recording condition where sample size permits. Preserve failed cases for review instead of silently excluding them.

## Version freeze

Every validation run should record:

- Git commit SHA
- NeuroABR version
- Python version
- dependency versions
- correction-table version
- preprocessing parameters
- objective detector parameters
- random seed
- dataset identifier/version

## Clinical boundary

Validation evidence must be established before describing automated thresholds as clinically validated. The software must not fabricate missing frequencies or apply an unvalidated universal nHL→eHL correction.
