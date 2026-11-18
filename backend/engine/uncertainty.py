"""Data-completeness and uncertainty gate."""

from __future__ import annotations

from typing import Any

from engine.constants import SPARSE_EHR_MONTHS


def assess_uncertainty(row: dict[str, Any]) -> dict[str, str]:
    """
    IF ehr_months_history < 6 AND no consented genomic tier
    THEN HIGH uncertainty → Baseline Wellness Onboarding.
    """
    ehr_months = int(float(row.get("ehr_months_history") or 0))
    genomic = row.get("consented_genomic_tier")
    sparse_genomic = genomic in (None, "", "none", "null")

    if ehr_months < SPARSE_EHR_MONTHS and sparse_genomic:
        return {
            "uncertainty": "HIGH",
            "confidence_badge": "Low Confidence / Sparse Record (Trigger Baseline Intake)",
            "force_pathway": "Baseline Wellness Onboarding",
        }

    if ehr_months >= 24 and (not sparse_genomic or ehr_months >= 36):
        badge = f"High Confidence ({ehr_months} months longitudinal EHR"
        if not sparse_genomic:
            badge += " + consented genomic report"
        badge += ")"
        return {
            "uncertainty": "LOW",
            "confidence_badge": badge,
            "force_pathway": "",
        }

    return {
        "uncertainty": "MEDIUM",
        "confidence_badge": f"Medium Confidence ({ehr_months} months longitudinal EHR)",
        "force_pathway": "",
    }
