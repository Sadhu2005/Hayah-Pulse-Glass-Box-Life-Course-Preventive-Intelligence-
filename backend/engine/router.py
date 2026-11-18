"""Guideline-constrained pathway router."""

from __future__ import annotations

from typing import Any


def route_pathway(
    row: dict[str, Any],
    *,
    uncertainty: dict[str, str],
    rule_hits: list[dict[str, str]],
    risk_tier: str,
) -> dict[str, str]:
    if uncertainty.get("force_pathway"):
        return {
            "pathway": "Baseline Wellness Onboarding",
            "pathway_recommendation": "Baseline Wellness Onboarding (Sparse Record)",
            "risk_tier": "baseline_onboarding",
        }

    age = int(float(row.get("age") or 0))
    genomic = row.get("consented_genomic_tier")
    rule_ids = {h["id"] for h in rule_hits}

    if genomic == "actionable" and uncertainty.get("uncertainty") != "HIGH":
        return {
            "pathway": "Targeted Genetic / Specialist Counselling",
            "pathway_recommendation": "Targeted Genetic Counselling + Pathway-Aligned Screen",
            "risk_tier": risk_tier,
        }

    if age < 18:
        rec = "Well-Child Visit + Developmental Review"
        if "WC_OVERDUE_30" in rule_ids or "PED_GROWTH_DRIFT" in rule_ids:
            rec = "18-Month Well-Child + Targeted Speech/Developmental Screen"
        return {
            "pathway": "Well-Child & Developmental",
            "pathway_recommendation": rec,
            "risk_tier": risk_tier,
        }

    rec = "IFHAS Adult Comprehensive Screening"
    if "HBA1C_UP" in rule_ids or "FHX_PRESENT" in rule_ids or risk_tier == "high":
        rec = "Priority IFHAS Cardiometabolic + Early HbA1c Panel"
    return {
        "pathway": "IFHAS Adult Comprehensive",
        "pathway_recommendation": rec,
        "risk_tier": risk_tier,
    }
