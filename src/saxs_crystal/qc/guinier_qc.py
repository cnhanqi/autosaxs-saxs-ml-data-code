from __future__ import annotations

from collections.abc import Mapping


def evaluate_guinier_qc(
    low_q_points: int,
    slope: float | None,
    weighted_r2: float | None = None,
    *,
    rules: Mapping[str, object] | None = None,
) -> dict[str, object]:
    """Return a lightweight Guinier QC decision payload."""
    rules = dict(rules or {})
    min_points = int(rules.get("require_low_q_points", 8))
    require_negative_slope = bool(rules.get("require_negative_slope", True))
    min_weighted_r2 = rules.get("min_weighted_r2")

    reasons: list[str] = []

    if low_q_points < min_points:
        reasons.append("insufficient_low_q_points")

    if require_negative_slope and (slope is None or slope >= 0):
        reasons.append("non_negative_guinier_slope")

    if min_weighted_r2 is not None and weighted_r2 is not None and weighted_r2 < float(min_weighted_r2):
        reasons.append("weighted_r2_below_threshold")

    return {
        "run": not reasons,
        "reasons": reasons,
    }
