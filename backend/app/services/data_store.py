"""Load synthetic cohort and engine artifacts from disk."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.config import Settings, get_settings

CLINICAL_FIREWALL = (
    "Population outreach prioritization only — diagnostic orders require "
    "clinician confirmation under DoH guidelines."
)
SMALL_CELL_MASK = "<10 — Suppressed for Privacy"


class DataStore:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.data_dir: Path = self.settings.data_dir

    def _read_json(self, name: str) -> Any | None:
        path = self.data_dir / name
        if not path.exists():
            return None
        with path.open(encoding="utf-8") as f:
            return json.load(f)

    def meta(self) -> dict[str, Any]:
        return self._read_json("meta.json") or {
            "disclaimer": "Synthetic demo data — not real patients",
            "n_residents": 0,
            "n_households": 0,
        }

    def residents(self) -> list[dict[str, Any]]:
        raw = self._read_json("residents.json")
        if isinstance(raw, list):
            return raw
        if isinstance(raw, dict) and "residents" in raw:
            return raw["residents"]
        return []

    def households(self) -> list[dict[str, Any]]:
        raw = self._read_json("households.json")
        if isinstance(raw, list):
            return raw
        if isinstance(raw, dict) and "households" in raw:
            return raw["households"]
        return []

    def engine_outputs(self) -> dict[str, dict[str, Any]]:
        raw = self._read_json("engine_outputs.json")
        if isinstance(raw, list):
            return {row["resident_id"]: row for row in raw if "resident_id" in row}
        if isinstance(raw, dict) and "outputs" in raw:
            return {row["resident_id"]: row for row in raw["outputs"]}
        if isinstance(raw, dict):
            return raw
        return {}

    def evaluation_report(self) -> dict[str, Any] | None:
        return self._read_json("evaluation_report.json")

    def get_resident(self, resident_id: str) -> dict[str, Any] | None:
        for row in self.residents():
            if row.get("resident_id") == resident_id:
                return row
        return None


def get_store() -> DataStore:
    return DataStore()
