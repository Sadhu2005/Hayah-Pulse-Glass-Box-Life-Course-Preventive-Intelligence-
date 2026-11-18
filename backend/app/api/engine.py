"""Engine artifact endpoints."""

from fastapi import APIRouter, HTTPException

from app.schemas import EngineOutput
from app.services.data_store import get_store

router = APIRouter(prefix="/engine", tags=["engine"])


@router.get("/outputs", response_model=list[EngineOutput])
def list_outputs() -> list[EngineOutput]:
    store = get_store()
    return [EngineOutput.model_validate(v) for v in store.engine_outputs().values()]


@router.get("/outputs/{resident_id}", response_model=EngineOutput)
def get_output(resident_id: str) -> EngineOutput:
    store = get_store()
    raw = store.engine_outputs().get(resident_id)
    if raw is None:
        raise HTTPException(status_code=404, detail="Engine output not found")
    return EngineOutput.model_validate(raw)
