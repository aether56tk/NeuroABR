# NeuroABR — Public ABR datasets for development and validation

This project needs **frequency-specific ABR waveforms + intensity metadata + repeated trials/averages + a reference threshold/audiogram**.

Do not commit downloaded research datasets to this repository. Use the source repositories and keep only scripts/manifests locally.

## 1. Primary human dataset: PhysioNet EARH

**Evoked Auditory Responses in Hearing Impaired (EARH)**

- Source: https://physionet.org/content/earh/1.0.0/
- License: Open Data Commons Attribution License v1.0
- Size: ~13 GB uncompressed
- Participants: 8 adults with hearing impairment
- Age: 40–85 years
- Recording: tone-burst ABR + OAE
- Stimuli: 1 kHz and 4 kHz tone bursts
- Levels: approximately threshold to 100 dB peSPL in 5 dB steps
- Raw records are stored in WFDB format with frequency, level, ear and trial encoded in the record name.
- Clinical/behavioral reference thresholds are included in the metadata.

**Use in NeuroABR:** parser testing, single-trial/level grouping, threshold detection, waveform QC, and validation against known hearing-impaired recordings.

Download:

```bash
wget -r -N -c -np https://physionet.org/files/earh/1.0.0/
```

## 2. Primary human normal-hearing dataset: PhysioNet EARNDB

**Evoked Auditory Responses in Normals across Stimulus Level**

- Source: https://www.physionet.org/content/earndb/1.0.0/
- License: Open Data Commons Attribution License v1.0
- Size: ~56.9 GB uncompressed
- Participants: 8 healthy listeners
- Raw ABR + OAE recordings
- Independent first-half and second-half averages
- Stimulus levels increase in 5 dB steps from the listener threshold to 100 dB peSPL
- Raw and averaged data are available.
- Headers include stimulus frequency, level, ear, trial length and condition.

**Use in NeuroABR:** normal-hearing baseline, reproducibility testing, split-half validation, SNR/QC development, and level-response modeling.

Download:

```bash
wget -r -N -c -np https://physionet.org/files/earndb/1.0.0/
```

## 3. High-value human frequency-specific dataset: pABR Dryad

**Optimizing parameters for using the parallel auditory brainstem response (pABR) to quickly estimate hearing thresholds**

- Source: https://doi.org/10.5061/dryad.1c59zw3vm
- 20 adults per experiment, normal hearing
- Frequency-specific pABR using five frequencies
- Behavioral thresholds and stimulus correction factors are included
- EEG/pABR dataset is ~9.9 GB; behavioral dataset is ~15 MB.
- Particularly useful for validating frequency-specific processing and nHL correction concepts.

**Use in NeuroABR:** frequency-specific waveform processing, correction-factor pipeline, and audiogram construction tests.

## 4. Most important target dataset for final validation: 70-adult hearing-loss pABR study

Polonenko & Maddox reported a 70-adult study with widely varying sensorineural hearing-loss configurations.

- Frequencies: 500–8000 Hz octave frequencies
- Both ears
- Behavioral pure-tone audiogram used as ground truth
- pABR threshold estimates were compared against behavioral thresholds
- 79% of pABR thresholds were within one 10-dB step of behavioral thresholds.
- The authors report per-frequency correlations and errors.
- **The study data are currently available on reasonable request rather than as a public download.**

Paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC12697277/

**Action:** request the raw pABR waveforms, threshold-search logs, behavioral audiograms, stimulus calibration/correction metadata, and participant-level inclusion/exclusion metadata from the authors.

## 5. Algorithm-development datasets (animal; do not use as clinical ground truth)

### ABRpresto / Regeneron

- GitHub: https://github.com/Regeneron-RGM/ABRpresto
- Zenodo: https://zenodo.org/records/13987792
- 7,857 waveform stacks from 351 mice
- 123,140 single-trial ABR waveforms
- Expert human-rated ABR thresholds
- Frequency-specific tone-pip recordings and multiple intensity levels.

**Use:** objective threshold-engine development and regression testing only. Mouse thresholds/frequencies/corrections must not be presented as human hearing-aid fitting data.

### Stanford trial-by-trial ABR dataset

- Dryad: https://doi.org/10.5061/dryad.2jm63xt4j
- 5 rats
- 514 trials per level
- 16 kHz tone pips
- 5 dB intensity steps.

**Use:** single-trial detection experiments and stress-testing objective scoring. Not human clinical validation.

## 6. Data that NeuroABR should eventually collect from a clinical partner

For the hearing-aid/PTA objective, the ideal human dataset should contain:

| Field | Required |
|---|---|
| Subject ID | Yes |
| Ear | Yes |
| Age | Yes |
| Stimulus frequency | Yes |
| Stimulus type | Yes |
| Transducer | Yes |
| Calibration/reference level | Yes |
| Intensity in dB nHL/peSPL | Yes |
| Individual trial waveforms | Strongly preferred |
| Number of trials | Yes |
| Behavioral PTA/audiogram | **Ground truth** |
| ABR threshold selected by clinician | **Ground truth** |
| nHL→eHL correction protocol | Yes |
| Wave-V present/absent | Strongly preferred |
| Wave-V latency | Preferred |
| Artifact/rejection information | Preferred |
| Hearing-loss type/configuration | Preferred |
| Bone-conduction ABR metadata | Optional but valuable |

### Minimum frequency set

For an audiogram/PTA-oriented prototype:

`500, 1000, 2000, 4000 Hz`

For a fuller audiogram:

`250, 500, 1000, 2000, 4000, 8000 Hz`

The software must report missing frequencies instead of interpolating them as if they were measured.

## Recommended development sequence

1. **EARNDB** → normal waveform/QC and reproducibility.
2. **EARH** → human hearing-loss waveform testing.
3. **pABR Dryad** → frequency-specific processing + correction-factor pipeline.
4. **70-adult pABR dataset** → request raw data for the main human validation set.
5. **Local clinical dataset** → prospective validation against behavioral audiograms before any clinical/hearing-aid use.

## Important

The animal datasets are excellent for algorithm development but cannot establish human nHL→eHL corrections or hearing-aid fitting accuracy. Human validation must remain the final validation layer.
