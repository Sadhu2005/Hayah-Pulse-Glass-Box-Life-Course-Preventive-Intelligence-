"""Feature attribution — SHAP when model available, else rule/heuristic hybrid."""

from __future__ import annotations

from typing import Any

from engine.model import FEATURE_COLUMNS, _to_float


def _readable(name: str, value: float) -> tuple[str, str]:
    mapping = {
        "milestone_overdue_days": ("Care Gap", "Well-Child milestone overdue contribution"),
        "ifhas_overdue_days": ("Care Gap", "IFHAS overdue contribution"),
        "family_history_flag": ("Family / Genomic Context", "Family history contribution"),
        "hba1c_trend": ("Trajectory Drift", "HbA1c trajectory contribution"),
        "bp_trend": ("Trajectory Drift", "Blood-pressure trajectory contribution"),
        "weight_for_length_percentile_delta": (
            "Trajectory Drift",
            "Growth percentile drift contribution",
        ),
        "ehr_months_history": ("Data Completeness", "Longitudinal EHR depth contribution"),
        "days_since_last_preventive": ("Care Gap", "Days since last preventive visit"),
        "age": ("Demographics", "Age contribution to prioritization"),
    }
    theme, detail = mapping.get(name, ("Model Factor", f"{name} contribution"))
    return theme, f"{detail} (value={value:.3f})"


def top_shap_reasons(
    model: Any,
    row: dict[str, Any],
    feature_names: list[str] | None = None,
    top_k: int = 3,
) -> list[dict[str, Any]]:
    names = feature_names or FEATURE_COLUMNS
    values = {c: _to_float(row.get(c)) for c in names}

    if model is not None:
        try:
            import numpy as np
            import shap

            explainer = shap.TreeExplainer(model.estimator if hasattr(model, "estimator") else model)
            x = np.array([[values[c] for c in names]], dtype=float)
            shap_values = explainer.shap_values(x)
            if isinstance(shap_values, list):
                shap_values = shap_values[1]
            contribs = list(zip(names, shap_values[0].tolist(), strict=False))
            contribs.sort(key=lambda t: abs(t[1]), reverse=True)
            reasons = []
            for rank, (name, _sv) in enumerate(contribs[:top_k], start=1):
                theme, detail = _readable(name, values[name])
                reasons.append({"rank": rank, "theme": theme, "detail": detail})
            return reasons
        except Exception:
            pass

    # Heuristic attribution by magnitude of key drivers
    scored = sorted(values.items(), key=lambda kv: abs(kv[1]), reverse=True)
    reasons = []
    for rank, (name, value) in enumerate(scored[:top_k], start=1):
        if abs(value) < 1e-9 and name not in {"family_history_flag"}:
            continue
        theme, detail = _readable(name, value)
        reasons.append({"rank": rank, "theme": theme, "detail": detail})
    return reasons
