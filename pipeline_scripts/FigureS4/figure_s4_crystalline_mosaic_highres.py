# -*- coding: utf-8 -*-
"""
Figure S4:
High-resolution crystalline peak mosaics rebuilt from selected/*.dat and useful_parameters.csv.

Source dataset:
    data/processed/intermediate/6/analysis/selected

Outputs:
    data/processed/intermediate/6/analysis/selected/analysis/crystalline_present_true/
        crystalline_present_true_mosaic_annot_highres_5col.png
        crystalline_present_true_mosaic_simple_highres_5col.png
"""

from __future__ import annotations

from math import ceil
from pathlib import Path
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data" / "processed" / "intermediate" / "6" / "analysis" / "selected"
ANALYSIS_DIR = DATA_DIR / "analysis"
CRYST_DIR = ANALYSIS_DIR / "crystalline_present_true"
USEFUL_PARAMETERS_CSV = ANALYSIS_DIR / "useful_parameters.csv"

OUTPUT_ANNOT = CRYST_DIR / "crystalline_present_true_mosaic_annot_highres_5col.png"
OUTPUT_SIMPLE = CRYST_DIR / "crystalline_present_true_mosaic_simple_highres_5col.png"

N_COLS = 5
MOSAIC_DPI = 700
PANEL_WIDTH = 4.6
PANEL_HEIGHT = 3.6
Q_HALF_WIDTH = 0.02

TITLE_FONTSIZE = 16
AXIS_LABEL_FONTSIZE = 13
TICK_FONTSIZE = 11
ANNOT_FONTSIZE = 13
GROUP_LABEL_FONTSIZE = 15
LINE_WIDTH = 1.3
MARKER_SIZE = 5
X_TICK_VALUES = [0.09, 0.10, 0.12, 0.13]
X_TICK_LABELS = ["0.09", "0.1", "0.12", "0.13"]

plt.rcParams["font.family"] = "Arial"


