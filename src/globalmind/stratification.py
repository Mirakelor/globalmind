"""Within-country post-stratification weighting for the Global Mind Project.

The GMP is an internet-based survey whose respondents are not selected
by probability sampling.  Certain demographic groups — younger, urban,
male users in well-connected countries — tend to be over-represented
relative to the general adult population.

This module provides two approaches:

1. **Iterative Proportional Fitting (IPF)** — rakes on three margins
   (year, age×sex, rural_urban) simultaneously via :func:`iterative_proportional_fitting`.
2. **Simple post-stratification** — single-step weighting by year,
   age_group, and sex via :func:`simple_stratification`.  Countries
   or years without population benchmarks receive ``_weight = null``.

Both methods operate on cell-aggregated counts (a few thousand rows)
and the resulting ``_weight`` column is joined back to the individual
records.  All operations are Polars-lazy except the cell aggregation
and the IPF iteration itself.

-----\n**Data coverage notes:**

* 2020–2021 lack ``rural_urban`` (the question was introduced
  in 2022).  Sex data for those years is recovered from the
  ``gender`` column.  Rows with missing rural‑urban are excluded
  from that margin; their weights come from year and age×sex.
* 2025–2026 urbanisation rates are not yet available from the World
  Bank.  We use the latest observed value (2024).
* Taiwan is not covered by the World Bank urbanisation indicator.
  Its rural‑urban margin is skipped — only year and age×sex are
  raked.

Usage::

    from globalmind import read_table, clean_data, iterative_proportional_fitting

    df = read_table("gmp_data.csv")
    df = clean_data(df)
    df = iterative_proportional_fitting(df)
    # df now has a _weight column — pass to weighted aggregations
"""

import polars as pl
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# Country name normalisation
# ═══════════════════════════════════════════════════════════════════════════════

_COUNTRY_NAME_MAP: dict[str, str] = {
    # GMP raw value → standardised name matching the benchmark data files.
    #
    # "भारत (इंडिया)" (Hindi for "India") appeared in ~1,300 rows
    # alongside 229K rows already labelled "India".  Merging them
    # ensures a single benchmark lookup and correct cell aggregation.
    "भारत (इंडिया)": "India",
}

# ═══════════════════════════════════════════════════════════════════════════════
# Stratum variable harmonisation maps
# ═══════════════════════════════════════════════════════════════════════════════

# -- age -----------------------------------------------------------------------
# From 2023 onwards the MHQ switched from pre-binned ranges (18-24, 25-34, …)
# to individual ages: 18, 19, 20, 21-24.  We collapse everything back to the
# original 8 groups so the stratification is consistent across all years.
_AGE_MAP: dict[str, str] = {
    "18":    "18-24",
    "19":    "18-24",
    "20":    "18-24",
    "21-24": "18-24",
}

# -- sex -----------------------------------------------------------------------
# The survey renamed its sex question between 2021 and 2022:
#   2020–2021  →  ``gender``          (Female / Male / Non-binary / …)
#   2022–2026  →  ``biological_sex``  (Female / Male / Other/Intersex / …)
#
# The two columns are *complementary* — never both non-null in the same row.
# We coalesce them into ``_stratum_sex``, then collapse the tiny (≈0.1 %)
# non‑binary categories into a single "Other" label.
#
# "N/A" and "Prefer not to say" are nulled out; those rows are excluded
# from the sex margin during raking but still receive weights from the
# other two margins.
_SEX_MAP: dict[str, str] = {
    "Female":                  "Female",
    "Male":                    "Male",
    # ── collapsed ──
    "Other/Intersex":          "Other",
    "अन्य / इंटरसेक्स":          "Other",
    "Other":                   "Other",
    "Non-binary/Third Gender": "Other",
}

