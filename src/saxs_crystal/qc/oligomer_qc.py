from __future__ import annotations

from collections.abc import Mapping


def evaluate_oligomer_qc(
    *,
    has_pdb_model: bool,
    atsas_available: bool,
    rules: Mapping[str, object] | None = None,
) -> dict[str, object]:
    """Decide whether ATSAS/OLIGOMER work should run for a sample."""
    rules = dict(rules or {})
    require_pdb_model = bool(rules.get("require_pdb_model", True))
    require_atsas = bool(rules.get("require_atsas", True))

    reasons: list[str] = []
    if require_pdb_model and not has_pdb_model:
        reasons.append("missing_pdb_model")
    if require_atsas and not atsas_available:
        reasons.append("atsas_not_available")

    return {
        "run": not reasons,
        "reasons": reasons,
    }
