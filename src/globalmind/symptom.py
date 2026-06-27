import polars as pl

# 20 Problem items — clinical threshold ≥8
_PROBLEM_COLS = [
    "restless_hyperactive",          # Restlessness & Hyperactivity
    "fear_anxiety",                  # Fear & Anxiety
    "infections",                    # Susceptibility to Infections
    "aggression",                    # Aggression Towards Others
    "avoidance",                     # Avoidance & Withdrawal
    "obsessive_thoughts",            # Unwanted, Strange or Obsessive Thoughts
    "mood_swings",                   # Mood Swings
    "detached_reality",              # Sense of being detached from reality
    "nightmares",                    # Nightmares
    "addictions",                    # Addictions
    "anger",                         # Anger & Irritability
    "suicidal_thoughts",             # Suicidal Thoughts or Intentions
    "pain",                          # Experience of Pain
    "guilt_blame",                   # Guilt & Blame
    "hallucinations",                # Hallucinations
    "flashblacks",                   # Traumatic Flashbacks
    "repetitive_actions",            # Repetitive or Compulsive Actions
    "sad_hopeless",                  # Feelings of Sadness, Distress or Hopelessness
    "physical_health",               # Physical Health Issues
    "confusion",                     # Confusion or Slowed Thinking
]

# 27 Spectrum items — clinical threshold ≤1
_SPECTRUM_COLS = [
    "adapt_to_change",               # Adaptability to Change
    "self_worth_confidence",         # Self Worth & Confidence
    "creativity_problem_solving",    # Creativity & Problem Solving
    "drive_motivation",              # Drive & Motivation
    "stability_calmness",            # Stability & Calmness
    "sleep_quality",                 # Sleep Quality
    "self_control_impulsivity",      # Self Control & Impulsivity
    "ability_learn",                 # Ability to Learn
    "coordination",                  # Coordination
    "relationships",                 # Relationships with others
    "emotional_resilience",          # Emotional Resilience
    "planning_organization",         # Planning & Organisation
    "physical_intimacy",             # Physical Intimacy
    "speech_language",               # Speech & Language
    "memory",                        # Memory
    "social_cooperation",            # Social interactions & Cooperation
    "decision_risk",                 # Decision-making & Risk-taking
    "curiosity_enthusiasm",          # Curiosity, Interest & Enthusiasm
    "energy",                        # Energy Level
    "emotional_control",             # Emotional Control
    "focus_concentration",           # Focus & Concentration
    "appetite_regulation",           # Appetite Regulation
    "empathy",                       # Empathy
    "sensory_sensitivity",           # Sensory Sensitivity
    "self_image",                    # Self-Image
    "outlook_optimism",              # Outlook & Optimism
    "selective_attention",           # Selective Attention
]

# DSM‑5 mapping rules
_SYM = "_symptom"

_DSM5_RULES: dict[str, dict] = {
    "DSM5_depression": {
        "core_groups": [0, 1], "min_groups": 5,
        "groups": [
            [f"drive_motivation{_SYM}", f"curiosity_enthusiasm{_SYM}"],
            [f"sad_hopeless{_SYM}", f"outlook_optimism{_SYM}"],
            [f"appetite_regulation{_SYM}"], [f"confusion{_SYM}"], [f"energy{_SYM}"],
            [f"self_worth_confidence{_SYM}", f"self_image{_SYM}", f"guilt_blame{_SYM}"],
            [f"focus_concentration{_SYM}", f"selective_attention{_SYM}", f"decision_risk{_SYM}"],
            [f"suicidal_thoughts{_SYM}"],
        ],
    },
    "DSM5_anxiety": {
        "required": [f"fear_anxiety{_SYM}"], "required_groups": [0], "min_groups": 3,
        "groups": [
            [f"stability_calmness{_SYM}", f"emotional_control{_SYM}"],
            [f"restless_hyperactive{_SYM}"], [f"energy{_SYM}"],
            [f"focus_concentration{_SYM}", f"selective_attention{_SYM}"],
            [f"anger{_SYM}"], [f"pain{_SYM}"], [f"sleep_quality{_SYM}"], [f"avoidance{_SYM}"],
        ],
    },
    "DSM5_bipolar": {
        "required": [f"mood_swings{_SYM}"], "core_groups": [0, 1], "min_groups": 5,
        "groups": [
            [f"drive_motivation{_SYM}", f"curiosity_enthusiasm{_SYM}"],
            [f"sad_hopeless{_SYM}", f"outlook_optimism{_SYM}"],
            [f"appetite_regulation{_SYM}"], [f"confusion{_SYM}"], [f"energy{_SYM}"],
            [f"self_worth_confidence{_SYM}", f"self_image{_SYM}", f"guilt_blame{_SYM}"],
            [f"focus_concentration{_SYM}", f"selective_attention{_SYM}", f"decision_risk{_SYM}"],
            [f"suicidal_thoughts{_SYM}"],
        ],
    },
    "DSM5_ptsd": {
        "trauma_required": True, "core_groups": [0],
        "required": [f"avoidance{_SYM}"], "min_groups": 2,
        "groups": [
            [f"flashblacks{_SYM}", f"nightmares{_SYM}", f"obsessive_thoughts{_SYM}"],
            [f"memory{_SYM}"],
            [f"self_worth_confidence{_SYM}", f"self_image{_SYM}", f"outlook_optimism{_SYM}"],
            [f"guilt_blame{_SYM}"], [f"sad_hopeless{_SYM}"],
            [f"curiosity_enthusiasm{_SYM}", f"drive_motivation{_SYM}"],
            [f"relationships{_SYM}"],
        ],
    },
    "DSM5_ocd": {
        "required": [f"obsessive_thoughts{_SYM}", f"repetitive_actions{_SYM}", f"fear_anxiety{_SYM}"],
        "min_groups": 1,
        "groups": [
            [f"stability_calmness{_SYM}"], [f"self_control_impulsivity{_SYM}"],
            [f"emotional_control{_SYM}"],
        ],
    },
    "DSM5_schizophrenia": {
        "required": [f"obsessive_thoughts{_SYM}", f"hallucinations{_SYM}"], "min_groups": 1,
        "groups": [
            [f"speech_language{_SYM}"], [f"repetitive_actions{_SYM}"],
            [f"drive_motivation{_SYM}", f"relationships{_SYM}",
             f"social_cooperation{_SYM}", f"curiosity_enthusiasm{_SYM}"],
        ],
    },
    "DSM5_eating": {
        "required": [f"appetite_regulation{_SYM}", f"fear_anxiety{_SYM}", f"self_image{_SYM}"],
        "groups": [],
    },
    "DSM5_addiction": {
        "required": [f"addictions{_SYM}"], "min_groups": 2,
        "groups": [
            [f"decision_risk{_SYM}"], [f"emotional_control{_SYM}"], [f"avoidance{_SYM}"],
            [f"relationships{_SYM}"], [f"self_control_impulsivity{_SYM}"],
        ],
    },
    "DSM5_adhd": {
        "min_groups": 4,
        "groups": [
            [f"focus_concentration{_SYM}"], [f"selective_attention{_SYM}"],
            [f"drive_motivation{_SYM}"], [f"planning_organization{_SYM}"], [f"memory{_SYM}"],
        ],
    },
    "DSM5_asd": {
        "min_groups": 3,
        "groups": [
            [f"social_cooperation{_SYM}"], [f"relationships{_SYM}"],
            [f"repetitive_actions{_SYM}"], [f"adapt_to_change{_SYM}"],
            [f"sensory_sensitivity{_SYM}"],
            [f"selective_attention{_SYM}", f"focus_concentration{_SYM}"],
        ],
    },
}