# -- rural / urban -------------------------------------------------------------
# The raw column has four fine‑grained categories plus Hindi translations
# that appeared in 2026.  We collapse to a binary Urban / Rural split so
# that the single population benchmark — national urbanisation rate — can
# be used for raking.
#
# "N/A" (2020–2021, before the question was introduced) and
# "Prefer not to say" are nulled out.
_RURAL_URBAN_MAP: dict[str, str] = {
    # English
    "A large city":                  "Urban",
    "A small city or town":          "Urban",
    "A suburb near a large city":    "Urban",
    "A rural or remote community":   "Rural",
    # Hindi (2026)
    "एक बड़े शहर के पास का एक उपनगर (सबअर्ब)": "Urban",
    "एक ग्रामीण इलाका या दूर की जगह":         "Rural",
}

# Values to be turned into null (not used in raking for that margin).
_SEX_NULLS: frozenset[str] = frozenset({"N/A", "Prefer not to say"})
_RU_NULLS:  frozenset[str] = frozenset({"N/A", "Prefer not to say"})

# ═══════════════════════════════════════════════════════════════════════════════
# Harmonisation helper
# ═══════════════════════════════════════════════════════════════════════════════

def _harmonize_strata(df: pl.LazyFrame) -> pl.LazyFrame:
    """Normalise country names and unify stratum variables.

    Operates **lazily** on the incoming LazyFrame.  Original columns are
    left untouched; three new columns are added:

    ``_stratum_sex``
        Coalesced from ``biological_sex`` (2022+) and ``gender``
        (2020–2021), then mapped to Female / Male / Other / null.
    ``_stratum_age``
        Individual ages 18/19/20/21-24 folded into ``"18-24"``.
        The remaining group labels pass through unchanged.
    ``_stratum_ru``
        Four city/suburb/town/rural categories collapsed to
        ``"Urban"`` / ``"Rural"``, Hindi translations included.
        ``"N/A"`` and ``"Prefer not to say"`` become null.

    ``country``
        Normalised in-place via :data:`_COUNTRY_NAME_MAP`
        (currently only the Hindi‑script India variant).

    Returns
    -------
    pl.LazyFrame
    """
    # -- country ---------------------------------------------------------------
    df = df.with_columns(
        pl.col("country")
        .replace_strict(
            list(_COUNTRY_NAME_MAP.keys()),
            list(_COUNTRY_NAME_MAP.values()),
            default=pl.col("country"),
        )
        .alias("country")
    )

    # -- sex -------------------------------------------------------------------
    df = df.with_columns(
        pl.coalesce("biological_sex", "gender").alias("_stratum_sex")
    )
    df = df.with_columns(
        pl.col("_stratum_sex")
        .replace_strict(
            list(_SEX_MAP.keys()),
            list(_SEX_MAP.values()),
            default=pl.col("_stratum_sex"),
        )
        .alias("_stratum_sex")
    )
    df = df.with_columns(
        pl.when(pl.col("_stratum_sex").is_in(list(_SEX_NULLS)))
        .then(pl.lit(None, dtype=pl.Utf8))
        .otherwise(pl.col("_stratum_sex"))
        .alias("_stratum_sex")
    )

    # -- age -------------------------------------------------------------------
    df = df.with_columns(
        pl.col("age")
        .replace_strict(
            list(_AGE_MAP.keys()),
            list(_AGE_MAP.values()),
            default=pl.col("age"),
        )
        .alias("_stratum_age")
    )

    # -- rural_urban -----------------------------------------------------------
    df = df.with_columns(
        pl.col("rural_urban")
        .replace_strict(
            list(_RURAL_URBAN_MAP.keys()),
            list(_RURAL_URBAN_MAP.values()),
            default=pl.col("rural_urban"),
        )
        .alias("_stratum_ru")
    )
    df = df.with_columns(
        pl.when(pl.col("_stratum_ru").is_in(list(_RU_NULLS)))
        .then(pl.lit(None, dtype=pl.Utf8))
        .otherwise(pl.col("_stratum_ru"))
        .alias("_stratum_ru")
    )

    return df


# ═══════════════════════════════════════════════════════════════════════════════
# Iterative Proportional Fitting (within-country raking on three margins)
# ═══════════════════════════════════════════════════════════════════════════════

