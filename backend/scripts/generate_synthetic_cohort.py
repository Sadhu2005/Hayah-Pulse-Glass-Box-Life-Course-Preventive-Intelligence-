#!/usr/bin/env python3
"""Build Step 1 — generate 500 synthetic residents / 150 households."""

from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from app.config import get_settings  # noqa: E402

DISTRICTS = [
    "Al Ain",
    "Al Dhafra",
    "Abu Dhabi Island",
    "Khalifa City",
    "Mohammed Bin Zayed City",
    "Mussafah",
    "Al Shamkha",
    "Yas Island",
    "Saadiyat",
    "Rare District Zayed",  # small-cell demo
]

FIRST_NAMES = [
    "Zayed", "Fatima", "Omar", "Aisha", "Hassan", "Maryam", "Yusuf", "Noor",
    "Khalid", "Sara", "Ahmed", "Layla", "Hamad", "Hessa", "Ali", "Amna",
    "Daniel", "Maria", "Juan", "Ayesha", "Imran", "Priya", "James", "Elena",
]

SEGMENTS = {
    "infant_toddler": 0.25,
    "child_adolescent": 0.15,
    "young_adult": 0.20,
    "cardiometabolic_adult": 0.20,
    "elder": 0.10,
    "sparse_newcomer": 0.10,
}


def _allocate_segments(n: int, rng: np.random.Generator) -> list[str]:
    counts = {k: int(round(v * n)) for k, v in SEGMENTS.items()}
    # fix rounding
    while sum(counts.values()) > n:
        counts[max(counts, key=counts.get)] -= 1
    while sum(counts.values()) < n:
        counts[min(counts, key=counts.get)] += 1
    labels: list[str] = []
    for seg, c in counts.items():
        labels.extend([seg] * c)
    rng.shuffle(labels)
    return labels


def _age_for_segment(segment: str, rng: np.random.Generator) -> int:
    ranges = {
        "infant_toddler": (0, 5),
        "child_adolescent": (6, 17),
        "young_adult": (18, 35),
        "cardiometabolic_adult": (36, 64),
        "elder": (65, 88),
        "sparse_newcomer": (8, 55),
    }
    lo, hi = ranges[segment]
    return int(rng.integers(lo, hi + 1))