def _group_flags(df: pl.LazyFrame, groups: list[list[str]]) -> list[pl.Expr]:
    """Return one boolean expression per group (True if any symptom in group is True)."""
    return [
        pl.any_horizontal(
            [
                pl.col(c).fill_null(False)
                for c in grp
            ]
        )
        for grp in groups
    ]

def identify_symptoms(df: pl.LazyFrame) -> pl.LazyFrame:
    """Identify symptoms based on clinical thresholds for problem and spectrum items.
    Args:
        df (pl.LazyFrame): Input Polars LazyFrame containing the data.
    Returns:
        pl.LazyFrame: A new Polars LazyFrame with additional columns indicating the presence of symptoms.
    """
    # Identify problem symptoms (clinical threshold ≥8)
    for col in _PROBLEM_COLS:
        df = df.with_columns(
            (pl.col(col) >= 8).alias(f"{col}_symptom")
        )

    # Identify spectrum symptoms (clinical threshold ≤1)
    for col in _SPECTRUM_COLS:
        df = df.with_columns(
            (pl.col(col) <= 1).alias(f"{col}_symptom")
        )
    
    df = df.with_columns(
        pl.sum_horizontal(
            [pl.col(f"{c}_symptom") for c in _PROBLEM_COLS + _SPECTRUM_COLS]
        ).alias("symptom_count")
    )

    return df

def mapping_to_DSM5(df: pl.LazyFrame) -> pl.LazyFrame:
    """Map the identified symptoms to DSM-5 categories.
    Args:
        df (pl.LazyFrame): Input Polars LazyFrame containing the data with symptom indicators.
    Returns:
        pl.LazyFrame: A new Polars LazyFrame with additional columns indicating DSM-5 categories.
    """

    # Pre‑compute a "has trauma" flag for PTSD
    df = df.with_columns(
        pl.when(
            pl.col("trauma_childhood").list.len() > 0
            & ~pl.col("trauma_childhood").list.contains(
                "I did not experience any of the above during my childhood"
            )
        )
        .then(True)
        .when(
            pl.col("trauma_adulthood").list.len() > 0
            & ~pl.col("trauma_adulthood").list.contains(
                "I did not experience any of the above"
            )
        )
        .then(True)
        .otherwise(False)
        .alias("_has_trauma")
    )

    for label, rule in _DSM5_RULES.items():
        g = _group_flags(df, rule["groups"])
        ok = pl.lit(True)

        # Required single columns (ALL must be True)
        for c in rule.get("required", []):
            ok = ok & pl.col(c).fill_null(False)

        # Required groups (each must be True)
        for gi in rule.get("required_groups", []):
            ok = ok & g[gi]

        # Core group check (≥1 of this set must be True)
        if "core_groups" in rule:
            ok = ok & pl.any_horizontal([g[i] for i in rule["core_groups"]])

        # Min total groups check
        if rule.get("min_groups"):
            total = pl.sum_horizontal([*g])
            ok = ok & (total >= rule["min_groups"])

        # Special: trauma flag
        if rule.get("trauma_required"):
            ok = ok & pl.col("_has_trauma")

        df = df.with_columns(ok.alias(label))

    return df.drop("_has_trauma")