def iterative_proportional_fitting(
    df: pl.LazyFrame,
    max_iter: int = 50,
    tolerance: float = 1e-4,
) -> pl.LazyFrame:
    """Add a ``_weight`` column via Iterative Proportional Fitting (IPF).

    IPF is run **independently for each country** on three margins
    whose population targets are stored in the package data files::

        _data/pop_age_sex.csv   → year × country pop,  age × sex pyramid
        _data/urban_pct.csv     → urbanisation rate

    ------
    **Margin 1 — year**
        Per-country year proportions of the adult (18+) population.
        Ensures that e.g. 2020's weight contribution matches its share
        of the country's total adult population across 2020–2026.

    **Margin 2 — age_group × sex**
        Per-country × year proportions of each (age group, sex) cell in
        the adult age‑sex pyramid.  Eight age groups × (Female / Male).

    **Margin 3 — rural_urban**
        Per-country × year urban vs. rural split from the World Bank
        ``SP.URB.TOTL.IN.ZS`` indicator.  (Taiwan is not covered by
        this indicator; its rural‑urban margin is skipped.)

    ------
    **Null handling:**
    Rows with null ``_stratum_sex`` or null ``_stratum_ru`` are excluded
    from the corresponding margin.  Their weights are carried forward
    from the other margins (i.e. they receive an adjustment factor of 1).

    ------
    **Algorithm:**
    1. Harmonise strata via :func:`_harmonize_strata`.
    2. Aggregate to cell-level counts (cheap — a few thousand rows).
    3. Iterate:
       a. Fit margin 1 (country × year).
       b. Fit margin 2 (country × year × age × sex).
       c. Fit margin 3 (country × year × rural_urban).
       d. Normalise weights within each country so they sum to *n*.
       e. Check convergence (max absolute weight change).
    4. Clip weights to [0.05, 20] and join back to individual rows.

    Parameters
    ----------
    df : pl.LazyFrame
        GMP data **after** :func:`clean_data`.  Must contain the columns
        ``country``, ``year``, ``age``, ``biological_sex``, ``gender``,
        and ``rural_urban``.
    max_iter : int
        Maximum number of IPF iterations (default 50).
    tolerance : float
        Stop when the maximum absolute weight change across all cells
        falls below this value.

    Returns
    -------
    pl.LazyFrame
        The input frame unchanged except for:
        * ``country`` — normalised (Hindi‑script India merged).
        * ``_stratum_sex``, ``_stratum_age``, ``_stratum_ru`` — harmonised
          stratum columns added by :func:`_harmonize_strata`.
        * ``_weight`` (Float64) — post-stratification weight in [0.05, 20].
          Pass to Polars weighted aggregations or use as a survey weight.
    """
    # ── 1. Harmonise strata ─────────────────────────────────────────────────
    df = _harmonize_strata(df)
    df = df.with_columns(pl.col("year").cast(pl.Int64))

    # ── 2. Load population benchmarks ────────────────────────────────────────
    _data = Path(__file__).parent / "_data"
    pop = pl.read_csv(
        _data / "pop_age_sex.csv",
        # columns:  country, year, age_group, pop_male, pop_female, pop_total
    )
    urban = pl.read_csv(
        _data / "urban_pct.csv",
        # columns:  country, year, urban_pct
    )

    # ── 3. Build target margins (proportion columns _t1 / _t2 / _t3) ─────────

    # Margin 1 — year targets (within each country, sum = 1)
    m1 = (
        pop.group_by(["country", "year"])
        .agg(pl.col("pop_total").sum())
        .with_columns(
            (pl.col("pop_total") / pl.col("pop_total").sum().over("country"))
            .alias("_t1")
        )
        .select(["country", "year", "_t1"])
    )

    # Margin 2 — age × sex targets (within each country×year, sum = 1)
    m2_long = pl.concat([
        pop.select(["country", "year", "age_group",
                     pl.col("pop_male").alias("pop"),
                     pl.lit("Male").alias("_stratum_sex")]),
        pop.select(["country", "year", "age_group",
                     pl.col("pop_female").alias("pop"),
                     pl.lit("Female").alias("_stratum_sex")]),
    ])
    m2 = (
        m2_long
        .with_columns(
            (pl.col("pop") / pl.col("pop").sum().over(["country", "year"]))
            .alias("_t2")
        )
        .select(["country", "year", "_stratum_sex", "age_group", "_t2"])
        .rename({"age_group": "_stratum_age"})
    )

    # Margin 3 — urban / rural targets (within each country×year, sum = 1)
    m3 = pl.concat([
        urban.select(["country", "year",
                       (pl.col("urban_pct") / 100.0).alias("_t3"),
                       pl.lit("Urban").alias("_stratum_ru")]),
        urban.select(["country", "year",
                       (1.0 - pl.col("urban_pct") / 100.0).alias("_t3"),
                       pl.lit("Rural").alias("_stratum_ru")]),
    ])

    # ── 4. Aggregate to cell counts ──────────────────────────────────────────
    #    Only this step triggers collection — the cell table is at most
    #    ~10K rows (83 countries × 7 years × 8 ages × 3 sexes × 3 RU).
    #    Replace null stratum values with a sentinel so that Polars joins
    #    them correctly (null ≠ null in join keys).
    _NULL_SENTINEL = "__null__"
    cell_key = ["country", "year", "_stratum_sex", "_stratum_age", "_stratum_ru"]
    df = df.with_columns(
        pl.col("_stratum_sex").fill_null(_NULL_SENTINEL),
        pl.col("_stratum_ru").fill_null(_NULL_SENTINEL),
    )
    cells = df.group_by(cell_key).len().collect()
    cells = cells.with_columns(pl.lit(1.0).alias("_weight"))

    # ── 5. IPF iteration ─────────────────────────────────────────────────────
    for _ in range(max_iter):
        prev = cells["_weight"].to_list()

        # ---- Margin 1: country × year ---------------------------------------
        pw_country = cells.group_by("country").agg(
            pl.col("_weight").sum().alias("_pc")
        )
        current = cells.group_by(["country", "year"]).agg(
            pl.col("_weight").sum().alias("_w"),
        )
        current = current.join(pw_country, on="country", how="left")
        current = current.join(m1, on=["country", "year"], how="left")
        current = current.with_columns(
            pl.when(pl.col("_t1").is_not_null())
            .then(pl.col("_t1") / (pl.col("_w") / pl.col("_pc")))
            .otherwise(pl.lit(1.0))
            .alias("_adj1")
        )
        cells = cells.join(
            current.select(["country", "year", "_adj1"]),
            on=["country", "year"], how="left",
        )
        cells = cells.with_columns(
            (pl.col("_weight") * pl.col("_adj1")).alias("_weight")
        ).drop("_adj1")

        # ---- Margin 2: country × year × age × sex ---------------------------
        valid2 = cells.filter(pl.col("_stratum_sex") != _NULL_SENTINEL)
        # Only Male+Female have population benchmarks (_t2 sums to 1 over them).
        # Include Other in "current" so it gets adj=1, but exclude it from _pcy.
        pw_cy = (
            cells.filter(pl.col("_stratum_sex").is_in(["Male", "Female"]))
            .group_by(["country", "year"])
            .agg(pl.col("_weight").sum().alias("_pcy"))
        )
        current = valid2.group_by(
            ["country", "year", "_stratum_sex", "_stratum_age"]
        ).agg(
            pl.col("_weight").sum().alias("_w"),
        )
        current = current.join(pw_cy, on=["country", "year"], how="left")
        current = current.join(
            m2, on=["country", "year", "_stratum_sex", "_stratum_age"], how="left",
        )
        current = current.with_columns(
            pl.when(pl.col("_t2").is_not_null())
            .then(pl.col("_t2") / (pl.col("_w") / pl.col("_pcy")))
            .otherwise(pl.lit(1.0))
            .alias("_adj2")
        )
        cells = cells.join(
            current.select(["country", "year", "_stratum_sex", "_stratum_age", "_adj2"]),
            on=["country", "year", "_stratum_sex", "_stratum_age"], how="left",
        )
        cells = cells.with_columns(
            pl.when(pl.col("_adj2").is_not_null())
            .then(pl.col("_weight") * pl.col("_adj2"))
            .otherwise(pl.col("_weight"))
            .alias("_weight")
        ).drop("_adj2")

        # ---- Margin 3: country × year × rural_urban -------------------------
        valid3 = cells.filter(pl.col("_stratum_ru") != _NULL_SENTINEL)
        # Only Urban+Rural have population benchmarks (_t3 sums to 1 over them).
        pw_cy = (
            cells.filter(pl.col("_stratum_ru").is_in(["Urban", "Rural"]))
            .group_by(["country", "year"])
            .agg(pl.col("_weight").sum().alias("_pcy"))
        )
        current = valid3.group_by(
            ["country", "year", "_stratum_ru"]
        ).agg(
            pl.col("_weight").sum().alias("_w"),
        )
        current = current.join(pw_cy, on=["country", "year"], how="left")
        current = current.join(
            m3, on=["country", "year", "_stratum_ru"], how="left",
        )
        current = current.with_columns(
            pl.when(pl.col("_t3").is_not_null())
            .then(pl.col("_t3") / (pl.col("_w") / pl.col("_pcy")))
            .otherwise(pl.lit(1.0))
            .alias("_adj3")
        )
        cells = cells.join(
            current.select(["country", "year", "_stratum_ru", "_adj3"]),
            on=["country", "year", "_stratum_ru"], how="left",
        )
        cells = cells.with_columns(
            pl.when(pl.col("_adj3").is_not_null())
            .then(pl.col("_weight") * pl.col("_adj3"))
            .otherwise(pl.col("_weight"))
            .alias("_weight")
        ).drop("_adj3")

        # ---- Convergence check -----------------------------------------------
        if max(abs(a - b) for a, b in zip(cells["_weight"].to_list(), prev)) < tolerance:
            break

        # ---- Per-iteration normalisation (anchor sum to n per country) -------
        norm = cells.group_by("country").agg(
            pl.col("len").sum().alias("_nc"),
            pl.col("_weight").sum().alias("_wc"),
        )
        cells = cells.join(norm, on="country")
        cells = cells.with_columns(
            (pl.col("_weight") * pl.col("_nc") / pl.col("_wc")).alias("_weight")
        ).drop(["_nc", "_wc"])

    # ── 6. Clip weights ──────────────────────────────────────────────────────
    cells = cells.with_columns(
        pl.col("_weight").clip(0.05, 20.0).alias("_weight")
    )

    # ── 7. Join weights back to individual rows (lazy — no extra collection) ──
    cell_weights = cells.select(cell_key + ["_weight"]).lazy()
    df = df.join(cell_weights, on=cell_key, how="left")

    # Restore nulls from sentinel
    df = df.with_columns(
        pl.when(pl.col("_stratum_sex") == _NULL_SENTINEL)
        .then(pl.lit(None, dtype=pl.Utf8))
        .otherwise(pl.col("_stratum_sex"))
        .alias("_stratum_sex"),
        pl.when(pl.col("_stratum_ru") == _NULL_SENTINEL)
        .then(pl.lit(None, dtype=pl.Utf8))
        .otherwise(pl.col("_stratum_ru"))
        .alias("_stratum_ru"),
    )

    return df


