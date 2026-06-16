"""
Helpers for keeping output artifacts in typed subfolders.
"""

from __future__ import annotations

from pathlib import Path


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def output_root(project_root: str | Path) -> Path:
    return ensure_dir(Path(project_root) / "outputs")


def output_dir(project_root: str | Path, *parts: str) -> Path:
    return ensure_dir(output_root(project_root).joinpath(*parts))


def output_file(project_root: str | Path, *parts: str) -> Path:
    if len(parts) < 1:
        raise ValueError("output_file requires at least one path part")
    directory = output_dir(project_root, *parts[:-1]) if len(parts) > 1 else output_root(project_root)
    return directory / parts[-1]


def heatmap_image_dir(project_root: str | Path, bundle: str) -> Path:
    return output_dir(project_root, "heatmaps", bundle)


def heatmap_csv_dir(project_root: str | Path, bundle: str) -> Path:
    return output_dir(project_root, "csv", "heatmaps", bundle)
