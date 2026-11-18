#!/usr/bin/env python3
"""Build Step 2 — run hybrid risk / uncertainty / routing engine."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from app.config import get_settings  # noqa: E402
from engine.pipeline import run_pipeline  # noqa: E402


def main() -> None:
    settings = get_settings()
    data_dir = settings.data_dir
    residents_path = data_dir / "residents.json"
    households_path = data_dir / "households.json"

    if not residents_path.exists():
        raise SystemExit(
            f"Missing {residents_path}. Run: python backend/scripts/generate_synthetic_cohort.py"
        )

    with residents_path.open(encoding="utf-8") as f:
        residents = json.load(f)
    households = []
    if households_path.exists():
        with households_path.open(encoding="utf-8") as f:
            households = json.load(f)

    outputs = run_pipeline(residents, households, seed=settings.random_seed)

    out_json = data_dir / "engine_outputs.json"
    out_csv = data_dir / "engine_outputs.csv"
    with out_json.open("w", encoding="utf-8") as f:
        json.dump(outputs, f, indent=2, ensure_ascii=False)

    flat = []
    for row in outputs:
        flat.append(
            {
                **{k: v for k, v in row.items() if k not in {"top_reasons", "rule_hits", "data_sources_used", "data_sources_not_used"}},
                "top_reasons": " | ".join(r["detail"] for r in row.get("top_reasons", [])),
                "rule_hits": ",".join(row.get("rule_hits", [])),
            }
        )
    pd.DataFrame(flat).to_csv(out_csv, index=False)
    print(f"Wrote {len(outputs)} engine outputs to {out_json}")


if __name__ == "__main__":
    main()