def main() -> None:
    settings = get_settings()
    seed = settings.random_seed
    rng = np.random.default_rng(seed)
    reference_date = date(2026, 11, 18)
    n_residents, n_households = 500, 150

    out_dir = settings.data_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    # Households
    households = []
    for i in range(1, n_households + 1):
        district = DISTRICTS[i % (len(DISTRICTS) - 1)]  # keep rare district mostly empty
        if i <= 6:
            district = "Rare District Zayed"
        households.append(
            {
                "household_id": f"HH-{i:04d}",
                "district": district,
                "member_count": 0,
                "has_child": False,
                "has_adult": False,
                "geographic_exposure_index": round(float(rng.uniform(0, 1)), 3),
            }
        )

    segments = _allocate_segments(n_residents, rng)
    residents = []

    for i in range(1, n_residents + 1):
        segment = segments[i - 1]
        hh = households[(i - 1) % n_households]
        # Bias sparse newcomers / rare district for small cells
        if segment == "sparse_newcomer" and i % 17 == 0:
            hh = households[rng.integers(0, 6)]  # rare district households

        age = _age_for_segment(segment, rng)
        sex = "female" if rng.random() < 0.5 else "male"
        ehr_months = int(rng.integers(0, 72))
        genomic = rng.choice(["actionable", "informational", "none", None], p=[0.12, 0.18, 0.5, 0.2])
        if segment == "sparse_newcomer":
            ehr_months = int(rng.integers(0, 6))
            genomic = rng.choice(["none", None], p=[0.7, 0.3])

        milestone_overdue = None
        ifhas_overdue = None
        growth_delta = None
        well_child_due = None
        last_days = int(rng.integers(10, 400))

        if age < 18:
            well_child_due = int(rng.choice([6, 12, 18, 24, 36, 48, 60]))
            if rng.random() < 0.35:
                milestone_overdue = int(rng.integers(31, 120))
            elif rng.random() < 0.2:
                milestone_overdue = int(rng.integers(1, 30))
            else:
                milestone_overdue = 0
            growth_delta = round(float(rng.normal(0, 4)), 2)
            if rng.random() < 0.15:
                growth_delta = round(float(rng.uniform(6, 15)), 2)
        else:
            if rng.random() < 0.4:
                ifhas_overdue = int(rng.integers(31, 200))
            elif rng.random() < 0.2:
                ifhas_overdue = int(rng.integers(1, 30))
            else:
                ifhas_overdue = 0

        # Compounding risk enrichment
        family_hx = bool(rng.random() < 0.25)
        if segment == "cardiometabolic_adult" and rng.random() < 0.55:
            family_hx = True
            genomic = "actionable" if rng.random() < 0.35 else genomic

        hba1c = round(float(rng.normal(0.0, 0.04)), 3)
        bp = round(float(rng.normal(0.0, 0.04)), 3)
        if family_hx and rng.random() < 0.5:
            hba1c = round(float(rng.uniform(0.06, 0.2)), 3)

        lang = rng.choice(["ar", "en", "ur", "tl"], p=[0.45, 0.4, 0.1, 0.05])
        consent = rng.choice(["opt_in", "opt_out", "unknown"], p=[0.85, 0.1, 0.05])
        last_date = reference_date - timedelta(days=last_days)

        residents.append(
            {
                "resident_id": f"R-{i:04d}",
                "display_name": f"{rng.choice(FIRST_NAMES)} {1000 + i}",
                "age": age,
                "sex": sex,
                "district": hh["district"],
                "household_id": hh["household_id"],
                "ehr_months_history": ehr_months,
                "last_well_child_or_ifhas_date": last_date.isoformat(),
                "days_since_last_preventive": last_days,
                "hba1c_trend": hba1c,
                "bp_trend": bp,
                "weight_for_length_percentile_delta": growth_delta,
                "family_history_flag": family_hx,
                "consented_genomic_tier": genomic,
                "preferred_language": lang,
                "outreach_consent_status": consent,
                "resident_segment": segment,
                "well_child_milestone_due_age_months": well_child_due,
                "milestone_overdue_days": milestone_overdue,
                "ifhas_overdue_days": ifhas_overdue,
                "chronic_condition_flags": "",
                "funnel_stage": rng.choice(
                    [None, "invited", "booked", "completed", "followup_resolved"],
                    p=[0.35, 0.2, 0.2, 0.15, 0.1],
                ),
            }
        )

    # Recompute household aggregates
    by_hh: dict[str, list[dict]] = {}
    for r in residents:
        by_hh.setdefault(r["household_id"], []).append(r)
    for h in households:
        members = by_hh.get(h["household_id"], [])
        h["member_count"] = len(members)
        h["has_child"] = any(m["age"] < 18 for m in members)
        h["has_adult"] = any(m["age"] >= 18 for m in members)

    residents_df = pd.DataFrame(residents)
    households_df = pd.DataFrame(households)

    residents_df.to_csv(out_dir / "residents.csv", index=False)
    households_df.to_csv(out_dir / "households.csv", index=False)

    with (out_dir / "residents.json").open("w", encoding="utf-8") as f:
        json.dump(residents, f, indent=2, ensure_ascii=False)
    with (out_dir / "households.json").open("w", encoding="utf-8") as f:
        json.dump(households, f, indent=2, ensure_ascii=False)

    meta = {
        "dataset_name": "hayah_pulse_synthetic_v0.5",
        "n_residents": n_residents,
        "n_households": n_households,
        "seed": seed,
        "reference_date": reference_date.isoformat(),
        "disclaimer": "Synthetic demo data — not real patients",
    }
    with (out_dir / "meta.json").open("w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"Wrote {n_residents} residents and {n_households} households to {out_dir}")


if __name__ == "__main__":
    main()
