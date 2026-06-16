"""
Centralised path helpers for the ML project.

Design:
  - project_root()          鈫?repo root (folder containing this constants/ pkg)
  - data_raw() / data_processed()  鈫?standard data layout
  - dataset_dir(name)       鈫?shortcut to a named dataset folder
  - analysis_dir_for(data_dir, tag) 鈫?derive analysis output path from data_dir
  - available_datasets()    鈫?auto-discover datasets with *.dat files
"""
from __future__ import annotations
from pathlib import Path
from typing import Iterable, List


# 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€ core roots 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

def project_root() -> Path:
    """Return ML project root (folder containing this constants package)."""
    return Path(__file__).resolve().parents[1]


def data_raw() -> Path:
    return project_root() / 'data' / 'raw'


def data_processed() -> Path:
    return project_root() / 'data' / 'processed'


def processed_intermediate() -> Path:
    return data_processed() / 'intermediate'


def processed_final() -> Path:
    return data_processed() / 'final'


# 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€ dataset helpers 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

# Known dataset folder names at project root level.
# Order matters: first match wins for auto-discovery in choose_existing.
KNOWN_DATASET_NAMES = [
    'selected_for_ML', # representative public SAXS profiles
    '4crys',        # crystal aggregation
    '3sol',         # solution scattering
    '1TemConc',     # temperature-concentration
    '2TemCapHeat',  # temperature-heat capacity
    '5EANConcOld',  # legacy EAN concentration
    'EANConc',      # EAN concentration (new)
    '6',            # dataset 6
]


def dataset_dir(name: str) -> Path:
    """Return full path to a named dataset folder at project root."""
    return project_root() / name


def available_datasets() -> List[str]:
    """Auto-discover dataset folders that exist and contain *.dat files."""
    found = []
    root = project_root()
    for name in KNOWN_DATASET_NAMES:
        d = root / name
        if d.is_dir() and list(d.glob('*.dat')):
            found.append(name)
    return found


def pdb_dir() -> Path:
    """Return PDB directory (shared across all datasets)."""
    candidates = [
        project_root() / 'oligomer_basis',
        project_root() / '0PDB',
        project_root() / '6' / 'PDB',
    ]
    return choose_existing(candidates) or (project_root() / '0PDB')


def analysis_dir_for(data_dir: Path, tag: str = 'analysis') -> Path:
    """
    Derive the analysis output path from the data directory.

    Strategy:
      1. Use  data/processed/intermediate/<dataset_name>/<tag>
         (keeps source data read-only, outputs in a clean tree)
      2. Fallback: <data_dir>/<tag>  (legacy in-place behaviour)

    Parameters
    ----------
    data_dir : Path
        The raw data directory (e.g. project_root() / '4crys').
    tag : str
        Sub-folder name inside the output dir, e.g. 'analysis', 'analysis4'.
        Default is 'analysis'.
    """
    dataset_name = data_dir.name       # e.g. '4crys', 'EANConc'
    preferred = processed_intermediate() / dataset_name / tag
    # Always use the processed tree 鈥?create if needed
    return preferred


# 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€ utilities 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

def choose_existing(paths: Iterable[Path]) -> Path | None:
    """Return the first path that exists, or None."""
    for p in paths:
        if p and Path(p).exists():
            return Path(p)
    return None

