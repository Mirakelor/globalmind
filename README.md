# globalmind

[![PyPI - Version](https://img.shields.io/pypi/v/globalmind.svg)](https://pypi.org/project/globalmind)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/globalmind.svg)](https://pypi.org/project/globalmind)

-----

Python pipeline for the [Global Mind Project (GMP)](https://sapienlabs.org/global-mind-project/) — ingest, filter, profile, and
classify mental health data collected through the Mind Health Quotient (MHQ).

## Background

The Global Mind database contains mental health profiles from nearly 2 million
internet-enabled respondents across 130+ countries in 17+ languages, with
1,000–2,000 new responses added each day. Data are collected using the **Mind
Health Quotient (MHQ)** — an online assessment developed from a review of over
10,000 questions drawn from 126 commonly used mental health tools spanning 10
disorders. The MHQ consists of 47 items that rate individual aspects of mind
health on a 1–9 scale, together with aggregate scores, demographics, and
lifestyle/life‑context factors.

`globalmind` provides a pure‑Polars pipeline to go from raw CSV exports to
DSM‑5 diagnostic classifications in a few lines of code. All operations are
**lazy** (build a query plan, `.collect()` once at the end) for memory‑safe
processing of the full dataset.

## Features

### Data loading & cleaning
- **`read_table(path)`** — scan CSV with automatic N/A → null conversion,
  pipe‑delimited multi‑select splitting (21 columns), and stray‑pipe cleanup on
  single‑select categoricals.
- **`clean_data(df)`** — apply four quality filters:
  - completion time ≥ 7 minutes
  - response variance across 47 rating items (std dev ≥ 0.2)
  - comprehension check (`understanding` ≠ "No")
  - countries with ≥ 1,000 responses

### 205‑column schema
- **`COLUMN_DESCRIPTIONS`** — dictionary mapping every column name to an
  English description with a Chinese gloss.
- **`describe_column(name)`** — lookup helper.

### Symptom identification & DSM‑5 mapping
- **`identify_symptoms(df)`** — flags each of the 47 MHQ items as a clinical
  symptom per DSM‑5 thresholds:
  - *Problem items* (20): threshold ≥ 8 on a 1–9 severity scale
  - *Spectrum items* (27): threshold ≤ 1 (challenge end of the spectrum)
  - Adds 47 `_symptom` boolean columns + a `symptom_count` column.
- **`mapping_to_DSM5(df)`** — data‑driven rule engine classifying 10 disorder
  categories: Depression, Anxiety, Bipolar, PTSD, OCD, Schizophrenia, Eating
  Disorder, Addiction, ADHD, ASD.

## Installation

```console
pip install globalmind
```

Requires Python ≥ 3.10 and `polars ≥ 1.0`.

## Quick start

```python
from globalmind import (
    read_table, clean_data,
    identify_symptoms, mapping_to_DSM5,
)

df = read_table("gmp_data.csv")
df = clean_data(df)
df = identify_symptoms(df)
df = mapping_to_DSM5(df)
df.collect()  # all operations are lazy
```

## References

- **Data cleaning criteria** — Bala, Jerzy, Oleksii Sukhoi, Jennifer Jane
  Newson, Priscila Pereira Machado, Mark Lawrence, and Tara C. Thiagarajan.
  "Estimation of the Nature and Magnitude of Mental Distress in the Population
  Associated with Ultra-Processed Food Consumption." *Frontiers in Nutrition* 12
  (November 2025): 1562286.
  [https://doi.org/10.3389/fnut.2025.1562286](https://doi.org/10.3389/fnut.2025.1562286)
- **Symptom thresholds & DSM‑5 mapping** — Newson, Jennifer Jane, Vladyslav
  Pastukh, and Tara C. Thiagarajan. "Poor Separation of Clinical Symptom
  Profiles by DSM-5 Disorder Criteria." *Frontiers in Psychiatry* 12 (November
  2021): 775762.
  [https://doi.org/10.3389/fpsyt.2021.775762](https://doi.org/10.3389/fpsyt.2021.775762)

## License

`globalmind` is distributed under the terms of the
[MIT](https://spdx.org/licenses/MIT.html) license.
