# SPDX-FileCopyrightText: 2026-present Nianyu Su <mirakelor@outlook.com>
#
# SPDX-License-Identifier: MIT

"""GlobalMind: GMP (Global Mind Project) data analysis toolkit."""

from globalmind.data import read_table, clean_data
from globalmind.schema import COLUMN_DESCRIPTIONS, describe_column
from globalmind.symptom import identify_symptoms, mapping_to_DSM5
from globalmind.stratification import post_stratification_weighting
from globalmind.__about__ import __version__

__all__ = [
    "read_table",
    "clean_data",
    "COLUMN_DESCRIPTIONS",
    "describe_column",
    "identify_symptoms",
    "mapping_to_DSM5",
    "post_stratification_weighting",
    "__version__",
]