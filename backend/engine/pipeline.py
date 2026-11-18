"""End-to-end engine pipeline over synthetic residents."""

from __future__ import annotations

from typing import Any

from engine.constants import CLINICAL_FIREWALL, DATA_SOURCES_NOT_USED
from engine.model import predict_proba, score_to_tier, train_calibrated_model
from engine.router import route_pathway
from engine.rules import evaluate_rules
from engine.shap_explain import top_shap_reasons
from engine.uncertainty import assess_uncertainty


def _merge_reasons(
    rule_hits: list[dict[str, str]],
    shap_reasons: list[dict[str, Any]],
    limit: int = 5,
) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    seen_themes: set[str] = set()
    for hit in rule_hits:
        theme = hit["theme"]
        if theme in seen_themes:
            continue
        seen_themes.add(theme)
        merged.append(
            {
                "rank": len(merged) + 1,
                "theme": theme,
                "detail": hit["detail"],
            }
        )
        if len(merged) >= limit:
            return merged
    for reason in shap_reasons:
        theme = reason["theme"]
        if theme in seen_themes:
            continue
        seen_themes.add(theme)
        merged.append(
            {
                "rank": len(merged) + 1,
                "theme": theme,
                "detail": reason["detail"],
            }
        )
        if len(merged) >= limit:
            break
    return merged


def _data_sources_used(row: dict[str, Any]) -> list[str]:
    used = ["Past clinic / registry visit history"]
    if int(float(row.get("ehr_months_history") or 0)) > 0:
        used.append("Longitudinal EHR & labs (synthetic Malaffi-compatible)")
    genomic = row.get("consented_genomic_tier")
    if genomic not in (None, "", "none", "null"):
        used.append("Consented Newborn/Family Wellness genomic profile")
    if bool(row.get("family_history_flag")):
        used.append("Authorized family-history flag")
    return used


def _household_bundle_hint(
    row: dict[str, Any],
    households_by_id: dict[str, dict[str, Any]],
    residents_by_hh: dict[str, list[dict[str, Any]]],
) -> str | None:
    hh_id = row.get("household_id")
    if not hh_id:
        return None
    members = residents_by_hh.get(hh_id, [])
    age = int(float(row.get("age") or 0))
    if age < 18:
        for m in members:
            if int(float(m.get("age") or 0)) >= 18 and float(m.get("ifhas_overdue_days") or 0) > 0:
                return (
                    "An adult in this household also has an overdue IFHAS checkup — "
                    "consider bundling the same clinic visit."
                )
    else:
        for m in members:
            if int(float(m.get("age") or 0)) < 18 and float(m.get("milestone_overdue_days") or 0) > 30:
                return (
                    "A child in this household has an overdue Well-Child visit — "
                    "offer a household bundle booking."
                )
    _ = households_by_id
    return None


def run_pipeline(
    residents: list[dict[str, Any]],
    households: list[dict[str, Any]] | None = None,
    seed: int = 42,
) -> list[dict[str, Any]]:
    households = households or []
    households_by_id = {h["household_id"]: h for h in households if "household_id" in h}
    residents_by_hh: dict[str, list[dict[str, Any]]] = {}
    for r in residents:
        residents_by_hh.setdefault(r.get("household_id", ""), []).append(r)

    # Attach geographic exposure onto resident for future feature use
    for r in residents:
        hh = households_by_id.get(r.get("household_id", ""), {})
        r.setdefault("geographic_exposure_index", hh.get("geographic_exposure_index", 0.0))

    model, feature_names = train_calibrated_model(residents, seed=seed)
    outputs: list[dict[str, Any]] = []

    for row in residents:
        rules = evaluate_rules(row)
        unc = assess_uncertainty(row)
        score = predict_proba(model, row, feature_names)
        tier = score_to_tier(score)
        routed = route_pathway(row, uncertainty=unc, rule_hits=rules, risk_tier=tier)
        shap_reasons = top_shap_reasons(model, row, feature_names, top_k=3)
        top_reasons = _merge_reasons(rules, shap_reasons, limit=5)
        if not top_reasons:
            top_reasons = [
                {
                    "rank": 1,
                    "theme": "Baseline",
                    "detail": "Insufficient strong drivers — routine guideline pathway.",
                }
            ]

        outputs.append(
            {
                "resident_id": row["resident_id"],
                "risk_score": round(float(score), 4),
                "risk_tier": routed["risk_tier"],
                "uncertainty": unc["uncertainty"],
                "confidence_badge": unc["confidence_badge"],
                "top_reasons": top_reasons,
                "rule_hits": [h["id"] for h in rules],
                "pathway": routed["pathway"],
                "pathway_recommendation": routed["pathway_recommendation"],
                "clinical_firewall": CLINICAL_FIREWALL,
                "data_sources_used": _data_sources_used(row),
                "data_sources_not_used": list(DATA_SOURCES_NOT_USED),
                "household_bundle_hint": _household_bundle_hint(
                    row, households_by_id, residents_by_hh
                ),
            }
        )

    return outputs
