"""Resident list and detail endpoints."""

from fastapi import APIRouter, HTTPException

from app.schemas import EngineOutput, ResidentDetail, ResidentSummary
from app.services.data_store import get_store

router = APIRouter(prefix="/residents", tags=["residents"])


@router.get("", response_model=list[ResidentSummary])
def list_residents() -> list[ResidentSummary]:
    store = get_store()
    outputs = store.engine_outputs()
    rows: list[ResidentSummary] = []
    for r in store.residents():
        out = outputs.get(r.get("resident_id", ""), {})
        rows.append(
            ResidentSummary(
                resident_id=r.get("resident_id", ""),
                display_name=r.get("display_name", ""),
                age=int(r.get("age", 0)),
                sex=r.get("sex", ""),
                district=r.get("district", ""),
                household_id=r.get("household_id", ""),
                preferred_language=r.get("preferred_language", "en"),
                resident_segment=r.get("resident_segment", ""),
                risk_tier=out.get("risk_tier"),
                pathway=out.get("pathway"),
            )
        )
    return rows


@router.get("/{resident_id}", response_model=ResidentDetail)
def get_resident(resident_id: str) -> ResidentDetail:
    store = get_store()
    resident = store.get_resident(resident_id)
    if resident is None:
        raise HTTPException(status_code=404, detail="Resident not found")
    raw_out = store.engine_outputs().get(resident_id)
    engine = EngineOutput.model_validate(raw_out) if raw_out else None
    return ResidentDetail(resident=resident, engine=engine)
