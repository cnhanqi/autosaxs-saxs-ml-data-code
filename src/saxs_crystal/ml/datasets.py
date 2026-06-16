from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_feature_table(path: str | Path) -> pd.DataFrame:
    """Load the canonical processed feature table."""
    return pd.read_csv(path)
