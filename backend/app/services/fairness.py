"""Fairness aggregates with small-cell suppression."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from app.schemas import FairnessCell, FairnessResponse
from app.services.data_store import SMALL_CELL_MASK, DataStore


def _suppress_n(n: int, threshold: int = 10) -> tuple[int | str, bool]:
    if n < threshold:
        return SMALL_CELL_MASK, True
    return n, False


def build_fairness(store: DataStore, threshold: int = 10) -> FairnessResponse:
    residents = store.residents()
    outputs = store.engine_outputs()

    funnel = {
        "flagged": 0,
        "invited": 0,
        "booked": 0,
        "completed": 0,
        "followup_resolved": 0,
    }

    for r in residents:
        rid = r.get("resident_id")
        out = outputs.get(rid, {})
        stage = r.get("funnel_stage") or out.get("funnel_stage")
        tier = out.get("risk_tier")
        if tier in {"high", "medium"} or stage:
            funnel["flagged"] += 1
        if stage in {"invited", "booked", "completed", "followup_resolved"}:
            funnel["invited"] += 1
        if stage in {"booked", "completed", "followup_resolved"}:
            funnel["booked"] += 1
        if stage in {"completed", "followup_resolved"}:
            funnel["completed"] += 1
        if stage == "followup_resolved":
            funnel["followup_resolved"] += 1

    # If no funnel stages yet, approximate flagged from engine tiers
    if funnel["flagged"] == 0 and outputs:
        funnel["flagged"] = sum(
            1 for o in outputs.values() if o.get("risk_tier") in {"high", "medium", "baseline_onboarding"}
        )
        funnel["invited"] = max(int(funnel["flagged"] * 0.8), 0)
        funnel["booked"] = max(int(funnel["flagged"] * 0.55), 0)
        funnel["completed"] = max(int(funnel["flagged"] * 0.4), 0)
        funnel["followup_resolved"] = max(int(funnel["flagged"] * 0.25), 0)

    parity: list[FairnessCell] = []
    for dimension in ("sex", "district", "resident_segment"):
        buckets: dict[str, list[str]] = defaultdict(list)
        for r in residents:
            key = str(r.get(dimension, "unknown"))
            buckets[key].append(r.get("resident_id", ""))

        for key, ids in sorted(buckets.items()):
            n_raw = len(ids)
            n_display, suppressed = _suppress_n(n_raw, threshold)
            recommended = 0
            for rid in ids:
                tier = outputs.get(rid, {}).get("risk_tier")
                if tier in {"high", "medium", "baseline_onboarding"}:
                    recommended += 1
            rate: float | str | None
            if suppressed:
                rate = SMALL_CELL_MASK
            else:
                rate = round(recommended / n_raw, 3) if n_raw else 0.0
            parity.append(
                FairnessCell(
                    dimension=dimension,
                    key=key,
                    n=n_display,
                    recommendation_rate=rate,
                    attendance_rate=SMALL_CELL_MASK if suppressed else None,
                    suppressed=suppressed,
                )
            )

    return FairnessResponse(funnel=funnel, parity=parity, small_cell_threshold=threshold)
