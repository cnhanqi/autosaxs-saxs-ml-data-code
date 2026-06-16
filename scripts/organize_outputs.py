"""
Reorganize legacy files in outputs/ into typed subfolders.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS = PROJECT_ROOT / "outputs"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def _target_for_root_file(path: Path) -> Path | None:
    name = path.name
    suffix = path.suffix.lower()

    if name == "README.md":
        return None
    if name.startswith("advanced_"):
        bucket = "figures" if suffix == ".png" else "reports"
        return OUTPUTS / "advanced" / bucket / name
    if name.startswith("analysis_"):
        return OUTPUTS / "analysis" / "figures" / name
    if name.startswith("extended_"):
        bucket = "figures" if suffix == ".png" else "reports"
        return OUTPUTS / "extended" / bucket / name
    if name.startswith("heatmap_y1_rg"):
        return OUTPUTS / "heatmaps" / "rg" / name
    if name.startswith("heatmap_ci_regression"):
        return OUTPUTS / "heatmaps" / "ci" / name
    if name.startswith("calibration_"):
        return OUTPUTS / "calibration" / name
    if name.startswith("shap_"):
        return OUTPUTS / "shap" / name
    if name == "workflow_figure.json":
        return OUTPUTS / "workflow" / name
    if suffix == ".txt":
        return OUTPUTS / "reports" / name
    return None


def _move_if_needed(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() == target.resolve():
        return
    if target.exists():
        return
    shutil.move(str(source), str(target))


def main() -> None:
    moved: list[tuple[Path, Path]] = []

    for path in OUTPUTS.iterdir():
        if path.is_file():
            target = _target_for_root_file(path)
            if target is not None:
                _move_if_needed(path, target)
                moved.append((path, target))

    csv_root = OUTPUTS / "csv"
    default_csv_dir = csv_root / "heatmaps" / "default"
    default_csv_dir.mkdir(parents=True, exist_ok=True)
    for path in csv_root.iterdir():
        if path.is_file() and path.suffix.lower() == ".csv":
            target = default_csv_dir / path.name
            _move_if_needed(path, target)
            moved.append((path, target))

    print("Moved files:")
    for source, target in moved:
        try:
            print(f" - {source.relative_to(OUTPUTS)} -> {target.relative_to(OUTPUTS)}")
        except Exception:
            print(f" - {source.name} -> {target.name}")


if __name__ == "__main__":
    main()
