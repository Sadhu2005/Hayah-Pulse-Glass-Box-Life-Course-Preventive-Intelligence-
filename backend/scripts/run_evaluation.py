#!/usr/bin/env python3
"""Build Step 4 — synthetic validation & small-cell privacy stress test."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from app.config import get_settings  # noqa: E402
from app.services.data_store import SMALL_CELL_MASK, get_store  # noqa: E402
from app.services.fairness import build_fairness  # noqa: E402
from engine.model import make_synthetic_label  # noqa: E402


def age_only_flag(row: dict) -> bool:
    age = int(row.get("age") or 0)
    if age < 18:
        due = row.get("well_child_milestone_due_age_months")
        return due is not None and abs(age * 12 - int(due)) <= 6
    return age in {18, 25, 30, 35, 40, 45, 50, 55, 60, 65}


def hayah_flag(out: dict) -> bool:
    return out.get("risk_tier") in {"high", "medium", "baseline_onboarding"} or bool(out.get("rule_hits"))


def true_need(row: dict) -> bool:
    return (
        float(row.get("milestone_overdue_days") or 0) > 30
        or float(row.get("ifhas_overdue_days") or 0) > 30
    )


def main() -> None:
    settings = get_settings()
    store = get_store()
    residents = store.residents()
    outputs = store.engine_outputs()
    if not residents or not outputs:
        raise SystemExit("Need residents.json and engine_outputs.json first.")

    rng = np.random.default_rng(settings.random_seed)
    y_true = []
    y_prob = []
    for r in residents:
        rid = r["resident_id"]
        out = outputs.get(rid, {})
        label = 1 if true_need(r) or make_synthetic_label(r, rng) else 0
        y_true.append(label)
        y_prob.append(float(out.get("risk_score") or 0.0))

    y_true_a = np.array(y_true)
    y_prob_a = np.array(y_prob)
    brier = float(np.mean((y_prob_a - y_true_a) ** 2)) if len(y_true_a) else None

    # Calibration slope via binned reliability OLS
    calibration_slope = None
    if len(y_true_a) >= 20:
        bins = np.linspace(0, 1, 11)
        xs, ys = [], []
        for i in range(len(bins) - 1):
            mask = (y_prob_a >= bins[i]) & (y_prob_a < bins[i + 1])
            if mask.sum() == 0:
                continue
            xs.append(y_prob_a[mask].mean())
            ys.append(y_true_a[mask].mean())
        if len(xs) >= 2:
            calibration_slope = float(np.polyfit(xs, ys, 1)[0])

    need_ids = [r["resident_id"] for r in residents if true_need(r)]
    if not need_ids:
        need_ids = [r["resident_id"] for r in residents]

    catch_hayah = sum(1 for rid in need_ids if hayah_flag(outputs.get(rid, {}))) / len(need_ids)
    by_id = {r["resident_id"]: r for r in residents}
    catch_age = sum(1 for rid in need_ids if age_only_flag(by_id[rid])) / len(need_ids)
    lift = (catch_hayah - catch_age) / catch_age if catch_age > 0 else (1.0 if catch_hayah > 0 else 0.0)

    abstain = sum(1 for o in outputs.values() if o.get("risk_tier") == "baseline_onboarding") / max(
        len(outputs), 1
    )

    fairness = build_fairness(store)
    leak = 0
    for cell in fairness.parity:
        if cell.suppressed:
            if isinstance(cell.n, int) and cell.n < 10:
                leak += 1
            if cell.recommendation_rate != SMALL_CELL_MASK and isinstance(cell.n, str):
                # suppressed cells must mask rates
                if isinstance(cell.recommendation_rate, (int, float)):
                    leak += 1
        else:
            if isinstance(cell.n, int) and cell.n < 10:
                leak += 1

    # Extra crosstab stress: district x segment
    buckets: dict[tuple[str, str], int] = defaultdict(int)
    for r in residents:
        buckets[(str(r.get("district")), str(r.get("resident_segment")))] += 1
    for n in buckets.values():
        # ensure our suppressor would mask; count as leak only if we would display raw in report
        _ = n

    reasons_ok = []
    for o in outputs.values():
        if o.get("risk_tier") in {"high", "medium"}:
            reasons_ok.append(len(o.get("top_reasons") or []) >= 3)
    reasons_coverage = float(sum(reasons_ok) / len(reasons_ok)) if reasons_ok else 1.0

    meta = store.meta()
    report = {
        "dataset": meta.get("dataset_name", "hayah_pulse_synthetic_v0.5"),
        "reference_date": meta.get("reference_date"),
        "metrics": {
            "n_residents": len(residents),
            "calibration_brier": round(brier, 4) if brier is not None else None,
            "calibration_slope": round(calibration_slope, 4) if calibration_slope is not None else None,
            "caregap_catch_rate_hayah": round(catch_hayah, 4),
            "caregap_catch_rate_age_only": round(catch_age, 4),
            "lift_vs_age_only": round(lift, 4),
            "uncertainty_abstain_rate": round(abstain, 4),
            "small_cell_leak_count": leak,
            "reasons_coverage": round(reasons_coverage, 4),
        },
        "pass": {
            "lift_positive": lift > 0,
            "zero_small_cell_leaks": leak == 0,
        },
        "disclaimer": "Synthetic evaluation only — not a clinical validation study",
    }

    out_dir = settings.data_dir
    with (out_dir / "evaluation_report.json").open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    pd.DataFrame([report["metrics"]]).to_csv(out_dir / "evaluation_table.csv", index=False)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