_RE_EAN_NUM = re.compile(r"(?:^|[_\-])EAN\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE)
_RE_SOLVENT_BUF = re.compile(r"\bBuf\b", re.IGNORECASE)
_RE_SOLVENT_EAN = re.compile(r"\bEAN\b", re.IGNORECASE)
_RE_MG = re.compile(r"(?:^|[_\-])([0-9]+(?:\.[0-9]+)?)\s*mg\b", re.IGNORECASE)
_RE_TIME = re.compile(r"(?:^|[_\-])([0-9]+(?:\.[0-9]+)?)\s*(min|mins|m|h|hr|hrs|hour|hours|d|day|days)\b", re.IGNORECASE)
_RE_BATCH_B = re.compile(r"(?:^|[_\-])([0-9]+(?:\.[0-9]+)?)mgb\b", re.IGNORECASE)


def _read_dat(path: Path) -> tuple[np.ndarray, np.ndarray]:
    rows = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            text = line.strip()
            if not text or text.startswith(("#", "!", ";")):
                continue
            parts = text.split()
            if len(parts) < 2:
                continue
            try:
                q_val = float(parts[0])
                i_val = float(parts[1])
            except ValueError:
                continue
            rows.append((q_val, i_val))
    if not rows:
        return np.array([]), np.array([])
    arr = np.array(rows, dtype=float)
    return arr[:, 0], arr[:, 1]


def _parse_name_params(stem: str) -> dict[str, object]:
    if _RE_SOLVENT_BUF.search(stem):
        solvent = "Buf"
    elif _RE_SOLVENT_EAN.search(stem):
        solvent = "EAN"
    else:
        solvent = "UNK"

    m_ean = _RE_EAN_NUM.search(stem)
    ean = float(m_ean.group(1)) if m_ean else np.nan

    mg_all = _RE_MG.findall(stem)
    protein_mgml = float(mg_all[-1]) if mg_all else np.nan

    batch_tag = "b" if _RE_BATCH_B.search(stem) else ""

    m_time = _RE_TIME.search(stem)
    if m_time:
        value = float(m_time.group(1))
        unit = m_time.group(2).lower()
        if unit in {"min", "mins", "m"}:
            time_min = value
        elif unit in {"h", "hr", "hrs", "hour", "hours"}:
            time_min = value * 60.0
        elif unit in {"d", "day", "days"}:
            time_min = value * 24.0 * 60.0
        else:
            time_min = np.nan
    else:
        time_min = np.nan

    return {
        "solvent": solvent,
        "EAN": ean,
        "protein_mgml": protein_mgml,
        "batch_tag": batch_tag,
        "time_min": time_min,
    }


def _protein_label(params: dict[str, object]) -> str:
    ean = params.get("EAN", np.nan)
    mg = params.get("protein_mgml", np.nan)
    lines: list[str] = []
    if np.isfinite(ean):
        ean_float = float(ean)
        ean_label = f"{int(round(ean_float))}" if abs(ean_float - round(ean_float)) < 1e-6 else f"{ean_float:g}"
        lines.append(f"EAN {ean_label}wt%")
    if np.isfinite(mg):
        mg_float = float(mg)
        mg_label = f"{int(round(mg_float))}" if abs(mg_float - round(mg_float)) < 1e-6 else f"{mg_float:g}"
        lines.append(f"{mg_label} mg/mL")
    return "\n".join(lines) if lines else "NA"


def _sort_key(item: dict[str, object]) -> tuple:
    params = item["params"]
    mg = params.get("protein_mgml", np.nan)
    mg_key = float(mg) if np.isfinite(mg) else 1e9
    bt = str(params.get("batch_tag", "")).lower()
    bt_key = 1 if bt == "b" else 0
    return (mg_key, bt_key, str(item["stem"]))


def _load_items() -> list[dict[str, object]]:
    if not USEFUL_PARAMETERS_CSV.exists():
        raise FileNotFoundError(f"Missing useful_parameters.csv: {USEFUL_PARAMETERS_CSV}")

    df = pd.read_csv(USEFUL_PARAMETERS_CSV)
    if "crystalline_present" not in df.columns:
        raise ValueError("Column 'crystalline_present' not found in useful_parameters.csv")

    df_true = df[df["crystalline_present"] == True].copy()
    if df_true.empty:
        raise ValueError("No crystalline_present == True rows found.")

    items = []
    for _, row in df_true.iterrows():
        stem = str(row.get("file", "")).strip()
        if not stem:
            continue
        dat_path = DATA_DIR / f"{stem}.dat"
        if not dat_path.exists():
            continue
        params = _parse_name_params(stem)
        items.append(
            {
                "stem": stem,
                "dat_path": dat_path,
                "params": params,
                "peak1_q": pd.to_numeric(row.get("peak1_q", np.nan), errors="coerce"),
                "peak1_fwhm": pd.to_numeric(row.get("peak1_fwhm_Ainv", row.get("peak1_fwhm", np.nan)), errors="coerce"),
                "peak1_binA": pd.to_numeric(row.get("peak1_binA", np.nan), errors="coerce"),
                "peak1_domain_nm_meas": pd.to_numeric(row.get("peak1_domain_nm_meas", np.nan), errors="coerce"),
            }
        )

    if not items:
        raise ValueError("No valid crystalline items with matching .dat files were found.")

    items.sort(key=_sort_key)
    return items


def _shared_xlim(items: list[dict[str, object]]) -> tuple[float, float]:
    qmins = []
    qmaxs = []
    for item in items:
        q1 = item.get("peak1_q", np.nan)
        if np.isfinite(q1):
            qmins.append(float(q1) - Q_HALF_WIDTH)
            qmaxs.append(float(q1) + Q_HALF_WIDTH)
    if qmins:
        return float(min(qmins)), float(max(qmaxs))

    q_arrays = []
    for item in items:
        q, _ = _read_dat(item["dat_path"])
        if q.size:
            q_arrays.append(q)
    all_q = np.concatenate(q_arrays)
    return float(np.nanmin(all_q)), float(np.nanmax(all_q))


def _draw_single_panel(
    ax: plt.Axes,
    item: dict[str, object],
    xlim: tuple[float, float],
    annotated: bool,
    *,
    show_ylabel: bool,
    show_xlabel: bool,
) -> None:
    q, intensity = _read_dat(item["dat_path"])
    q1 = item.get("peak1_q", np.nan)
    fwhm = item.get("peak1_fwhm", np.nan)
    bin_a = item.get("peak1_binA", np.nan)
    domain_nm = item.get("peak1_domain_nm_meas", np.nan)

    mask = (q >= xlim[0]) & (q <= xlim[1])
    q_plot = q[mask] if mask.any() else q
    i_plot = intensity[mask] if mask.any() else intensity

    ax.plot(q_plot, i_plot, "-", lw=LINE_WIDTH, color="#2C7FB8")
    ax.plot(q_plot, i_plot, "o", ms=MARKER_SIZE * 0.35, mec="none", color="#2C7FB8", alpha=0.75)

    if np.isfinite(q1):
        ax.axvline(float(q1), color="#D7301F", alpha=0.9, lw=1.2)
    if np.isfinite(q1) and np.isfinite(fwhm) and float(fwhm) > 0:
        ax.axvspan(float(q1) - 0.5 * float(fwhm), float(q1) + 0.5 * float(fwhm), color="#FB6A4A", alpha=0.18)

    ax.set_xlim(*xlim)
    ax.set_xlabel("q(A-1)" if show_xlabel else "", fontsize=AXIS_LABEL_FONTSIZE)
    ax.set_ylabel("I(q), a.u." if show_ylabel else "", fontsize=AXIS_LABEL_FONTSIZE)
    ax.set_yticks([])
    ax.tick_params(axis="both", labelsize=TICK_FONTSIZE)
    ax.tick_params(axis="y", left=False, labelleft=False)
    ax.set_xticks(X_TICK_VALUES)
    ax.set_xticklabels(X_TICK_LABELS)
    ax.text(
        0.03,
        0.04,
        _protein_label(item["params"]),
        transform=ax.transAxes,
        va="bottom",
        ha="left",
        fontsize=TITLE_FONTSIZE,
    )

    if annotated:
        text_lines = []
        if np.isfinite(q1):
            text_lines.append(f"peak1 q = {float(q1):.4f}")
        if np.isfinite(bin_a):
            text_lines.append(f"bin dq = {float(bin_a):.6f}")
        if np.isfinite(fwhm):
            text_lines.append(f"FWHM = {float(fwhm):.6f}")
        if np.isfinite(domain_nm):
            text_lines.append(f"domain ~ {float(domain_nm):.1f} nm")
        panel_text = "\n".join(text_lines)
    else:
        text_lines = []
        if np.isfinite(q1):
            text_lines.append(f"q1 = {float(q1):.4f}")
        panel_text = "\n".join(text_lines)

    ax.text(
        0.98,
        0.98,
        panel_text,
        transform=ax.transAxes,
        va="top",
        ha="right",
        fontsize=ANNOT_FONTSIZE,
    )


def build_mosaic(items: list[dict[str, object]], out_path: Path, annotated: bool) -> Path:
    n_items = len(items)
    n_rows = int(ceil(n_items / N_COLS))
    fig_w = PANEL_WIDTH * N_COLS
    fig_h = PANEL_HEIGHT * n_rows

    fig, axes = plt.subplots(n_rows, N_COLS, figsize=(fig_w, fig_h), squeeze=False)
    xlim = _shared_xlim(items)

    for idx, item in enumerate(items):
        row = idx // N_COLS
        col = idx % N_COLS
        _draw_single_panel(
            axes[row, col],
            item,
            xlim,
            annotated=annotated,
            show_ylabel=(col == 0),
            show_xlabel=(row == n_rows - 1),
        )

    for idx in range(n_items, n_rows * N_COLS):
        row = idx // N_COLS
        col = idx % N_COLS
        axes[row, col].axis("off")

    fig.subplots_adjust(left=0.05, right=0.99, bottom=0.05, top=0.96, wspace=0.12, hspace=0.18)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=MOSAIC_DPI, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    items = _load_items()
    out_annot = build_mosaic(items, OUTPUT_ANNOT, annotated=True)
    out_simple = build_mosaic(items, OUTPUT_SIMPLE, annotated=False)
    print("FigureS4 high-resolution mosaics written")
    print(f"  Annotated: {out_annot}")
    print(f"  Simple:    {out_simple}")
    print(f"  Items:     {len(items)}")
    print(f"  Layout:    {N_COLS} columns x {ceil(len(items)/N_COLS)} rows")
    print(f"  DPI:       {MOSAIC_DPI}")


if __name__ == "__main__":
    main()
