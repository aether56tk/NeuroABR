# NeuroABR: first real-data run

## What you need

1. Python 3.11+
2. Git
3. About 5–10 GB free disk for a small development subset.
4. Internet access.
5. Do not put downloaded research data into Git.

## Step 1 — clone the project

```bash
git clone https://github.com/aether56tk/NeuroABR.git
cd NeuroABR
```

## Step 2 — install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS/Linux, activate with `source .venv/bin/activate`.

## Step 3 — download a small EARNDB subset

Start with one normal-hearing listener and 20 averaged records:

```bash
python scripts/prepare_earndb.py --subjects N1 --max-records 20
```

The complete EARNDB archive is about 56.9 GB, so do not download the whole database initially. PhysioNet provides the database through WFDB and the project script uses the WFDB downloader to select records.

## Step 4 — inspect the generated data

The script creates:

`data/processed/earndb_averages.csv`

Columns include:

- subject
- frequency_hz
- level_pespl
- rep
- time_ms
- amplitude
- unit
- source_record

Important: EARNDB levels are **peSPL**, not dB nHL. This file is for algorithm development and reproducibility testing. It must not be sent through the clinical nHL-to-eHL correction table.

## Step 5 — run tests

```bash
pytest -q
```

## Step 6 — run the application

```bash
streamlit run app.py
```

## What we do next

### Phase A — detector validation
Use EARNDB independent first-half/second-half averages to test reproducibility, correlation, SNR and response-vs-level behavior.

### Phase B — human hearing-loss validation
Use EARH to test the detector on hearing-impaired human tone-burst ABRs. EARH contains 1 and 4 kHz tone-burst ABRs across levels and is openly accessible under ODC Attribution.

### Phase C — frequency-specific audiogram
Add human datasets containing multiple frequencies and behavioral audiograms. The pABR Dryad dataset is useful here because it contains frequency-specific EEG/pABR and behavioral data.

### Phase D — clinical target
Obtain a human dataset containing frequency-specific ABR plus behavioral pure-tone thresholds, protocol/transducer metadata, and validated nHL-to-eHL corrections. This is required before NeuroABR can be evaluated as a hearing-aid fitting input.

## Ground-truth rule

NeuroABR must compare its output against a reference rather than assuming its own Wave-V detector is correct:

`ABR waveform → NeuroABR threshold → corrected eHL → audiogram/PTA`

versus

`same patient → clinician/behavioral audiogram`

Report MAE, bias, correlation, frequency-specific error, threshold agreement within 5/10 dB, false-response rate and missed-response rate.

Do not train and test on the same participant. Split at the **subject level**, not at the waveform level.

## Data licensing

Check and preserve the original dataset license/citation. Do not commit downloaded waveform files to the NeuroABR Git repository unless the dataset license explicitly permits redistribution and we have deliberately chosen to redistribute it.