# ═══════════════════════════════════════════════════════════════════════════════
# Simple post-stratification (year × age_group × sex, single-step)
# ═══════════════════════════════════════════════════════════════════════════════

def simple_stratification(df: pl.LazyFrame) -> pl.LazyFrame:
    """Add a ``_weight`` column via single-step post-stratification on
    year × age_group × sex.

    Unlike :func:`iterative_proportional_fitting`, this performs a
    **one-shot** weighting without iteration and without the rural‑urban
    margin.  For each country, weights are computed as:

    .. math::

        w_{\\text{cell}} = \\frac{P_{\\text{cell}} / P_{\\text{country}}}
                                 {n_{\\text{cell}} / n_{\\text{country}}}

    where *P* is the population benchmark and *n* the sample count.

    **Countries or years not found in the population benchmarks receive
    ``_weight = null``.**  Rows with ``_stratum_sex = null`` (e.g.
    "Other", "Prefer not to say") also receive null because the
    population benchmarks only cover Male and Female.

    Parameters
    ----------
    df : pl.LazyFrame
        GMP data **after** :func:`clean_data`.  Must contain the columns
        ``country``, ``year``, ``age``, ``biological_sex``, ``gender``.

    Returns
    -------
    pl.LazyFrame
        The input frame with ``country`` normalised and the columns
        ``_stratum_sex``, ``_stratum_age``, ``_weight`` added.
        ``_weight`` is null for rows whose country×year is absent from
        the population benchmarks.
    """
    # ── 1. Harmonise strata ─────────────────────────────────────────────────
    df = _harmonize_strata(df)
    df = df.with_columns(pl.col("year").cast(pl.Int64))

    # ── 2. Load population benchmarks ───────────────────────────────────────
    _data = Path(__file__).parent / "_data"
    pop = pl.read_csv(_data / "pop_age_sex.csv")
    # columns: country, year, age_group, pop_male, pop_female, pop_total

    # ── 3. Build target: country × year × age_group × sex proportions ───────
    # Total adult population per country (summed across all available years)
    pop_total_by_country = (
        pop.group_by("country")
        .agg(pl.col("pop_total").sum().alias("_pop_country"))
    )

    # Long-format target: each row = (country, year, age_group, sex, pop)
    target = pl.concat([
        pop.select([
            "country", "year", "age_group",
            pl.col("pop_male").alias("_pop"),
            pl.lit("Male").alias("_stratum_sex"),
        ]),
        pop.select([
            "country", "year", "age_group",
            pl.col("pop_female").alias("_pop"),
            pl.lit("Female").alias("_stratum_sex"),
        ]),
    ])
    # Attach total country pop and compute cell proportion
    target = target.join(pop_total_by_country, on="country", how="left")
    target = target.with_columns(
        (pl.col("_pop") / pl.col("_pop_country")).alias("_target_prop")
    ).rename({"age_group": "_stratum_age"})

    # ── 4. Aggregate sample to cells ────────────────────────────────────────
    cell_key = ["country", "year", "_stratum_sex", "_stratum_age"]
    cells = df.group_by(cell_key).len().collect()

    # Total sample n per country
    n_country = cells.group_by("country").agg(
        pl.col("len").sum().alias("_n_country")
    )
    cells = cells.join(n_country, on="country", how="left")
    cells = cells.with_columns(
        (pl.col("len") / pl.col("_n_country")).alias("_sample_prop")
    )

    # ── 5. Join with targets and compute weights ─────────────────────────────
    cells = cells.join(
        target.select(["country", "year", "_stratum_sex", "_stratum_age", "_target_prop"]),
        on=["country", "year", "_stratum_sex", "_stratum_age"],
        how="left",
    )
    cells = cells.with_columns(
        pl.when(pl.col("_target_prop").is_not_null())
        .then(pl.col("_target_prop") / pl.col("_sample_prop"))
        .otherwise(pl.lit(None, dtype=pl.Float64))
        .alias("_weight")
    )

    # ── 6. Normalise within country (sum of non-null weights → n) ────────────
    norm = (
        cells.filter(pl.col("_weight").is_not_null())
        .group_by("country")
        .agg(
            pl.col("len").sum().alias("_nc"),
            pl.col("_weight").sum().alias("_wc"),
        )
    )
    cells = cells.join(norm, on="country", how="left")
    cells = cells.with_columns(
        pl.when(pl.col("_weight").is_not_null())
        .then(pl.col("_weight") * pl.col("_nc") / pl.col("_wc"))
        .otherwise(pl.col("_weight"))
        .alias("_weight")
    ).drop(["_nc", "_wc"])

    # ── 7. Clip weights ─────────────────────────────────────────────────────
    cells = cells.with_columns(
        pl.when(pl.col("_weight").is_not_null())
        .then(pl.col("_weight").clip(0.05, 20.0))
        .otherwise(pl.col("_weight"))
        .alias("_weight")
    )

    # ── 8. Join weights back to individual rows ──────────────────────────────
    cell_weights = cells.select(cell_key + ["_weight"]).lazy()
    df = df.join(cell_weights, on=cell_key, how="left")

    return df
