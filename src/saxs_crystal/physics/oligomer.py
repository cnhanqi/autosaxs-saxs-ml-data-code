from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class OligomerJob:
    sample_id: str
    input_dat: Path
    form_factor_dat: Path
    s_min: float = 0.01
    s_max: float = 0.30


@dataclass(frozen=True)
class OligomerResult:
    sample_id: str
    chi2: float | None = None
    fit_class: str | None = None
    dominant_state: str | None = None


def build_oligomer_command(job: OligomerJob, oligomer_exe: str | Path) -> list[str]:
    """Build a deterministic OLIGOMER command without executing it."""
    return [
        str(oligomer_exe),
        str(job.input_dat),
        str(job.form_factor_dat),
        f"/smin={job.s_min}",
        f"/smax={job.s_max}",
    ]
