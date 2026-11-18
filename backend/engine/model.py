"""Calibrated gradient-boosting risk stratifier.

shortcut: full train/persist lands in Build Step 2; heuristic score keeps API/demo path unblocked until then.
"""

from __future__ import annotations

from typing import Any

import numpy as np


FEATURE_COLUMNS = [
    "age",
    "ehr_months_history",
    "days_since_last_preventive",
    "hba1c_trend",
    "bp_trend",
    "weight_for_length_percentile_delta",
    "family_history_flag",
    "milestone_overdue_days",
    "ifhas_overdue_days",
]


def _to_float(value: Any, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def make_synthetic_label(row: dict[str, Any], rng: np.random.Generator) -> int:
    """Generative elevated-need label for synthetic training / eval."""
    score = 0.0
    score += 0.35 if _to_float(row.get("milestone_overdue_days")) > 30 else 0.0
    score += 0.35 if _to_float(row.get("ifhas_overdue_days")) > 30 else 0.0
    score += 0.2 if bool(row.get("family_history_flag")) else 0.0
    score += 0.15 if row.get("consented_genomic_tier") == "actionable" else 0.0
    score += 0.15 if _to_float(row.get("hba1c_trend")) > 0.05 else 0.0
    score += 0.1 if _to_float(row.get("bp_trend")) > 0.05 else 0.0
    score += 0.1 if _to_float(row.get("weight_for_length_percentile_delta")) > 5 else 0.0
    score += rng.normal(0, 0.05)
    return int(score >= 0.45)


def heuristic_risk_score(row: dict[str, Any]) -> float:
    """Deterministic stand-in until calibrated GB model is trained on cohort."""
    score = 0.05
    score += min(_to_float(row.get("milestone_overdue_days")) / 120.0, 0.35)
    score += min(_to_float(row.get("ifhas_overdue_days")) / 180.0, 0.35)
    score += 0.15 if bool(row.get("family_history_flag")) else 0.0
    score += 0.12 if row.get("consented_genomic_tier") == "actionable" else 0.0
    score += min(max(_to_float(row.get("hba1c_trend")), 0.0) * 2.0, 0.15)
    score += min(max(_to_float(row.get("bp_trend")), 0.0) * 2.0, 0.1)
    return float(np.clip(score, 0.0, 1.0))


def score_to_tier(score: float) -> str:
    if score >= 0.65:
        return "high"
    if score >= 0.35:
        return "medium"
    return "low"


def train_calibrated_model(rows: list[dict[str, Any]], seed: int = 42):  # noqa: ANN201
    """Train GradientBoosting + CalibratedClassifierCV when sklearn available.

    Returns (model, feature_names) or (None, FEATURE_COLUMNS) if training skipped.
    """
    if len(rows) < 50:
        return None, FEATURE_COLUMNS

    from sklearn.calibration import CalibratedClassifierCV
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.model_selection import train_test_split

    rng = np.random.default_rng(seed)
    X = np.array([[_to_float(r.get(c)) for c in FEATURE_COLUMNS] for r in rows], dtype=float)
    y = np.array([make_synthetic_label(r, rng) for r in rows], dtype=int)
    if len(np.unique(y)) < 2:
        return None, FEATURE_COLUMNS

    X_train, X_cal, y_train, y_cal = train_test_split(
        X, y, test_size=0.25, random_state=seed, stratify=y
    )
    base = GradientBoostingClassifier(random_state=seed)
    base.fit(X_train, y_train)
    try:
        from sklearn.frozen import FrozenEstimator

        calibrated = CalibratedClassifierCV(FrozenEstimator(base), method="isotonic")
    except Exception:
        calibrated = CalibratedClassifierCV(base, method="isotonic", cv=3)
    calibrated.fit(X_cal, y_cal)
    return calibrated, FEATURE_COLUMNS


def predict_proba(model: Any, row: dict[str, Any], feature_names: list[str]) -> float:
    if model is None:
        return heuristic_risk_score(row)
    x = np.array([[_to_float(row.get(c)) for c in feature_names]], dtype=float)
    proba = model.predict_proba(x)[0]
    # positive class index 1 when available
    return float(proba[1] if len(proba) > 1 else proba[0])
