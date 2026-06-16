from __future__ import annotations

from pathlib import Path

import numpy as np


def read_dat(file_path: str | Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Read a 2- or 3-column SAXS .dat file into q, intensity, and error arrays."""
    path = Path(file_path)
    q_list: list[float] = []
    intensity_list: list[float] = []
    error_list: list[float] = []

    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line[0] in "#!%;":
                continue

            parts = line.split()
            if len(parts) < 2:
                continue

            try:
                q_value = float(parts[0])
                intensity_value = float(parts[1])
                error_value = float(parts[2]) if len(parts) > 2 else 0.0
            except ValueError:
                continue

            q_list.append(q_value)
            intensity_list.append(intensity_value)
            error_list.append(error_value)

    return np.asarray(q_list), np.asarray(intensity_list), np.asarray(error_list)
