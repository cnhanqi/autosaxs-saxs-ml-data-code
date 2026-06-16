from __future__ import annotations

from collections.abc import Mapping


def build_feature_row(
    *,
    manifest_row: Mapping[str, object],
    guinier_result: Mapping[str, object] | None = None,
    crystallinity_result: Mapping[str, object] | None = None,
    oligomer_result: Mapping[str, object] | None = None,
    gate_result: Mapping[str, object] | None = None,
) -> dict[str, object]:
    """Merge manifest and analysis outputs into one canonical feature row."""
    guinier_result = dict(guinier_result or {})
    crystallinity_result = dict(crystallinity_result or {})
    oligomer_result = dict(oligomer_result or {})
    gate_result = dict(gate_result or {})

    return {
        "sample_id": manifest_row.get("sample_id"),
        "ean_wt_pct": manifest_row.get("ean_wt_pct"),
        "protein_mg_ml": manifest_row.get("protein_mg_ml"),
        "rg": guinier_result.get("rg"),
        "rg_kind": guinier_result.get("rg_kind", "pseudo"),
        "i0": guinier_result.get("i0"),
        "ci": crystallinity_result.get("ci"),
        "peak_detected": crystallinity_result.get("peak_detected"),
        "q_peak": crystallinity_result.get("q_peak"),
        "d_spacing": crystallinity_result.get("d_spacing"),
        "oligomer_chi2": oligomer_result.get("chi2"),
        "oligomer_state": oligomer_result.get("dominant_state"),
        "label_crystal": manifest_row.get("label_crystal"),
        "analysis_status": gate_result.get("analysis_status"),
        "warnings": ";".join(gate_result.get("warnings", [])),
    }
