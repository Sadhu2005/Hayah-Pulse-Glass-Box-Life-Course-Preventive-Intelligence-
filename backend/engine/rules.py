"""Deterministic care-gap and context rules."""

from __future__ import annotations

from typing import Any

from engine.constants import (
    BP_TREND_THRESHOLD,
    GROWTH_DRIFT_THRESHOLD,
    HBA1C_TREND_THRESHOLD,
    IFHAS_OVERDUE_DAYS,
    WELL_CHILD_OVERDUE_DAYS,
)


def _num(row: dict[str, Any], key: str, default: float = 0.0) -> float:
    val = row.get(key)
    if val is None or val == "":
        return default
    try:
        return float(val)
    except (TypeError, ValueError):
        return default


def evaluate_rules(row: dict[str, Any]) -> list[dict[str, str]]:
    """Return fired rules as {id, theme, detail}."""
    hits: list[dict[str, str]] = []
    age = int(_num(row, "age"))
    milestone_overdue = _num(row, "milestone_overdue_days")
    ifhas_overdue = _num(row, "ifhas_overdue_days")

    if age < 18 and milestone_overdue > WELL_CHILD_OVERDUE_DAYS:
        hits.append(
            {
                "id": "WC_OVERDUE_30",
                "theme": "Care Gap",
                "detail": (
                    f"Missed Well-Child milestone overdue by {int(milestone_overdue)} days."
                ),
            }
        )
    elif age < 18 and 0 < milestone_overdue <= WELL_CHILD_OVERDUE_DAYS:
        hits.append(
            {
                "id": "WC_DUE_SOON",
                "theme": "Care Gap",
                "detail": f"Well-Child milestone due soon ({int(milestone_overdue)} days overdue).",
            }
        )

    if age >= 18 and ifhas_overdue > IFHAS_OVERDUE_DAYS:
        hits.append(
            {
                "id": "IFHAS_OVERDUE_30",
                "theme": "Care Gap",
                "detail": f"IFHAS screening overdue by {int(ifhas_overdue)} days.",
            }
        )
    elif age >= 18 and ifhas_overdue > 0:
        hits.append(
            {
                "id": "IFHAS_OVERDUE",
                "theme": "Care Gap",
                "detail": f"IFHAS screening overdue by {int(ifhas_overdue)} days.",
            }
        )

    if bool(row.get("family_history_flag")):
        hits.append(
            {
                "id": "FHX_PRESENT",
                "theme": "Family / Genomic Context",
                "detail": "First-degree family history flag present.",
            }
        )

    genomic = row.get("consented_genomic_tier")
    if genomic == "actionable":
        hits.append(
            {
                "id": "GENOMIC_ACTIONABLE",
                "theme": "Family / Genomic Context",
                "detail": "Consented actionable genomic / metabolic risk marker.",
            }
        )

    if _num(row, "hba1c_trend") > HBA1C_TREND_THRESHOLD:
        hits.append(
            {
                "id": "HBA1C_UP",
                "theme": "Trajectory Drift",
                "detail": "Upward HbA1c trajectory across recent observations.",
            }
        )

    if _num(row, "bp_trend") > BP_TREND_THRESHOLD:
        hits.append(
            {
                "id": "BP_UP",
                "theme": "Trajectory Drift",
                "detail": "Upward blood-pressure trajectory across recent observations.",
            }
        )

    if age < 18 and _num(row, "weight_for_length_percentile_delta") > GROWTH_DRIFT_THRESHOLD:
        hits.append(
            {
                "id": "PED_GROWTH_DRIFT",
                "theme": "Trajectory Drift",
                "detail": "Upward shift in weight-for-length percentile across recent visits.",
            }
        )

    return hits
