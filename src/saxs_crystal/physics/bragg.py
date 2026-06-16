from __future__ import annotations

import numpy as np


def detect_bragg_peaks(
    q: np.ndarray,
    signal: np.ndarray,
    *,
    prominence_threshold: float = 0.05,
) -> dict[str, float]:
    """Detect simple Bragg peak features from a residual or intensity signal."""
    if q.size < 3 or signal.size < 3:
        return {
            "peak_detected": 0.0,
            "num_peaks": 0.0,
            "q_peak": float("nan"),
            "d_spacing": float("nan"),
        }

    try:
        from scipy.signal import find_peaks
    except ImportError:
        peak_index = int(np.argmax(signal))
        peak_height = float(signal[peak_index])
        if peak_height <= prominence_threshold:
            return {
                "peak_detected": 0.0,
                "num_peaks": 0.0,
                "q_peak": float("nan"),
                "d_spacing": float("nan"),
            }
        q_peak = float(q[peak_index])
        return {
            "peak_detected": 1.0,
            "num_peaks": 1.0,
            "q_peak": q_peak,
            "d_spacing": float((2.0 * np.pi) / q_peak) if q_peak > 0 else float("nan"),
        }

    height_threshold = prominence_threshold * float(np.nanmax(signal))
    peaks, _ = find_peaks(signal, height=height_threshold)
    if len(peaks) == 0:
        return {
            "peak_detected": 0.0,
            "num_peaks": 0.0,
            "q_peak": float("nan"),
            "d_spacing": float("nan"),
        }

    peak_index = int(peaks[0])
    q_peak = float(q[peak_index])
    return {
        "peak_detected": 1.0,
        "num_peaks": float(len(peaks)),
        "q_peak": q_peak,
        "d_spacing": float((2.0 * np.pi) / q_peak) if q_peak > 0 else float("nan"),
    }
