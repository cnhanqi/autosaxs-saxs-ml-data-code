from __future__ import annotations

import numpy as np

from saxs_crystal.physics.bragg import detect_bragg_peaks


def estimate_crystallinity(
    q: np.ndarray,
    intensity: np.ndarray,
    *,
    q_min: float = 0.02,
    q_max: float = 0.35,
    smooth_sigma: float = 2.0,
    prominence_threshold: float = 0.05,
) -> dict[str, float]:
    """Estimate crystallinity index and basic Bragg summary values."""
    mask = (q >= q_min) & (q <= q_max) & np.isfinite(intensity)
    q_sub = q[mask]
    i_sub = intensity[mask]

    if q_sub.size < 10:
        return {
            "ci": 0.0,
            "total_area": 0.0,
            "crystalline_area": 0.0,
            "peak_detected": 0.0,
            "num_peaks": 0.0,
            "q_peak": float("nan"),
            "d_spacing": float("nan"),
        }

    try:
        from scipy.ndimage import gaussian_filter1d, minimum_filter
    except ImportError:
        baseline = np.minimum.accumulate(i_sub)
    else:
        dq = float(np.mean(np.diff(q_sub)))
        window_pts = max(5, int(0.05 / dq)) if dq > 0 else 5
        baseline = minimum_filter(i_sub, size=window_pts)
        baseline = gaussian_filter1d(baseline, sigma=smooth_sigma)
        baseline = np.minimum(i_sub, baseline)

    total_area = float(np.trapz(i_sub, q_sub))
    amorphous_area = float(np.trapz(baseline, q_sub))
    crystalline_area = max(total_area - amorphous_area, 0.0)
    ci = crystalline_area / total_area if total_area > 0 else 0.0

    residual = i_sub - baseline
    peak_summary = detect_bragg_peaks(
        q_sub,
        residual,
        prominence_threshold=prominence_threshold,
    )

    return {
        "ci": float(ci),
        "total_area": total_area,
        "crystalline_area": crystalline_area,
        **peak_summary,
    }
