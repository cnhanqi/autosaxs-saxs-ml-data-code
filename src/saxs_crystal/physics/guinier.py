from __future__ import annotations

import numpy as np


def fit_guinier(
    q: np.ndarray,
    intensity: np.ndarray,
    *,
    q_min: float = 0.02,
    q_max: float = 0.05,
) -> dict[str, float]:
    """Fit a simple fixed-window Guinier line and return pseudo-Rg metrics."""
    mask = (q >= q_min) & (q <= q_max) & (intensity > 0)
    q_sel = q[mask]
    i_sel = intensity[mask]

    if q_sel.size < 5:
        return {
            "rg": float("nan"),
            "i0": float("nan"),
            "fit_slope": float("nan"),
            "r_squared": 0.0,
            "points_used": float(q_sel.size),
        }

    x = q_sel**2
    y = np.log(i_sel)
    design = np.vstack([x, np.ones_like(x)]).T
    slope, intercept = np.linalg.lstsq(design, y, rcond=None)[0]

    y_hat = slope * x + intercept
    ss_res = float(np.sum((y - y_hat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r_squared = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
    rg = float(np.sqrt(-3.0 * slope)) if slope < 0 else float("nan")

    return {
        "rg": rg,
        "i0": float(np.exp(intercept)),
        "fit_slope": float(slope),
        "r_squared": float(r_squared),
        "points_used": float(q_sel.size),
    }
