from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass(frozen=True)
class InputValidationReport:
    is_valid: bool
    n_points: int
    issues: list[str] = field(default_factory=list)


def validate_saxs_arrays(
    q: np.ndarray,
    intensity: np.ndarray,
    error: np.ndarray | None = None,
) -> InputValidationReport:
    """Validate basic SAXS input assumptions before QC or physics analysis."""
    issues: list[str] = []

    if q.size == 0 or intensity.size == 0:
        issues.append("empty_input")

    if q.size != intensity.size:
        issues.append("length_mismatch")

    if error is not None and error.size not in (0, q.size):
        issues.append("error_length_mismatch")

    if q.size > 1 and np.any(np.diff(q) <= 0):
        issues.append("q_not_strictly_increasing")

    if np.any(~np.isfinite(q)) or np.any(~np.isfinite(intensity)):
        issues.append("non_finite_values")

    return InputValidationReport(
        is_valid=not issues,
        n_points=int(q.size),
        issues=issues,
    )
