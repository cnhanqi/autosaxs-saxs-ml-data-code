from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field


@dataclass(frozen=True)
class SampleGateResult:
    sample_id: str
    analysis_status: str
    step_status: dict[str, str]
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class SampleGate:
    """Route a sample through the pipeline without hiding skip reasons."""

    def __init__(self, rules: Mapping[str, object] | None = None) -> None:
        self.rules = dict(rules or {})

    def evaluate(
        self,
        *,
        manifest_row: Mapping[str, object],
        qc_metrics: Mapping[str, object] | None = None,
    ) -> SampleGateResult:
        qc_metrics = dict(qc_metrics or {})
        sample_id = str(manifest_row.get("sample_id", "unknown"))
        reasons: list[str] = []
        warnings: list[str] = []

        step_status = {
            "guinier": "run",
            "crystallinity": "run",
            "bragg": "run",
            "oligomer": "run",
            "ml": "run",
        }

        if not bool(manifest_row.get("include_in_physics", True)):
            step_status["guinier"] = "skip"
            step_status["crystallinity"] = "skip"
            step_status["bragg"] = "skip"
            step_status["oligomer"] = "skip"
            reasons.append("excluded_from_physics_by_manifest")

        if not bool(manifest_row.get("has_low_q_region", True)):
            step_status["guinier"] = "skip"
            reasons.append("missing_low_q_region")

        if not bool(manifest_row.get("has_bragg_peak", True)):
            step_status["crystallinity"] = "skip"
            step_status["bragg"] = "skip"
            warnings.append("no_bragg_peak_flag")

        if not bool(manifest_row.get("has_pdb_model", False)):
            step_status["oligomer"] = "skip"
            warnings.append("no_pdb_model")

        if not bool(manifest_row.get("include_in_ml", True)):
            step_status["ml"] = "skip"
            reasons.append("excluded_from_ml_by_manifest")

        if qc_metrics.get("atsas_available") is False:
            step_status["oligomer"] = "skip"
            warnings.append("atsas_not_available")

        if qc_metrics.get("guinier_negative_slope") is False:
            step_status["guinier"] = "manual_review"
            warnings.append("guinier_non_negative_slope")

        if qc_metrics.get("low_q_points") is not None:
            min_points = int(
                dict(self.rules.get("guinier", {})).get("require_low_q_points", 8)
            )
            if int(qc_metrics["low_q_points"]) < min_points:
                step_status["guinier"] = "manual_review"
                warnings.append("insufficient_low_q_points")

        if qc_metrics.get("n_real_peaks") is not None:
            min_peaks = int(
                dict(self.rules.get("crystallinity", {})).get("min_real_peaks", 2)
            )
            if int(qc_metrics["n_real_peaks"]) < min_peaks:
                step_status["crystallinity"] = "manual_review"
                step_status["bragg"] = "manual_review"
                warnings.append("insufficient_real_peaks")

        analysis_status = "accepted"
        if reasons:
            analysis_status = "partial"
        if "manual_review" in step_status.values():
            analysis_status = "manual_review"

        return SampleGateResult(
            sample_id=sample_id,
            analysis_status=analysis_status,
            step_status=step_status,
            reasons=reasons,
            warnings=warnings,
        )


def evaluate_sample(
    *,
    manifest_row: Mapping[str, object],
    qc_metrics: Mapping[str, object] | None = None,
    rules: Mapping[str, object] | None = None,
) -> SampleGateResult:
    """Minimal entrypoint for sample-level routing decisions."""
    return SampleGate(rules=rules).evaluate(
        manifest_row=manifest_row,
        qc_metrics=qc_metrics,
    )
