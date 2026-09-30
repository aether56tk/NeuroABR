# NeuroABR threshold model

## Two different outputs

### 1. ABR response threshold

When the user supplies ABR recordings at multiple stimulus intensities, NeuroABR can estimate the lowest tested intensity at which a reproducible response is detected.

Example:

| Level | Response |
|---:|---|
| 60 dB nHL | Present |
| 40 dB nHL | Present |
| 30 dB nHL | Present |
| 20 dB nHL | Absent |

Output: **estimated ABR response threshold = 30 dB nHL**.

### 2. PTA

PTA is a pure-tone audiometric measure. NeuroABR must not label a single ABR waveform as a PTA.

To calculate PTA, the system needs frequency-specific thresholds, for example:

- 500 Hz
- 1000 Hz
- 2000 Hz

and those thresholds must be in an appropriate comparable scale (such as dB HL or appropriately corrected dB eHL).

The first implementation therefore calculates:

**PTA = (500 + 1000 + 2000 Hz thresholds) / 3**

only when all three frequency-specific values are supplied.

## Future ABR → eHL support

Frequency-specific ABR nHL-to-eHL correction will be implemented as a configurable table/model. It must be tied to stimulus type, transducer, frequency and the validation dataset rather than using a universal correction.

## Clinical status

All automated outputs are research estimates requiring clinician verification. NeuroABR does not diagnose hearing loss.
