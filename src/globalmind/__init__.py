# SPDX-FileCopyrightText: 2026-present Nianyu Su <mirakelor@outlook.com>
#
# SPDX-License-Identifier: MIT

"""GlobalMind: GMP (Global Mind Project) data analysis toolkit."""

from globalmind.data import read_table, clean_data
from globalmind.schema import COLUMN_DESCRIPTIONS, describe_column
from globalmind.symptom import identify_symptoms, mapping_to_DSM5
from globalmind.stratification import iterative_proportional_fitting, simple_stratification
from globalmind.__about__ import __version__

__all__ = [
    "read_table",
    "clean_data",
    "COLUMN_DESCRIPTIONS",
    "describe_column",
    "identify_symptoms",
    "mapping_to_DSM5",
    "iterative_proportional_fitting",
    "simple_stratification",
    "__version__",
]