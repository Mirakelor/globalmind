from pathlib import Path
import polars as pl

# Columns whose values are pipe-delimited multi-select strings.
_PIPE_DELIMITED_COLS: list[str] = [
    "live_close_nature",
    "time_nature",
    "sleep_problem_type",
    "work_factors",
    "substance_use",
    "medical_condition_type",
    "treatment_type_new",
    "treatment_type",
    "trauma_childhood",
    "trauma_adulthood",
    "friendship_type",
    "parental_support",
    "help_seeking",
    "mental_health_disorder",
    "internet_restrictions",
    "sm_impact",
    "ai_use_general",
    "ai_use_social",
    "ai_impact_personal",
    "ai_impact_work",
    "immersion_nature",
]

# Clean | artifacts from single-select categorical columns
_SINGLE_SELECT_PIPE_COLS: list[str] = [
    "ethnicity",
    "income_household",
    "city",
    "country",
    "employment_sector",
    "job_sector",
    "work_activity",
    "family_situation",
]

# Rating questions (1-9 scale, all MHQ items except categorical _type cols)
_RATING_COLS = [
    "adapt_to_change", "self_worth_confidence", "creativity_problem_solving",
    "drive_motivation", "stability_calmness", "sleep_quality",
    "self_control_impulsivity", "ability_learn", "coordination", "relationships",
    "emotional_resilience", "planning_organization", "physical_intimacy",
    "speech_language", "memory", "social_cooperation", "decision_risk",
    "curiosity_enthusiasm", "energy", "emotional_control", "focus_concentration",
    "appetite_regulation", "empathy", "sensory_sensitivity", "self_image",
    "outlook_optimism", "selective_attention", "restless_hyperactive",
    "fear_anxiety", "infections", "aggression", "avoidance", "obsessive_thoughts",
    "mood_swings", "detached_reality", "nightmares", "addictions", "anger",
    "suicidal_thoughts", "pain", "guilt_blame", "hallucinations", "flashblacks",
    "repetitive_actions", "sad_hopeless", "physical_health", "confusion",
]

def read_table(path: str) -> pl.LazyFrame:
    """Reads a CSV file and returns a Polars LazyFrame.
    Args:
        path (str): The path to the CSV file.
    Returns:
        pl.LazyFrame: The resulting Polars LazyFrame.
    Raises:
        FileNotFoundError: If the specified file does not exist.
        NotImplementedError: If the file format is not supported.
    """
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if source.suffix.lower() == ".csv":
        _score_cols = [
            "overall_mhq_score", "cognition_score", "adapt_resilience_score",
            "drive_motivation_score", "mood_outlook_score", "social_self_score",
            "mind_body_score",
        ]
        df = pl.scan_csv(
            path,
            infer_schema_length=0,
            null_values=["N/A", "NA", "null", "", "Prefer not to say"],
            schema_overrides={c: pl.Float64 for c in _RATING_COLS + _score_cols},
            )
        df = df.with_columns([
            pl.col(col).str.split("|").list.eval(pl.element().filter(pl.element().str.strip_chars() != "")).alias(col) 
            if col != "substance_use" 
            else pl.col(col).str.split("|").list.eval(pl.element().str.replace_all("##PIPE##", "|").filter(pl.element().str.strip_chars() != "")).alias(col)
            for col in _PIPE_DELIMITED_COLS
        ])
        df = df.with_columns([
            pl.col(col).str.strip_chars("|").str.replace_all(r"\|+", ",").alias(col) 
            for col in _SINGLE_SELECT_PIPE_COLS
        ])
        return df
    else:
        raise NotImplementedError(f"Unsupported file format: {source.suffix}")
    
def clean_data(df: pl.LazyFrame) -> pl.LazyFrame:
    """Apply GMP data quality filters.

    Removes records if:
    - time_to_complete < 7 minutes
    - same option selected for all rating questions (std dev < 0.2)
    - responded 'No' to 'Did you find this assessment easy to understand?'
    - country has fewer than 1,000 responses
    """
    # Filter out records with time_to_complete < 7 minutes
    df = df.with_columns(
        (pl.col("time_to_complete").str.split(":").list.get(0).cast(pl.Int64) * 60 + pl.col("time_to_complete").str.split(":").list.get(1).cast(pl.Int64))
        .alias("time_to_complete_minutes")
    ).filter(pl.col("time_to_complete_minutes") >= 7).drop("time_to_complete_minutes")

    # Filter out records with low variance in rating questions
    df = df.with_columns(
        pl.concat_list([pl.col(col) for col in _RATING_COLS]).list.std().alias("_ratings_std")
    ).filter(pl.col("_ratings_std") >= 0.2).drop("_ratings_std")

    # Filter out records that responded 'No' to 'Did you find this assessment easy to understand?'
    df = df.filter(pl.col("understanding") != "No")

    # Filter out countries with fewer than 1,000 responses
    country_counts = df.group_by("country").len().filter(pl.col("len") >= 1000).select("country")
    df = df.join(country_counts, on="country", how="semi")

    return df