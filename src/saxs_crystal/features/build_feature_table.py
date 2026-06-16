from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


def build_feature_table(rows: Iterable[dict[str, object]]) -> pd.DataFrame:
    """Build a canonical feature table from feature-row dictionaries."""
    return pd.DataFrame(list(rows))
