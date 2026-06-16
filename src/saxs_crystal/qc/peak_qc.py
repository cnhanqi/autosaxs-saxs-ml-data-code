from __future__ import annotations

from collections.abc import Mapping


def evaluate_peak_qc(
    n_real_peaks: int,
    peak_prominence_max: float | None = None,
    *,
    rules: Mapping[str, object] | None = None,
) -> dict[str, object]:
    """Decide whether crystallinity and Bragg analysis should proceed."""
    rules = dict(rules or {})
    min_real_peaks = int(rules.get("min_real_peaks", 2))
    prominence_threshold = float(rules.get("peak_prominence_threshold", 0.05))

    reasons: list[str] = []
    if n_real_peaks < min_real_peaks:
        reasons.append("insufficient_real_peaks")
    if peak_prominence_max is not None and peak_prominence_max < prominence_threshold:
        reasons.append("peak_prominence_below_threshold")

    return {
        "run": not reasons,
        "reasons": reasons,
    }
