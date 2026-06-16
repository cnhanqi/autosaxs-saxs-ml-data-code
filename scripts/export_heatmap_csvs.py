"""
Export traceable CSVs for the two heatmaps in outputs/.

This script creates:
- raw point tables used to train the heatmaps
- prediction grids behind each heatmap
- CI=0.1 contour vertices
- phase-transition interval summaries derived from CI >= 0.1
- a small inventory linking figures, code, and data sources
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
sys.path.append(str(PROJECT_ROOT))
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / ".mplconfig"))

from src.output_paths import heatmap_csv_dir, heatmap_image_dir
from src.visualization import generate_prediction_grid, train_best_model


X1_RANGE = (0.0, 100.0)
X2_RANGE = (0.0, 100.0)
RESOLUTION = 100
CI_THRESHOLD = 0.1


def _project_paths(bundle_name: str) -> dict[str, Path]:
    data_dir = PROJECT_ROOT / "data"
    outputs_csv_dir = heatmap_csv_dir(PROJECT_ROOT, bundle_name)
    outputs_image_dir = heatmap_image_dir(PROJECT_ROOT, bundle_name)
    return {
        "cleaned_csv": data_dir / "cleaned_data.csv",
        "ml_targets_csv": data_dir / "ML_targets_crystal_oligo v3.csv",
        "ml_targets_xlsx": data_dir / "ML_targets_crystal_oligo v3.xlsx",
        "selected_dir": PROJECT_ROOT / "selected for ML",
        "outputs_csv_dir": outputs_csv_dir,
        "outputs_image_dir": outputs_image_dir,
    }


def _normalize_original_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = out.columns.str.strip()
    rename_map: dict[str, str] = {}
    for col in out.columns:
        if col.startswith("x1") and "EAN" in col:
            rename_map[col] = "x1"
        elif col.startswith("x2") and "Protein" in col:
            rename_map[col] = "x2"
        elif col.startswith("y1") and "Rg" in col:
            rename_map[col] = "y1"
        elif col.startswith("y2") and "crystalline" in col:
            rename_map[col] = "y2"
        elif col == "CI":
            rename_map[col] = "CI"
        elif "R2_w" in col or "weighted R" in col:
            rename_map[col] = "R2_w"
    out = out.rename(columns=rename_map)
    out["x1"] = pd.to_numeric(out["x1"], errors="coerce")
    out["x2"] = pd.to_numeric(out["x2"], errors="coerce")
    out["source_ml_targets_data_row_1based"] = np.arange(1, len(out) + 1)
    return out


def _build_original_row_lookup(original_csv: Path) -> pd.DataFrame:
    original = pd.read_csv(original_csv)
    original = _normalize_original_columns(original)
    keep = ["x1", "x2", "source_ml_targets_data_row_1based"]
    return original[keep].dropna(subset=["x1", "x2"]).drop_duplicates(["x1", "x2"])


def _parse_selected_dat_files(selected_dir: Path) -> pd.DataFrame:
    records: list[dict[str, object]] = []
    for path in sorted(selected_dir.glob("*.dat")):
        stem = path.stem
        if stem.startswith("Buf_"):
            x1 = 0.0
            protein_token = stem.split("_", 1)[1]
        elif stem.startswith("EAN") and "_" in stem:
            prefix, protein_token = stem.split("_", 1)
            x1 = float(prefix.replace("EAN", ""))
        else:
            continue

        protein_token = protein_token.replace("mgb", "").replace("mg", "")
        x2 = float(protein_token)
        records.append(
            {
                "x1": x1,
                "x2": x2,
                "raw_dat_filename": path.name,
                "raw_dat_path": str(path),
            }
        )

    return pd.DataFrame(records).drop_duplicates(["x1", "x2"])


def _build_point_table(df: pd.DataFrame, raw_lookup: pd.DataFrame, row_lookup: pd.DataFrame, paths: dict[str, Path]) -> pd.DataFrame:
    points = df.copy()
    points["point_id"] = np.arange(1, len(points) + 1)
    points = points.merge(row_lookup, on=["x1", "x2"], how="left")
    points = points.merge(raw_lookup, on=["x1", "x2"], how="left")
    points["raw_dat_exists"] = points["raw_dat_path"].notna()
    points["source_cleaned_csv"] = str(paths["cleaned_csv"])
    points["source_ml_targets_csv"] = str(paths["ml_targets_csv"])
    points["source_ml_targets_xlsx"] = str(paths["ml_targets_xlsx"])
    return points


def _export_prediction_grid(df: pd.DataFrame, target_col: str, value_col: str, model_kind: str) -> tuple[pd.DataFrame, np.ndarray, np.ndarray, np.ndarray]:
    model, _data = train_best_model(df, target_col=target_col, model_kind=model_kind)
    x1_grid, x2_grid, pred = generate_prediction_grid(
        model,
        x1_range=X1_RANGE,
        x2_range=X2_RANGE,
        resolution=RESOLUTION,
    )
    grid_df = pd.DataFrame(
        {
            "x1_il_wt_pct": x1_grid.ravel(),
            "x2_protein_mg_ml": x2_grid.ravel(),
            value_col: pred.ravel(),
        }
    )
    return grid_df, x1_grid, x2_grid, pred


def _extract_ci_contour(x1_grid: np.ndarray, x2_grid: np.ndarray, ci_pred: np.ndarray) -> pd.DataFrame:
    fig, ax = plt.subplots()
    cs = ax.contour(x2_grid, x1_grid, ci_pred, levels=[CI_THRESHOLD])
    records: list[dict[str, float | int]] = []
    for contour_id, segment in enumerate(cs.allsegs[0], start=1):
        for vertex_idx, (x2_val, x1_val) in enumerate(segment, start=1):
            records.append(
                {
                    "contour_id": contour_id,
                    "vertex_index": vertex_idx,
                    "x2_protein_mg_ml": float(x2_val),
                    "x1_il_wt_pct": float(x1_val),
                    "threshold_ci": CI_THRESHOLD,
                }
            )
    plt.close(fig)
    return pd.DataFrame(records)


def _summarize_phase_interval(x1_grid: np.ndarray, x2_grid: np.ndarray, ci_pred: np.ndarray) -> tuple[pd.DataFrame, pd.DataFrame]:
    mask = ci_pred >= CI_THRESHOLD

    interval_rows: list[dict[str, float | int]] = []
    region_rows: list[dict[str, float | int]] = []

    for row_idx in range(mask.shape[0]):
        protein = float(x2_grid[row_idx, 0])
        il_values = x1_grid[row_idx, mask[row_idx, :]]
        if il_values.size == 0:
            continue

        interval_rows.append(
            {
                "x2_protein_mg_ml": protein,
                "x1_il_wt_pct_min": float(np.min(il_values)),
                "x1_il_wt_pct_max": float(np.max(il_values)),
                "n_grid_points_in_region": int(il_values.size),
                "criterion": f"predicted_CI >= {CI_THRESHOLD}",
            }
        )

        region_rows.extend(
            {
                "x2_protein_mg_ml": protein,
                "x1_il_wt_pct": float(il),
                "predicted_ci": float(ci_pred[row_idx, col_idx]),
                "criterion": f"predicted_CI >= {CI_THRESHOLD}",
            }
            for col_idx, il in enumerate(x1_grid[row_idx, :])
            if mask[row_idx, col_idx]
        )

    return pd.DataFrame(interval_rows), pd.DataFrame(region_rows)


def _summarize_observed_ci_points(points_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    observed = points_df.loc[points_df["CI"] >= CI_THRESHOLD].copy()
    observed_region = observed[
        [
            "point_id",
            "x1",
            "x2",
            "CI",
            "y1",
            "y2",
            "R2_w",
            "source_ml_targets_data_row_1based",
            "raw_dat_filename",
            "raw_dat_path",
        ]
    ].rename(
        columns={
            "x1": "x1_il_wt_pct",
            "x2": "x2_protein_mg_ml",
            "CI": "ci",
            "y1": "y1_rg_angstrom",
            "y2": "y2_crystalline",
            "R2_w": "r2_w",
        }
    )

    observed_interval = (
        observed.groupby("x2", as_index=False)
        .agg(
            x1_il_wt_pct_min=("x1", "min"),
            x1_il_wt_pct_max=("x1", "max"),
            n_observed_points=("x1", "size"),
        )
        .rename(columns={"x2": "x2_protein_mg_ml"})
    )
    observed_interval["criterion"] = f"observed_CI >= {CI_THRESHOLD}"
    return observed_interval, observed_region


def _build_inventory(paths: dict[str, Path], bundle_name: str, rg_model_kind: str, ci_model_kind: str, include_rg: bool) -> pd.DataFrame:
    records = []
    rg_figure_path = paths["outputs_image_dir"] / "heatmap_y1_rg.png"
    ci_figure_path = paths["outputs_image_dir"] / "heatmap_ci_regression.png"
    ci_generator_script = "scripts/generate_heatmap_ci.py"
    if bundle_name == "default":
        rg_figure_path = heatmap_image_dir(PROJECT_ROOT, "rg") / "heatmap_y1_rg.png"
        ci_figure_path = heatmap_image_dir(PROJECT_ROOT, "ci") / "heatmap_ci_regression.png"
    elif bundle_name == "ci_gb" or str(ci_model_kind).upper() == "GB":
        ci_generator_script = "scripts/generate_heatmap_ci_gb.py"
    if include_rg:
        records.append({
            "bundle_name": bundle_name,
            "figure_output": str(rg_figure_path),
            "generator_script": "scripts/generate_heatmap.py",
            "shared_plot_code": "src/visualization.py",
            "model_kind": rg_model_kind,
            "model_input_csv": str(paths["cleaned_csv"]),
            "upstream_cleaning_script": "scripts/run_analysis.py",
            "upstream_original_table_csv": str(paths["ml_targets_csv"]),
            "upstream_original_table_xlsx": str(paths["ml_targets_xlsx"]),
            "raw_saxs_folder": str(paths["selected_dir"]),
            "note": "Heatmap target is y1 (Rg).",
        })
    records.append({
            "bundle_name": bundle_name,
            "figure_output": str(ci_figure_path),
            "generator_script": ci_generator_script,
            "shared_plot_code": "src/visualization.py",
            "model_kind": ci_model_kind,
            "model_input_csv": str(paths["cleaned_csv"]),
            "upstream_cleaning_script": "scripts/run_analysis.py",
            "upstream_original_table_csv": str(paths["ml_targets_csv"]),
            "upstream_original_table_xlsx": str(paths["ml_targets_xlsx"]),
            "raw_saxs_folder": str(paths["selected_dir"]),
            "note": "Heatmap target is CI, with contour threshold at 0.1.",
        })
    return pd.DataFrame(records)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export traceable heatmap CSV bundles.")
    parser.add_argument("--bundle-name", default="default", help="Output bundle name under outputs/csv/heatmaps and outputs/heatmaps.")
    parser.add_argument("--rg-model-kind", default="auto", help="Model kind for the Rg prediction grid.")
    parser.add_argument("--ci-model-kind", default="auto", help="Model kind for the CI prediction grid.")
    parser.add_argument("--ci-only", action="store_true", help="Export only CI-linked CSV artifacts.")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    paths = _project_paths(args.bundle_name)
    cleaned = pd.read_csv(paths["cleaned_csv"])
    raw_lookup = _parse_selected_dat_files(paths["selected_dir"])
    row_lookup = _build_original_row_lookup(paths["ml_targets_csv"])
    point_table = _build_point_table(cleaned, raw_lookup, row_lookup, paths)

    y1_points = point_table[
        [
            "point_id",
            "x1",
            "x2",
            "y1",
            "y2",
            "CI",
            "R2_w",
            "source_ml_targets_data_row_1based",
            "raw_dat_filename",
            "raw_dat_path",
            "raw_dat_exists",
            "source_cleaned_csv",
            "source_ml_targets_csv",
            "source_ml_targets_xlsx",
        ]
    ].rename(
        columns={
            "x1": "x1_il_wt_pct",
            "x2": "x2_protein_mg_ml",
            "y1": "y1_rg_angstrom",
            "y2": "y2_crystalline",
            "CI": "ci",
            "R2_w": "r2_w",
        }
    )
    ci_points = point_table[
        [
            "point_id",
            "x1",
            "x2",
            "CI",
            "y2",
            "y1",
            "R2_w",
            "source_ml_targets_data_row_1based",
            "raw_dat_filename",
            "raw_dat_path",
            "raw_dat_exists",
            "source_cleaned_csv",
            "source_ml_targets_csv",
            "source_ml_targets_xlsx",
        ]
    ].rename(
        columns={
            "x1": "x1_il_wt_pct",
            "x2": "x2_protein_mg_ml",
            "CI": "ci",
            "y2": "y2_crystalline",
            "y1": "y1_rg_angstrom",
            "R2_w": "r2_w",
        }
    )

    if not args.ci_only:
        y1_grid_df, _x1_grid_y1, _x2_grid_y1, _y1_pred = _export_prediction_grid(
            cleaned,
            target_col="y1",
            value_col="predicted_y1_rg_angstrom",
            model_kind=args.rg_model_kind,
        )
    ci_grid_df, x1_grid_ci, x2_grid_ci, ci_pred = _export_prediction_grid(
        cleaned,
        target_col="CI",
        value_col="predicted_ci",
        model_kind=args.ci_model_kind,
    )

    contour_df = _extract_ci_contour(x1_grid_ci, x2_grid_ci, ci_pred)
    interval_df, region_df = _summarize_phase_interval(x1_grid_ci, x2_grid_ci, ci_pred)
    observed_interval_df, observed_region_df = _summarize_observed_ci_points(point_table)
    inventory_df = _build_inventory(paths, args.bundle_name, args.rg_model_kind, args.ci_model_kind, include_rg=not args.ci_only)

    out_dir = paths["outputs_csv_dir"]
    ci_points.to_csv(out_dir / "heatmap_ci_regression_points.csv", index=False)
    ci_grid_df.to_csv(out_dir / "heatmap_ci_regression_prediction_grid.csv", index=False)
    contour_df.to_csv(out_dir / "heatmap_ci_regression_contour_threshold_0p1.csv", index=False)
    interval_df.to_csv(out_dir / "phase_transition_interval_ci_ge_0p1.csv", index=False)
    region_df.to_csv(out_dir / "phase_transition_region_ci_ge_0p1_grid_points.csv", index=False)
    observed_interval_df.to_csv(out_dir / "phase_transition_interval_observed_ci_ge_0p1.csv", index=False)
    observed_region_df.to_csv(out_dir / "phase_transition_observed_points_ci_ge_0p1.csv", index=False)
    inventory_df.to_csv(out_dir / "heatmap_source_inventory.csv", index=False)
    if not args.ci_only:
        y1_points.to_csv(out_dir / "heatmap_y1_rg_points.csv", index=False)
        y1_grid_df.to_csv(out_dir / "heatmap_y1_rg_prediction_grid.csv", index=False)

    print(f"CSV exports written to: {out_dir}")
    for path in sorted(out_dir.glob("*.csv")):
        print(f" - {path.name}")


if __name__ == "__main__":
    main()
